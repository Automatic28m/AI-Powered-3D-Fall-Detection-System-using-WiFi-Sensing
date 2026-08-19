import cv2
import mediapipe as mp
import numpy as np
import serial
import csv
import threading
import time
import math
import os
import colorsys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Configuration ---
PORT = os.getenv('SERIAL_PORT') or os.getenv('PORT') or 'COM10'
BAUD_RATE = int(os.getenv('BAUD_RATE', 921600))
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 1))
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', 15)) # Adjust as needed
HEATMAP_HEIGHT = 400
MAX_LIVE_FRAMES = 500 # Size of sliding window for live heatmap
PAD_LEFT = 60
PAD_BOTTOM = 40

# Precompute 64 distinct colors for the subcarrier lines
SUBCARRIER_COLORS = []
for i in range(64):
    hue = i / 64.0
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    SUBCARRIER_COLORS.append((int(rgb[2]*255), int(rgb[1]*255), int(rgb[0]*255))) # BGR

# --- Shared Variables ---
app_state = "INIT"
start_time = 0
csi_data_list = [] # List of tuples: (timestamp, rssi, amplitude_array)
video_frames_list = [] # List of tuples: (timestamp, blank_frame_with_pose)
csi_matrix_live = np.zeros((64, MAX_LIVE_FRAMES))

# --- Mediapipe Setup ---
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

def serial_thread():
    global app_state, csi_data_list, start_time, csi_matrix_live
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        print(f"[Serial] Connected to {PORT}")
    except Exception as e:
        print(f"[Serial] Connection failed: {e}")
        app_state = "ERROR"
        return

    # Wait until main thread sets state to RECORDING
    print("[Serial] Waiting for countdown...")
    while app_state == "INIT":
        if ser.in_waiting > 0:
            ser.read(ser.in_waiting) # Smoothly drain the buffer
        time.sleep(0.01)
        
    print("[Serial] Started reading CSI...")
    while app_state == "RECORDING":
        try:
            if ser.in_waiting > 0:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw_line.startswith("CSI_DATA"):
                    parts = raw_line.split(',')
                    if len(parts) > 2:
                        rssi = int(parts[1])
                        iq_data = [int(x) for x in parts[2:]]
                        
                        # Calculate amplitude for 64 subcarriers
                        amplitude = [
                            math.sqrt(iq_data[i]**2 + iq_data[i+1]**2)
                            for i in range(0, len(iq_data)-1, 2)
                        ]
                        
                        if len(amplitude) >= 64:
                            csi_data_list.append((time.time(), rssi, amplitude[:64]))
                            
                            # Update live sliding window
                            csi_matrix_live[:, :-1] = csi_matrix_live[:, 1:]
                            csi_matrix_live[:, -1] = amplitude[:64]
                else:
                    # Ignore non-CSI lines
                    pass
        except Exception as e:
            print(f"[Serial Error] {e}")
            
    print(f"[Serial] Finished reading. Collected {len(csi_data_list)} packets.")
    ser.close()

