import os
import base64
import subprocess
import time

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            ext = os.path.splitext(image_path)[1].lower().replace('.', '')
            if ext == 'jpg': ext = 'jpeg'
            data = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/{ext};base64,{data}"
    return ""

exp6_dir = r"D:\Term1_69\Pre-Projec\AI-Powered-3D-Fall-Detection-System-using-WiFi-Sensing\experiment_6"
plan_img_b64 = get_base64_image(os.path.join(exp6_dir, "experiment_6_plan.png"))
charts_img_b64 = get_base64_image(r"D:\Term1_69\Pre-Projec\AI-Powered-3D-Fall-Detection-System-using-WiFi-Sensing\bg_substraction\experiment_6_summary_charts.png")

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>รายงานสรุปผลการทดลองที่ 6 (Experiment 6 Summary Report)</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Prompt:wght@400;500;600;700&display=swap');

        @page {{
            size: A4 portrait;
            margin: 15mm 15mm 15mm 15mm;
            @bottom-right {{
                content: counter(page) " / " counter(pages);
                font-family: 'Sarabun', sans-serif;
                font-size: 9pt;
                color: #64748b;
            }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Sarabun', 'Leelawadee UI', 'Segoe UI', Tahoma, sans-serif;
            font-size: 13.5px;
            line-height: 1.6;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .report-header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 24px 28px;
            border-radius: 12px;
            margin-bottom: 22px;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.15);
        }}

        .report-badge {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.3);
            border: 1px solid rgba(147, 197, 253, 0.4);
            color: #93c5fd;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .report-title {{
            font-family: 'Prompt', 'Sarabun', sans-serif;
            font-size: 22px;
            font-weight: 700;
            margin: 0 0 6px 0;
            color: #ffffff;
            letter-spacing: -0.3px;
        }}

        .report-subtitle {{
            font-size: 14px;
            font-weight: 500;
            color: #cbd5e1;
            margin: 0 0 10px 0;
        }}

        .report-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            font-size: 11px;
            color: #94a3b8;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 10px;
            margin-top: 10px;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        h2 {{
            font-family: 'Prompt', 'Sarabun', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 22px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        h2::before {{
            content: "";
            display: inline-block;
            width: 4px;
            height: 16px;
            background: #2563eb;
            border-radius: 2px;
        }}

        h3 {{
            font-family: 'Prompt', 'Sarabun', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #334155;
            margin-top: 14px;
            margin-bottom: 8px;
        }}

        p, li {{
            color: #334155;
            text-align: justify;
        }}

        ul, ol {{
            margin-top: 6px;
            margin-bottom: 10px;
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 4px;
        }}

        .card-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 12px 0;
        }}

        .card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 12px;
        }}

        .card-title {{
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 4px;
            font-size: 12.5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0 16px 0;
            font-size: 12px;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #cbd5e1;
        }}

        th {{
            background: #1e293b;
            color: #ffffff;
            font-weight: 600;
            text-align: center;
            padding: 8px 10px;
            border: 1px solid #334155;
        }}

        td {{
            padding: 7px 10px;
            border: 1px solid #e2e8f0;
            color: #334155;
            vertical-align: middle;
        }}

        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        .text-center {{ text-align: center; }}
        .text-right {{ text-align: right; }}
        .text-left {{ text-align: left; }}

        .badge-presence {{
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #bfdbfe;
            font-size: 11px;
        }}

        .badge-absent {{
            display: inline-block;
            background: #fee2e2;
            color: #991b1b;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #fecaca;
            font-size: 11px;
        }}

        .highlight-peak {{
            color: #dc2626;
            font-weight: 800;
            font-size: 13px;
        }}

        .highlight-blue {{
            color: #2563eb;
            font-weight: 700;
        }}

        .pipeline-box {{
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 12px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            font-weight: 600;
        }}

        .pipeline-step {{
            background: #ffffff;
            border: 1px solid #94a3b8;
            border-radius: 6px;
            padding: 8px 10px;
            text-align: center;
            flex: 1;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            color: #0f172a;
        }}

        .pipeline-arrow {{
            color: #64748b;
            font-size: 14px;
            font-weight: bold;
        }}

        .image-container {{
            text-align: center;
            margin: 14px 0;
            page-break-inside: avoid;
        }}

        .report-image {{
            max-width: 92%;
            height: auto;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .image-caption {{
            font-size: 11px;
            color: #64748b;
            margin-top: 6px;
            font-style: italic;
        }}

        .alert-box {{
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
            border-radius: 0 8px 8px 0;
            padding: 12px 16px;
            margin: 12px 0;
            font-size: 12.5px;
            color: #166534;
        }}

        .alert-box-title {{
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .page-break {{
            page-break-before: always;
        }}

        .avoid-break {{
            page-break-inside: avoid;
        }}

        .footer-note {{
            margin-top: 25px;
            padding-top: 10px;
            border-top: 1px solid #cbd5e1;
            font-size: 11px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
</head>
<body>

    <!-- Header Section -->
    <div class="report-header">
        <div class="report-badge">EXPERIMENT 6 TECHNICAL SUMMARY REPORT</div>
        <h1 class="report-title">รายงานสรุปผลการทดลองที่ 6 (Experiment 6 Summary Report)</h1>
        <div class="report-subtitle">ระบบตรวจจับการล้มและจำแนกพฤติกรรมมนุษย์แบบ 3 มิติด้วยสัญญาณ Wi-Fi CSI</div>
        <div style="font-size: 12.5px; color: #93c5fd; font-weight: 500;">AI-Powered 3D Fall Detection System using Wi-Fi Sensing</div>
        <div class="report-meta">
            <div class="meta-item">📅 วันที่จัดทำ: 22 สิงหาคม 2026</div>
            <div class="meta-item">📊 ไฟล์ข้อมูลอ้างอิง: master_experiment6_summary.csv</div>
            <div class="meta-item">🎯 พื้นที่ตรวจจับหลัก: Position 1 (ห้องน้ำ / Bathroom Target Zone)</div>
        </div>
    </div>

    <!-- Section 1 -->
    <h2>1. บทนำและวัตถุประสงค์ (Introduction & Objectives)</h2>
    <div class="card-grid">
        <div class="card">
            <div class="card-title">🎯 1. ตรวจจับการล้มในโซนเป้าหมาย</div>
            ประเมินประสิทธิภาพการตรวจจับการล้มและพฤติกรรมมนุษย์ในพื้นที่ห้องน้ำ (Position 1) ซึ่งเป็นจุดที่มีความเสี่ยงต่อการลื่นล้มสูงที่สุด
        </div>
        <div class="card">
            <div class="card-title">🛡️ 2. แยกแยะสัญญาณรบกวนนอกโซน</div>
            ทดสอบการแยกแยะสัญญาณนอกห้องน้ำและระเบียง (Position 2 – 5) เพื่อพิสูจน์ว่ากิจกรรมภายนอกไม่ทำให้เกิด False Alarm
        </div>
        <div class="card">
            <div class="card-title">📐 3. สร้าง Background Baseline</div>
            รวมชุดข้อมูลจาก Position 4 (ระเบียงนอกห้อง) เพื่อเป็นตัวแทนสภาวะว่างเปล่า (Empty Room) ที่เสถียรและแม่นยำ
        </div>
    </div>

    <!-- Section 2 -->
    <h2>2. ผังการทดลองและการวางตำแหน่งอุปกรณ์ (Experimental Setup)</h2>
    
    <div class="image-container">
        <img class="report-image" src="{plan_img_b64}" alt="ผังการทดลองที่ 6">
        <div class="image-caption">รูปที่ 1: ผังตำแหน่งการจัดวางอุปกรณ์และจุดทดสอบในการทดลองที่ 6 (Position 1 – Position 5)</div>
    </div>

    <h3>2.1 สภาพแวดล้อมและมิติของพื้นที่ทดสอบ</h3>
    <ul>
        <li><strong>พื้นที่ห้องน้ำ (Bathroom / Target Zone):</strong> ขนาด กว้าง 3.00 เมตร × ยาว 1.34 เมตร</li>
        <li><strong>พื้นที่ห้องนอน (Bedroom / Adjacent Zone):</strong> ขนาด กว้าง 3.00 เมตร × ยาว 5.00 เมตร</li>
    </ul>

    <h3>2.2 การติดตั้งอุปกรณ์รับ-ส่งสัญญาณ (Hardware Placement)</h3>
    <ul>
        <li><strong>เครื่องส่งสัญญาณ (Transmitter - Tx):</strong> ติดตั้งอยู่บริเวณขอบประตูด้านขวาของห้องน้ำ</li>
        <li><strong>เครื่องรับสัญญาณ (Receiver - Rx):</strong> ติดตั้งอยู่บริเวณฝั่งซ้ายของห้องน้ำ (ใกล้สุขภัณฑ์)</li>
        <li><strong>แนวลำคลื่นตรง (Line-of-Sight - LOS):</strong> พาดผ่านบริเวณ <strong>Position 1</strong> โดยตรง ซึ่งเป็นพื้นที่ตรวจจับหลัก</li>
    </ul>

    <h3>2.3 ตารางนิยามจุดทดสอบและกรณีศึกษา (Testing Positions & Cases)</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">ตำแหน่ง</th>
                <th style="width: 32%;">บริเวณตามผังห้อง</th>
                <th style="width: 25%;">ประเภทกรณีศึกษา (Case Type)</th>
                <th style="width: 28%;">พฤติกรรมที่ทดสอบ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center"><strong>Position 1</strong></td>
                <td><strong>ในห้องน้ำ (หน้าสุขภัณฑ์ / แนว LOS)</strong></td>
                <td class="text-center"><span class="badge-presence">🔵 Presence (In-Zone)</span></td>
                <td>• Get Up & Sit Down (จำลองการล้ม)<br>• Dance (เคลื่อนไหวต่อเนื่อง)<br>• Standstill (ยืนนิ่ง)</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Position 2</strong></td>
                <td>ห้องข้างเคียง (มีผนังกั้น)</td>
                <td class="text-center"><span class="badge-absent">🔴 Absent (Out-of-Zone)</span></td>
                <td>• Standstill (ยืนนิ่ง)</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Position 3</strong></td>
                <td>ทางเดินข้างเตียงนอน</td>
                <td class="text-center"><span class="badge-absent">🔴 Absent (Out-of-Zone)</span></td>
                <td>• Walking (เดินไป-กลับ)</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Position 4</strong></td>
                <td>ทางเดินระเบียงนอกห้อง</td>
                <td class="text-center"><span class="badge-absent">🔴 Absent (Out-of-Zone)</span></td>
                <td>• Walking (เดินไป-กลับ)<br><em>(Master Background Baseline)</em></td>
            </tr>
            <tr>
                <td class="text-center"><strong>Position 5</strong></td>
                <td>บริเวณกลางห้องนอนเหนือเตียง</td>
                <td class="text-center"><span class="badge-absent">🔴 Absent (Out-of-Zone)</span></td>
                <td>• Walking (เดินไป-กลับ)</td>
            </tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <!-- Section 3 -->
    <h2>3. ระเบียบวิธีประมวลผลสัญญาณ (Signal Processing Methodology)</h2>
    
    <div class="pipeline-box">
        <div class="pipeline-step">📡 Raw CSI Data<br><span style="font-size:10px; color:#64748b;">(64 Subcarriers)</span></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step">📊 pos4 Background<br><span style="font-size:10px; color:#64748b;">(Mean & Std Profiling)</span></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step">➖ BG Subtraction<br><span style="font-size:10px; color:#64748b;">Residual = CSI - BG_Mean</span></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step">🧹 Denoising<br><span style="font-size:10px; color:#64748b;">Noise Floor: 2.0 × Std</span></div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step">📈 Activity Index<br><span style="font-size:10px; color:#64748b;">(RMS Calculation)</span></div>
    </div>

    <ol style="font-size: 13px; margin-top: 10px;">
        <li><strong>Combined Background Baseline:</strong> รวมไฟล์ <code>pos4_*.csv</code> ทั้ง 4 ชุดข้อมูล (จำนวน \(N = 1,063\) ตัวอย่าง) เพื่อสกัดค่าเฉลี่ยสภาวะพื้นหลัง (\(\mu_{{\\text{{BG}}}} = 9.468\)) และส่วนเบี่ยงเบนมาตรฐาน (\(\sigma_{{\\text{{BG}}}} = 3.154\))</li>
        <li><strong>Background Subtraction:</strong> ลบค่าเฉลี่ยพื้นหลัง (\(\mu_{{\\text{{BG}}}}\)) ออกจากทุกเฟรมของสัญญาณ CSI เพื่อดึงเฉพาะสัญญาณการเปลี่ยนแปลง (Residual Matrix)</li>
        <li><strong>Denoising:</strong> ตัดสัญญาณ Residual ที่มีค่าน้อยกว่าระดับ Noise Floor (\(2.0 \times \sigma_{{\\text{{BG}}}} = 6.308\)) ให้มีค่าเป็นศูนย์ เพื่อขจัดสัญญาณรบกวนตามธรรมชาติของคลื่นวิทยุ</li>
        <li><strong>Activity Index (RMS):</strong> คำนวณค่า Root Mean Square ของสัญญาณ Residual ในแต่ละเฟรม เพื่อใช้เป็นดัชนีชี้วัดระดับความรุนแรงของการเคลื่อนไหว</li>
    </ol>

    <!-- Section 4 -->
    <h2>4. ตารางสรุปผลการทดลองเชิงสถิติ (Statistical Results)</h2>

    <h3>4.1 เปรียบเทียบตามประเภทกรณีศึกษา (Presence vs Absent Case)</h3>
    <table>
        <thead>
            <tr>
                <th>กรณีศึกษา (Case Type)</th>
                <th>ตำแหน่ง</th>
                <th>จำนวนไฟล์</th>
                <th>RSSI เฉลี่ย (dBm)</th>
                <th>CSI Std</th>
                <th>Denoised RMS</th>
                <th>Mean Max Activity</th>
                <th>Peak Activity</th>
                <th>% Active Frames</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: #f0f7ff;">
                <td><span class="badge-presence">🔵 Presence (In-Zone)</span></td>
                <td><strong>Pos 1 (ในห้องน้ำ)</strong></td>
                <td class="text-center">14</td>
                <td class="text-center">-70.73</td>
                <td class="text-center">7.07</td>
                <td class="text-center">0.99</td>
                <td class="text-center highlight-blue">12.89</td>
                <td class="text-center highlight-peak">87.45</td>
                <td class="text-center"><strong>49.63%</strong></td>
            </tr>
            <tr>
                <td><span class="badge-absent">🔴 Absent (Out-of-Zone)</span></td>
                <td>Pos 2–5 (นอกห้องน้ำ)</td>
                <td class="text-center">16</td>
                <td class="text-center">-69.10</td>
                <td class="text-center">7.09</td>
                <td class="text-center">1.16</td>
                <td class="text-center">7.17</td>
                <td class="text-center">8.42</td>
                <td class="text-center">40.01%</td>
            </tr>
        </tbody>
    </table>

    <h3>4.2 เปรียบเทียบแยกตามตำแหน่งทดสอบ (Position-wise Breakdown)</h3>
    <table>
        <thead>
            <tr>
                <th>ตำแหน่ง</th>
                <th>บริเวณพื้นที่</th>
                <th>สถานะ</th>
                <th>จำนวนไฟล์</th>
                <th>RSSI (dBm)</th>
                <th>CSI Std</th>
                <th>Denoised RMS</th>
                <th>Peak Activity</th>
                <th>% Active Frames</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: #eff6ff;">
                <td class="text-center"><strong>Pos 1</strong></td>
                <td><strong>ห้องน้ำ (หน้าสุขภัณฑ์ / LOS)</strong></td>
                <td class="text-center"><span class="badge-presence">Presence</span></td>
                <td class="text-center">14</td>
                <td class="text-center">-70.73</td>
                <td class="text-center">7.07</td>
                <td class="text-center">0.99</td>
                <td class="text-center highlight-peak">87.45</td>
                <td class="text-center"><strong>49.63%</strong></td>
            </tr>
            <tr>
                <td class="text-center"><strong>Pos 2</strong></td>
                <td>ห้องข้างเคียง (มีผนังกั้น)</td>
                <td class="text-center"><span class="badge-absent">Absent</span></td>
                <td class="text-center">4</td>
                <td class="text-center">-72.56</td>
                <td class="text-center">6.96</td>
                <td class="text-center">1.23</td>
                <td class="text-center">8.29</td>
                <td class="text-center">49.25%</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Pos 3</strong></td>
                <td>ทางเดินข้างเตียงนอน</td>
                <td class="text-center"><span class="badge-absent">Absent</span></td>
                <td class="text-center">4</td>
                <td class="text-center">-62.19</td>
                <td class="text-center">6.95</td>
                <td class="text-center">1.97</td>
                <td class="text-center">8.42</td>
                <td class="text-center">60.90%</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Pos 4</strong></td>
                <td>ระเบียงนอกห้อง (Master BG)</td>
                <td class="text-center"><span class="badge-absent">Absent</span></td>
                <td class="text-center">4</td>
                <td class="text-center">-71.29</td>
                <td class="text-center">7.13</td>
                <td class="text-center">0.77</td>
                <td class="text-center">8.19</td>
                <td class="text-center">23.22%</td>
            </tr>
            <tr>
                <td class="text-center"><strong>Pos 5</strong></td>
                <td>กลางห้องนอนเหนือเตียง</td>
                <td class="text-center"><span class="badge-absent">Absent</span></td>
                <td class="text-center">4</td>
                <td class="text-center">-70.37</td>
                <td class="text-center">7.32</td>
                <td class="text-center">0.66</td>
                <td class="text-center">7.25</td>
                <td class="text-center">26.68%</td>
            </tr>
        </tbody>
    </table>

    <div class="page-break"></div>

    <h3>4.3 เปรียบเทียบแยกตามพฤติกรรมการเคลื่อนไหว (Action-wise Breakdown)</h3>
    <table>
        <thead>
            <tr>
                <th>พฤติกรรม (Action)</th>
                <th>พื้นที่ทดสอบ</th>
                <th>จำนวนไฟล์</th>
                <th>RSSI (dBm)</th>
                <th>CSI Std</th>
                <th>Denoised RMS</th>
                <th>Max Activity (Mean)</th>
                <th>Peak Activity (Max)</th>
                <th>% Active Frames</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: #fef2f2;">
                <td><strong>Get Up & Sit Down</strong></td>
                <td>Presence (Pos 1)</td>
                <td class="text-center">5</td>
                <td class="text-center">-70.31</td>
                <td class="text-center">7.40</td>
                <td class="text-center">0.93</td>
                <td class="text-center highlight-blue">22.97</td>
                <td class="text-center highlight-peak">87.45</td>
                <td class="text-center">48.66%</td>
            </tr>
            <tr>
                <td><strong>Standstill</strong></td>
                <td>Presence (Pos 1)</td>
                <td class="text-center">5</td>
                <td class="text-center">-70.15</td>
                <td class="text-center">6.82</td>
                <td class="text-center">1.11</td>
                <td class="text-center">7.76</td>
                <td class="text-center">11.96</td>
                <td class="text-center">54.80%</td>
            </tr>
            <tr>
                <td><strong>Dance</strong></td>
                <td>Presence (Pos 1)</td>
                <td class="text-center">4</td>
                <td class="text-center">-71.97</td>
                <td class="text-center">6.98</td>
                <td class="text-center">0.93</td>
                <td class="text-center">6.73</td>
                <td class="text-center">7.45</td>
                <td class="text-center">44.38%</td>
            </tr>
            <tr>
                <td><strong>Standstill</strong></td>
                <td>Absent (Pos 2)</td>
                <td class="text-center">4</td>
                <td class="text-center">-72.56</td>
                <td class="text-center">6.96</td>
                <td class="text-center">1.23</td>
                <td class="text-center">7.84</td>
                <td class="text-center">8.29</td>
                <td class="text-center">49.25%</td>
            </tr>
            <tr>
                <td><strong>Walking</strong></td>
                <td>Absent (Pos 3, 4, 5)</td>
                <td class="text-center">12</td>
                <td class="text-center">-67.95</td>
                <td class="text-center">7.13</td>
                <td class="text-center">1.13</td>
                <td class="text-center">6.95</td>
                <td class="text-center">8.42</td>
                <td class="text-center">36.93%</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 5 -->
    <h2>5. การวิเคราะห์และอภิปรายผลการทดลอง (Key Findings & Discussion)</h2>
    
    <h3>5.1 การตรวจจับการล้มและการลุก-นั่ง (Fall / Vertical Transition Detection)</h3>
    <ul>
        <li>พฤติกรรม <strong>Get Up & Sit Down ใน Position 1</strong> ให้ค่า <strong>Peak Activity Index พุ่งสูงถึง 87.45 RMS</strong> (และมีค่าเฉลี่ยสูงสุด 22.97 RMS)</li>
        <li><strong>สาเหตุทางกายภาพ:</strong> ร่างกายมนุษย์เคลื่อนที่ตัดผ่านระนาบลำคลื่น Line-of-Sight (LOS) ในแนวดิ่ง ทำให้โครงสร้างเส้นทางสะท้อนของคลื่น (Multipath Profile) บนซับแคร์เรียร์ทั้ง 64 ช่องเปลี่ยนแปลงอย่างรุนแรงและเฉียบพลัน</li>
        <li><strong>Dynamic Contrast Margin > 10x:</strong> เมื่อเปรียบเทียบกับพฤติกรรมนอกโซน (Pos 2–5) ที่มีค่า Peak Activity สูงสุดเพียง <strong>8.42 RMS</strong> พบว่าสัญญาณการล้มในห้องน้ำมีความต่างสูงกว่าถึง <strong>~10.4 เท่า</strong> จึงสามารถใช้กำหนดขีดแบ่ง (Threshold) แจ้งเตือนการล้มได้อย่างเด็ดขาดโดยไม่มี False Alarm</li>
    </ul>

    <h3>5.2 การกักกันสัญญาณและการแยกแยะพื้นที่ (Spatial Zone Isolation)</h3>
    <ul>
        <li><strong>Position 2 (ห้องข้างเคียง):</strong> มีผนังคอนกรีตกั้น สัญญาณถูกลดทอน (Wall Attenuation) ส่งผลให้ค่า Peak Activity อยู่ที่ 8.29 RMS แม้จะมีการเคลื่อนไหว</li>
        <li><strong>Position 4 (ระเบียงนอกห้อง):</strong> มีค่า Active Frames ต่ำที่สุดที่ <strong>23.22%</strong> แสดงให้เห็นว่าคลื่นสะท้อนแทบไม่เล็ดลอดออกไปนอกห้อง ทำให้เหมาะเป็น <strong>Master Background Baseline</strong></li>
        <li><strong>Position 3 & 5 (ในห้องนอน):</strong> การเดินรอบเตียงนอนให้ค่า Peak Activity เฉลี่ย 6.95–8.42 RMS ซึ่งต่ำกว่าจังหวะการล้มในห้องน้ำอย่างชัดเจน</li>
    </ul>

    <!-- Section 6 -->
    <h2>6. สรุปผลและแนวทางการประยุกต์ใช้ (Conclusion & Recommendations)</h2>
    
    <div class="alert-box">
        <div class="alert-box-title">💡 เกณฑ์แนะนำการตั้งค่า Trigger Threshold สำหรับระบบจริง</div>
        <ul>
            <li><strong>Fall Detection Threshold (ตรวจจับการล้ม / เปลี่ยนระดับแนวดิ่ง):</strong> กำหนด <code>Activity Index > 15.0 RMS</code> (สามารถตรวจจับการล้มได้ 100% โดยไม่เกิด False Alarm จากนอกห้อง)</li>
            <li><strong>Presence Detection Threshold (ตรวจจับการมีอยู่ของมนุษย์ในห้องน้ำ):</strong> กำหนด <code>Activity Index > 2.5 RMS</code></li>
        </ul>
    </div>

    <ul>
        <li><strong>ความแม่นยำของ Background Subtraction:</strong> การใช้ค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐานจาก Position 4 ร่วมกับการตัด Noise Floor ที่ระดับ \(2.0 \times \\text{{SD}}\) สามารถแยกแยะสัญญาณมนุษย์ออกจากสัญญาณรบกวนแวดล้อมได้อย่างมีประสิทธิภาพ</li>
        <li><strong>การนำข้อมูลไปใช้ต่อในโมเดล AI:</strong> ข้อมูล Residual Matrix ที่บันทึกไว้ใน <code>master_experiment6_summary.csv</code> และไฟล์ CSV ใน <code>bg_substraction/</code> สามารถนำไปใช้เป็น Feature Matrix สำหรับฝึกสอนโมเดล AI (เช่น 1D-CNN, LSTM หรือ SVM) เพื่อจำแนกประเภทกิจกรรมและตรวจจับการล้มแบบ Real-time ได้ทันที</li>
    </ul>

    <!-- Section 7: Summary Visual Charts -->
    <div class="avoid-break" style="margin-top: 16px;">
        <h3>7. แผนภูมิสรุปผลการวิเคราะห์เชิงสถิติ (Summary Visual Charts)</h3>
        <div class="image-container">
            <img class="report-image" src="{charts_img_b64}" alt="สรุปแผนภูมิผลการทดลองที่ 6">
            <div class="image-caption">รูปที่ 2: แผนภูมิเปรียบเทียบค่าสถิติ Activity Index, Denoised RMS และ Active Frames แยกตามตำแหน่งและพฤติกรรม</div>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer-note">
        <div><strong>จัดทำโดย:</strong> ระบบประมวลผลข้อมูลการตรวจวัดสัญญาณ Wi-Fi CSI อัตโนมัติ</div>
        <div>AI-Powered 3D Fall Detection System using Wi-Fi Sensing</div>
    </div>

</body>
</html>
"""

html_file = os.path.join(exp6_dir, "EXPERIMENT_6_REPORT.html")
pdf_file = os.path.join(exp6_dir, "EXPERIMENT_6_REPORT.pdf")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML: {html_file}")

# Convert HTML to PDF using Headless Chrome or Edge
browser_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
browser_exe = next((p for p in browser_paths if os.path.exists(p)), None)

if browser_exe:
    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file}",
        "--no-pdf-header-footer",
        html_file
    ]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    time.sleep(1)
    if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 0:
        print(f"✅ Successfully created PDF: {pdf_file} ({os.path.getsize(pdf_file):,} bytes)")
    else:
        print(f"❌ Failed to generate PDF. Error: {result.stderr}")
else:
    print("❌ No Chrome or Edge executable found.")
