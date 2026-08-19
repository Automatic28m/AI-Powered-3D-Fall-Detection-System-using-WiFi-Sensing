import cv2
import serial
import csv
import threading
import time
import math
import os
import colorsys
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Configuration ---
PORT = os.getenv('SERIAL_PORT') or os.getenv('PORT') or 'COM10'
BAUD_RATE = int(os.getenv('BAUD_RATE', 921600))
WAIT_SECONDS = int(os.getenv('WAIT_SECONDS', 5))
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS', 30))
MAX_LIVE_FRAMES = 500
PAD_LEFT = 60
PAD_BOTTOM = 40
FRAME_W = 1000
FRAME_H = 400

# Precompute 64 distinct colors for the subcarrier lines
SUBCARRIER_COLORS = []
for i in range(64):
    hue = i / 64.0
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    SUBCARRIER_COLORS.append((int(rgb[2]*255), int(rgb[1]*255), int(rgb[0]*255))) # BGR

# --- Shared Variables ---
app_state = "INIT"
csi_data_list = []
csv_filename = f"./experiment/csi_exp_{int(time.time())}.csv"

def serial_thread():
    global app_state, csi_data_list, csv_filename
    
    try:
        ser = serial.Serial(PORT, BAUD_RATE)
        print(f"[Serial] Connected to {PORT}")
    except Exception as e:
        print(f"[Serial] Error opening port: {e}")
        app_state = "ERROR"
        return

    # Ensure experiment folder exists
    os.makedirs("./experiment", exist_ok=True)
    
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "RSSI"] + [f"Sub_{i}" for i in range(64)])
        
        while app_state == "RECORDING":
            if ser.in_waiting > 0:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                if raw_line.startswith("CSI_DATA"):
                    try:
                        parts = raw_line.split(',')
                        rssi = int(parts[1])
                        iq_data = [int(x) for x in parts[2:]]
                        
                        amplitude = [
                            math.sqrt(iq_data[i]**2 + iq_data[i+1]**2) 
                            for i in range(0, len(iq_data)-1, 2)
                        ]
                        
                        if len(amplitude) >= 64:
                            # Save to memory for live plot
                            ts = time.time()
                            csi_data_list.append((ts, rssi, amplitude[:64]))
                            # Save to CSV
                            writer.writerow([ts, rssi] + amplitude[:64])
                    except Exception:
                        pass
                        
    print(f"[Serial] Finished reading. Collected {len(csi_data_list)} packets. Saved to {csv_filename}")
    ser.close()