def generate_line_graph(matrix, frame_w, frame_h):
    """
    Renders a multi-line graph of Amplitude vs Time with Background Subtraction.
    """
    # 1. Filter out 'dead' subcarriers
    row_sums = np.sum(matrix, axis=1)
    valid_matrix = matrix[row_sums > 1.0]
    
    if valid_matrix.shape[0] == 0:
        valid_matrix = matrix 
        
    # 2. Background Subtraction
    # Subtract the mean of each subcarrier to remove static room baseline
    mean_per_subcarrier = np.mean(valid_matrix, axis=1, keepdims=True)
    centered_matrix = valid_matrix - mean_per_subcarrier
        
    # 3. Lightly smooth the data over time to remove high-frequency noise
    smoothed_matrix = cv2.blur(centered_matrix.astype(np.float32), (5, 1))
    
    # 4. Setup canvas
    plot_w = frame_w - PAD_LEFT
    plot_h = frame_h - PAD_BOTTOM
    final_img = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)
    
    y_min_amp = -25.0
    y_max_amp = 25.0
    amp_range = y_max_amp - y_min_amp
    
    # 5. Draw Grid and Y-axis tick labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    for amp_val in [-20, -10, 0, 10, 20]:
        y = int(plot_h - ((amp_val - y_min_amp) / amp_range * plot_h))
        y = max(0, min(plot_h, y))
        
        # Highlight the 0-baseline with a bright green line
        if amp_val == 0:
            cv2.line(final_img, (PAD_LEFT, y), (frame_w, y), (100, 255, 100), 2, lineType=cv2.LINE_AA)
        else:
            cv2.line(final_img, (PAD_LEFT, y), (frame_w, y), (50, 50, 50), 1, lineType=cv2.LINE_AA)
            
        text = str(amp_val)
        (tw, th), _ = cv2.getTextSize(text, font, 0.5, 1)
        cv2.putText(final_img, text, (PAD_LEFT - tw - 5, y + th//2), font, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

    # 6. Draw Subcarrier Lines
    num_subcarriers, T = smoothed_matrix.shape
    if T > 1:
        x_coords = np.linspace(PAD_LEFT, frame_w - 1, T).astype(np.int32)
        y_coords_scaled = plot_h - ((smoothed_matrix - y_min_amp) / amp_range * plot_h)
        y_coords_scaled = np.clip(y_coords_scaled, 0, plot_h).astype(np.int32)
        
        for m in range(num_subcarriers):
            pts = np.column_stack((x_coords, y_coords_scaled[m]))
            pts = pts.reshape((-1, 1, 2))
            color_idx = m % len(SUBCARRIER_COLORS)
            cv2.polylines(final_img, [pts], isClosed=False, color=SUBCARRIER_COLORS[color_idx], thickness=1, lineType=cv2.LINE_AA)
            
    # 7. Draw Y-axis title
    text_y = "Amplitude Dev."
    (text_w, text_h), _ = cv2.getTextSize(text_y, font, 0.6, 2)
    text_img = np.zeros((text_h + 10, text_w + 10, 3), dtype=np.uint8)
    cv2.putText(text_img, text_y, (5, text_h + 5), font, 0.6, (255, 255, 255), 2)
    text_img_rotated = cv2.rotate(text_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    rh, rw = text_img_rotated.shape[:2]
    y_offset = (plot_h - rh) // 2
    x_offset = max(0, 5) # Far left edge
    
    final_img[y_offset:y_offset+rh, x_offset:x_offset+rw] = text_img_rotated
    
    # 7. Draw X-axis text
    text_x = "Time"
    (text_w, text_h), _ = cv2.getTextSize(text_x, font, 0.6, 2)
    x_offset = PAD_LEFT + (plot_w - text_w) // 2
    y_offset = plot_h + (PAD_BOTTOM - text_h) // 2 + text_h
    cv2.putText(final_img, text_x, (x_offset, y_offset), font, 0.6, (255, 255, 255), 2)
    
    return final_img

def main():
    global app_state, start_time, video_frames_list, csi_data_list, csi_matrix_live
    
    # 1. Start Serial Thread
    t_serial = threading.Thread(target=serial_thread)
    t_serial.daemon = True
    t_serial.start()
    
    # 2. Open Camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[Camera] Cannot open camera.")
        app_state = "ERROR"
        return
        
    ret, frame = cap.read()
    if not ret:
        print("[Camera] Cannot read frame.")
        app_state = "ERROR"
        return
        
    frame_h, frame_w = frame.shape[:2]
    
    print("[Camera] Camera initialized. Starting countdown...")
    for i in range(5, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
        
    if app_state == "ERROR":
        return
        
    # Start Recording
    app_state = "RECORDING"
    start_time = time.time()
    print(f"--- RECORDING FOR {RECORD_SECONDS} SECONDS ---")
    
    # Play a single beep sound to indicate recording has started (macOS specific)
    os.system("afplay /System/Library/Sounds/Ping.aiff &")
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > RECORD_SECONDS:
            app_state = "DONE"
            break
            
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the image and find poses
        results = pose.process(image_rgb)
        
        # Create a black background (privacy preserving)
        blank_frame = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)
        
        # Draw pose on black background
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                blank_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
            )
            
        video_frames_list.append((time.time(), blank_frame.copy()))
        
        # --- Live Visualization (Multi-line Plot) ---
        live_heatmap_padded = generate_line_graph(csi_matrix_live, frame_w, HEATMAP_HEIGHT)
        
        # Draw real-time indicator at the very end of the plot area
        plot_h = HEATMAP_HEIGHT - PAD_BOTTOM
        cv2.line(live_heatmap_padded, (frame_w - 2, 0), (frame_w - 2, plot_h), (255, 255, 255), 2)
        
        # Combine pose and heatmap
        live_combined = np.vstack((blank_frame, live_heatmap_padded))
        
        # Show remaining time on the frame
        rem_time = max(0, RECORD_SECONDS - elapsed)
        cv2.putText(live_combined, f"Recording: {rem_time:.1f}s left", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
        cv2.imshow('Live Recording (Pose + CSI Timeline)', live_combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            app_state = "DONE"
            break
            
    # Play a double beep to indicate recording is finished
    os.system("(afplay /System/Library/Sounds/Ping.aiff; sleep 0.15; afplay /System/Library/Sounds/Ping.aiff) &")
            
    cap.release()
    cv2.destroyAllWindows()
    print(f"[Camera] Finished recording. Collected {len(video_frames_list)} frames.")
    
    # Wait for serial thread to wrap up
    time.sleep(0.5) 
    
    if len(csi_data_list) == 0 or len(video_frames_list) == 0:
        print("Error: No data collected.")
        return
        
    print("\n--- Starting Post-Processing ---")
    
    # --- Post-Processing: CSV ---
    timestamp_str = str(int(time.time()))
    csv_filename = f"CSI_sync_data_{timestamp_str}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        headers = ["Timestamp", "RSSI"] + [f"Sub_{i}" for i in range(64)]
        writer.writerow(headers)
        for data in csi_data_list:
            writer.writerow([data[0], data[1]] + data[2])
    print(f"[Export] CSI data saved to {csv_filename}")
    
    # --- Post-Processing: Multi-line Graph Generation ---
    csi_matrix_full = np.array([data[2] for data in csi_data_list]).T
    heatmap_padded = generate_line_graph(csi_matrix_full, frame_w, HEATMAP_HEIGHT)

    # --- Post-Processing: Video Compilation ---
    video_filename = f"synchronized_output_{timestamp_str}.mp4"
    actual_duration = video_frames_list[-1][0] - video_frames_list[0][0]
    fps = len(video_frames_list) / actual_duration if actual_duration > 0 else 30.0
    
    final_h = frame_h + HEATMAP_HEIGHT
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_w, final_h))
    
    print(f"[Export] Rendering synchronized video at {fps:.1f} FPS...")
    
    csi_start_time = csi_data_list[0][0]
    csi_end_time = csi_data_list[-1][0]
    csi_duration = csi_end_time - csi_start_time
    
    plot_w = frame_w - PAD_LEFT
    plot_h = HEATMAP_HEIGHT - PAD_BOTTOM
    
    for i, (frame_ts, pose_frame) in enumerate(video_frames_list):
        progress = 0
        if csi_duration > 0:
            progress = (frame_ts - csi_start_time) / csi_duration
            progress = max(0.0, min(1.0, progress))
            
        x_indicator = PAD_LEFT + int(progress * (plot_w - 1))
        
        current_heatmap = heatmap_padded.copy()
        cv2.line(current_heatmap, (x_indicator, 0), (x_indicator, plot_h), (255, 255, 255), 2)
        
        combined_frame = np.vstack((pose_frame, current_heatmap))
        out.write(combined_frame)
        
        if i % 30 == 0:
            print(f"  Rendering frame {i}/{len(video_frames_list)}...")
            
    out.release()
    print(f"[Export] Video saved to {video_filename}")
    print("--- Process Complete! ---")

if __name__ == "__main__":
    main()
