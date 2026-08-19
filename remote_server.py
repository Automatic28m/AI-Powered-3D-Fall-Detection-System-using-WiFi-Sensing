import http.server
import socketserver
import subprocess
import json
import socket
import urllib.parse
import glob
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

PORT = int(os.getenv('SERVER_PORT', 8000))
current_process = None

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CSI Remote Control</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            font-family: 'Outfit', sans-serif;
            color: white;
            overflow: hidden;
            -webkit-tap-highlight-color: transparent;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 50px 40px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
            width: 80%;
            max-width: 400px;
        }

        h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: -webkit-linear-gradient(#fff, #aaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-text {
            font-size: 1.2rem;
            font-weight: 600;
            color: #888;
            margin: 0;
            transition: color 0.3s ease;
        }

        .btn-container {
            position: relative;
            width: 200px;
            height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .btn {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: none;
            outline: none;
            cursor: pointer;
            font-size: 1.5rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            color: white;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background: linear-gradient(145deg, #2a5298, #1e3c72);
            box-shadow:  10px 10px 30px rgba(0,0,0,0.5), -10px -10px 30px rgba(255,255,255,0.05);
            z-index: 10;
        }

        .btn:active {
            transform: scale(0.9);
        }
        
        /* Waiting State (Countdown before recording) */
        .btn.waiting {
            background: linear-gradient(145deg, #f2994a, #f2c94c);
            animation: pulse-yellow 1s infinite;
            font-size: 4rem; /* Big number for countdown */
        }
        
        @keyframes pulse-yellow {
            0% { box-shadow: 0 0 0 0 rgba(242, 201, 76, 0.7); }
            70% { box-shadow: 0 0 0 30px rgba(242, 201, 76, 0); }
            100% { box-shadow: 0 0 0 0 rgba(242, 201, 76, 0); }
        }

        /* Running State (Countdown during recording) */
        .btn.running {
            background: linear-gradient(145deg, #ff416c, #ff4b2b);
            animation: pulse-red 1.5s infinite;
            font-size: 4rem; /* Big number for countdown */
        }

        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(255, 75, 43, 0.7); }
            70% { box-shadow: 0 0 0 30px rgba(255, 75, 43, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 75, 43, 0); }
        }

        /* Cooldown State */
        .btn.cooldown {
            background: linear-gradient(145deg, #11998e, #38ef7d);
            transform: scale(1);
            pointer-events: none;
            font-size: 1.5rem;
        }

        /* Rename Form Styles */
        .rename-form {
            display: none;
            flex-direction: column;
            gap: 15px;
            width: 100%;
            margin-top: 10px;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .rename-form input {
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1.1rem;
            font-family: 'Outfit', sans-serif;
            outline: none;
        }
        
        .rename-form input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        .btn-small {
            padding: 15px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(145deg, #f2994a, #f2c94c);
            color: #111;
            font-size: 1.1rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .btn-small:active {
            transform: scale(0.95);
        }
    </style>
</head>
<body>

    <div class="glass-panel">
        <h1>CSI Remote</h1>
        
        <div class="btn-container">
            <button class="btn" id="record-btn" onclick="startRecording()">START</button>
        </div>
        
        <p class="status-text" id="status-label">Ready</p>
        
        <!-- File Renaming Form -->
        <div class="rename-form" id="rename-form">
            <input type="text" id="pos-input" placeholder="Position (e.g. 1)">
            <input type="text" id="action-input" placeholder="Action (e.g. walking)">
            <button class="btn-small" onclick="saveName()">SAVE & RENAME</button>
        </div>
    </div>

    <script>
        const btn = document.getElementById('record-btn');
        const statusLabel = document.getElementById('status-label');
        const renameForm = document.getElementById('rename-form');
        const posInput = document.getElementById('pos-input');
        const actionInput = document.getElementById('action-input');
        
        let isPolling = false;

        async function startRecording() {
            if (btn.classList.contains('running') || btn.classList.contains('cooldown') || btn.classList.contains('waiting')) return;

            try {
                await fetch('/start', { method: 'POST' });
            } catch (e) {
                console.error(e);
                alert("Failed to start server. Is it running?");
                return;
            }

            // Reset UI and start PRE-collection countdown
            renameForm.style.display = 'none';
            btn.classList.add('waiting');
            statusLabel.style.color = "#f2c94c";
            
            let preCount = 5;
            btn.innerText = preCount;
            statusLabel.innerText = "Get Ready...";
            
            const preCountdownInterval = setInterval(() => {
                preCount--;
                if (preCount > 0) {
                    btn.innerText = preCount;
                } else {
                    clearInterval(preCountdownInterval);
                    
                    // Transition to red recording state (WHILE collection countdown)
                    btn.classList.remove('waiting');
                    btn.classList.add('running');
                    
                    let recordCount = 30; // 30 seconds of recording
                    btn.innerText = recordCount;
                    statusLabel.innerText = "Collecting CSI Data...";
                    statusLabel.style.color = "#ff4b2b";
                    
                    const recordCountdownInterval = setInterval(() => {
                        recordCount--;
                        if (recordCount > 0 && btn.classList.contains('running')) {
                            btn.innerText = recordCount;
                        } else {
                            clearInterval(recordCountdownInterval);
                        }
                    }, 1000);
                    
                    if (!isPolling) {
                        isPolling = true;
                        pollStatus();
                    }
                }
            }, 1000);
        }

        async function pollStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.status === 'idle') {
                    // Recording finished!
                    btn.classList.remove('running');
                    btn.classList.add('cooldown');
                    btn.innerText = "DONE!";
                    statusLabel.innerText = "Saved. Enter name below:";
                    statusLabel.style.color = "#38ef7d";
                    
                    // Show rename form
                    renameForm.style.display = 'flex';
                    posInput.focus();
                    
                    isPolling = false;
                } else {
                    // Still running, poll again in 1 second
                    setTimeout(pollStatus, 1000);
                }
            } catch (e) {
                console.error(e);
                setTimeout(pollStatus, 1000);
            }
        }
        
        async function saveName() {
            const pos = encodeURIComponent(posInput.value.trim());
            const action = encodeURIComponent(actionInput.value.trim());
            
            if (!pos || !action) {
                alert("Please enter both Position and Action.");
                return;
            }
            
            try {
                await fetch(`/rename?pos=${pos}&action=${action}`, { method: 'POST' });
                
                // Hide form and reset
                renameForm.style.display = 'none';
                posInput.value = '';
                actionInput.value = '';
                resetUI();
                
                statusLabel.innerText = "File Renamed Successfully!";
                statusLabel.style.color = "#38ef7d";
                setTimeout(() => {
                    if (!isPolling) {
                        statusLabel.innerText = "Ready";
                        statusLabel.style.color = "#888";
                    }
                }, 3000);
                
            } catch (e) {
                console.error(e);
                alert("Error saving name!");
            }
        }

        function resetUI() {
            btn.classList.remove('running', 'cooldown', 'waiting');
            btn.innerText = "START";
            statusLabel.innerText = "Ready";
            statusLabel.style.color = "#888";
        }
    </script>
</body>
</html>
"""

class RemoteControlHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global current_process
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path == '/status':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            status = "idle"
            if current_process is not None:
                if current_process.poll() is None: # Still running
                    status = "running"
                else:
                    current_process = None # Finished
                    
            response = json.dumps({"status": status})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global current_process
        if self.path == '/start':
            if current_process is None or current_process.poll() is not None:
                print("\n[Server] Received START command from phone. Launching collect_csi.py...")
                current_process = subprocess.Popen([sys.executable, "collect_csi.py"])
                
            self.send_response(200)
            self.end_headers()
            
        elif self.path.startswith('/rename'):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            pos = query.get('pos', [''])[0].strip()
            action = query.get('action', [''])[0].strip()
            
            if pos and action:
                list_of_files = glob.glob('./experiment/*.csv')
                if list_of_files:
                    # Find the newest CSV file (the one just recorded)
                    latest_file = max(list_of_files, key=os.path.getctime)
                    new_name = f"./experiment/pos{pos}_{action}.csv"
                    
                    try:
                        os.rename(latest_file, new_name)
                        print(f"\n[Server] Renamed {latest_file} -> {new_name}")
                    except Exception as e:
                        print(f"[Server] Failed to rename file: {e}")
            
            self.send_response(200)
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
    ip = get_local_ip()
    handler = RemoteControlHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("="*60)
        print("📱 CSI REMOTE CONTROL SERVER IS RUNNING")
        print("="*60)
        print(f"1. Connect your phone to the same Wi-Fi network.")
        print(f"2. Open Safari/Chrome on your phone and go to:")
        print(f"   --->  http://{ip}:{PORT}  <---")
        print("="*60)
        print("Press Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