def generate_line_graph(matrix, frame_w, frame_h):
    """
    Renders a multi-line graph of Amplitude vs Time with Background Subtraction.
    """
    row_sums = np.sum(matrix, axis=1)
    valid_matrix = matrix[row_sums > 1.0]
    
    if valid_matrix.shape[0] == 0:
        valid_matrix = matrix 
        
    mean_per_subcarrier = np.mean(valid_matrix, axis=1, keepdims=True)
    centered_matrix = valid_matrix - mean_per_subcarrier
        
    smoothed_matrix = cv2.blur(centered_matrix.astype(np.float32), (5, 1))
    
    plot_w = frame_w - PAD_LEFT
    plot_h = frame_h - PAD_BOTTOM
    final_img = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)
    
    y_min_amp = -25.0
    y_max_amp = 25.0
    amp_range = y_max_amp - y_min_amp
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    for amp_val in [-20, -10, 0, 10, 20]:
        y = int(plot_h - ((amp_val - y_min_amp) / amp_range * plot_h))
        y = max(0, min(plot_h, y))
        
        if amp_val == 0:
            cv2.line(final_img, (PAD_LEFT, y), (frame_w, y), (100, 255, 100), 2, lineType=cv2.LINE_AA)
        else:
            cv2.line(final_img, (PAD_LEFT, y), (frame_w, y), (50, 50, 50), 1, lineType=cv2.LINE_AA)
            
        text = str(amp_val)
        (tw, th), _ = cv2.getTextSize(text, font, 0.5, 1)
        cv2.putText(final_img, text, (PAD_LEFT - tw - 5, y + th//2), font, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

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
            
    text_y = "Amplitude Dev."
    (text_w, text_h), _ = cv2.getTextSize(text_y, font, 0.6, 2)
    text_img = np.zeros((text_h + 10, text_w + 10, 3), dtype=np.uint8)
    cv2.putText(text_img, text_y, (5, text_h + 5), font, 0.6, (255, 255, 255), 2)
    text_img_rotated = cv2.rotate(text_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    rh, rw = text_img_rotated.shape[:2]
    y_offset = (plot_h - rh) // 2
    x_offset = max(0, 5) 
    final_img[y_offset:y_offset+rh, x_offset:x_offset+rw] = text_img_rotated
    
    text_x = "Time"
    (text_w, text_h), _ = cv2.getTextSize(text_x, font, 0.6, 2)
    x_offset = PAD_LEFT + (plot_w - text_w) // 2
    y_offset = plot_h + (PAD_BOTTOM - text_h) // 2 + text_h
    cv2.putText(final_img, text_x, (x_offset, y_offset), font, 0.6, (255, 255, 255), 2)
    
    return final_img

def main():
    global app_state
    
    cv2.namedWindow('CSI Live Plot', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('CSI Live Plot', FRAME_W, FRAME_H)
    
    # --- COUNTDOWN ---
    app_state = "COUNTDOWN"
    start_time = time.time()
    
    print(f"--- COUNTDOWN {WAIT_SECONDS} SECONDS ---")
    
    while True:
        elapsed = time.time() - start_time
        remaining = WAIT_SECONDS - elapsed
        if remaining <= 0:
            break
            
        frame = np.zeros((FRAME_H, FRAME_W, 3), dtype=np.uint8)
        text = f"Recording in {remaining:.1f}s"
        font = cv2.FONT_HERSHEY_SIMPLEX
        (tw, th), _ = cv2.getTextSize(text, font, 1.5, 3)
        cv2.putText(frame, text, ((FRAME_W - tw) // 2, (FRAME_H + th) // 2), font, 1.5, (0, 255, 255), 3)
        
        cv2.imshow('CSI Live Plot', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            app_state = "DONE"
            cv2.destroyAllWindows()
            return
            
    # --- RECORDING ---
    app_state = "RECORDING"
    record_start_time = time.time()
    os.system("afplay /System/Library/Sounds/Ping.aiff &")
    print(f"--- RECORDING FOR {RECORD_SECONDS} SECONDS ---")
    
    t = threading.Thread(target=serial_thread)
    t.start()
    
    while True:
        elapsed = time.time() - record_start_time
        remaining = RECORD_SECONDS - elapsed
        
        if remaining <= 0:
            app_state = "DONE"
            break
            
        if len(csi_data_list) > 0:
            # Grab recent frames
            recent_data = csi_data_list[-MAX_LIVE_FRAMES:]
            csi_matrix_live = np.array([data[2] for data in recent_data]).T
            
            # Ensure matrix has enough width to plot smoothly
            if csi_matrix_live.shape[1] < MAX_LIVE_FRAMES:
                padding = np.zeros((64, MAX_LIVE_FRAMES - csi_matrix_live.shape[1]))
                csi_matrix_live = np.hstack((padding, csi_matrix_live))
                
            plot_frame = generate_line_graph(csi_matrix_live, FRAME_W, FRAME_H)
            
            # Draw remaining time
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{remaining:.1f}s remaining"
            cv2.putText(plot_frame, text, (FRAME_W - 200, 30), font, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('CSI Live Plot', plot_frame)
            
        if cv2.waitKey(10) & 0xFF == ord('q'):
            app_state = "DONE"
            break
            
    os.system("(afplay /System/Library/Sounds/Ping.aiff; sleep 0.15; afplay /System/Library/Sounds/Ping.aiff) &")
    
    print("[Main] Waiting for serial thread to finish...")
    t.join()
    cv2.destroyAllWindows()
    print("[Main] Collection complete.")

if __name__ == "__main__":
    main()
