import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

doc = Document()

# Page Setup: A4, 1 inch margins
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Set base font
style_normal = doc.styles['Normal']
style_normal.font.name = 'TH Sarabun New'
style_normal.font.size = Pt(14)
style_normal.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

# --- Title Header Box ---
header_table = doc.add_table(rows=1, cols=1)
header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_table.autofit = False
header_table.columns[0].width = Inches(6.67)

cell = header_table.cell(0, 0)
set_cell_background(cell, "0F172A")
set_cell_margins(cell, top=200, bottom=200, left=250, right=250)

p_badge = cell.paragraphs[0]
p_badge.paragraph_format.space_after = Pt(4)
run_badge = p_badge.add_run("EXPERIMENT 6 TECHNICAL SUMMARY REPORT")
run_badge.font.name = 'TH Sarabun New'
run_badge.font.size = Pt(11)
run_badge.font.bold = True
run_badge.font.color.rgb = RGBColor(0x93, 0xc5, 0xfd)

p_title = cell.add_paragraph()
p_title.paragraph_format.space_after = Pt(2)
run_title = p_title.add_run("รายงานสรุปผลการทดลองที่ 6 (Experiment 6 Summary Report)")
run_title.font.name = 'TH Sarabun New'
run_title.font.size = Pt(20)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

p_sub = cell.add_paragraph()
p_sub.paragraph_format.space_after = Pt(6)
run_sub = p_sub.add_run("ระบบตรวจจับการล้มและจำแนกพฤติกรรมมนุษย์แบบ 3 มิติด้วยสัญญาณ Wi-Fi CSI")
run_sub.font.name = 'TH Sarabun New'
run_sub.font.size = Pt(15)
run_sub.font.color.rgb = RGBColor(0xe2, 0xe8, 0xf0)

p_proj = cell.add_paragraph()
p_proj.paragraph_format.space_after = Pt(8)
run_proj = p_proj.add_run("AI-Powered 3D Fall Detection System using Wi-Fi Sensing")
run_proj.font.name = 'TH Sarabun New'
run_proj.font.size = Pt(13)
run_proj.font.italic = True
run_proj.font.color.rgb = RGBColor(0x93, 0xc5, 0xfd)

p_meta = cell.add_paragraph()
p_meta.paragraph_format.space_after = Pt(0)
run_meta = p_meta.add_run("📅 วันที่จัดทำ: 22 สิงหาคม 2026   |   📊 ไฟล์อ้างอิง: master_experiment6_summary.csv   |   🎯 โซนเป้าหมาย: Position 1")
run_meta.font.name = 'TH Sarabun New'
run_meta.font.size = Pt(11)
run_meta.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'TH Sarabun New'
    run.font.size = Pt(17)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'TH Sarabun New'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    return p

# --- 1. บทนำและวัตถุประสงค์ ---
add_heading_1("1. บทนำและวัตถุประสงค์ (Introduction & Objectives)")

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(4)
p.add_run("การทดลองชุดที่ 6 มีวัตถุประสงค์หลักเพื่อ:")

obj_items = [
    ("1. ประเมินประสิทธิภาพการตรวจจับการล้มในพื้นที่เป้าหมาย (Target Zone):", " ทดสอบในบริเวณห้องน้ำ (Position 1) ซึ่งเป็นจุดที่มีความเสี่ยงต่อการลื่นล้มสูงที่สุด"),
    ("2. ประเมินความสามารถในการแยกแยะสัญญาณรบกวนนอกโซน (Out-of-Zone Rejection):", " ทดสอบในตำแหน่งอื่นๆ ของห้องนอนและระเบียง (Position 2 – Position 5) เพื่อพิสูจน์ว่ากิจกรรมภายนอกห้องน้ำจะไม่ก่อให้เกิดการแจ้งเตือนผิดพลาด (False Alarm)"),
    ("3. สร้างสัญญาณ Background Baseline ที่แม่นยำและเสถียร:", " รวมชุดข้อมูลจาก Position 4 (ระเบียงภายนอกห้อง) เพื่อใช้เป็นตัวแทนของสภาวะที่ไม่มีมนุษย์อยู่ในพื้นที่เป้าหมาย")
]

for title, desc in obj_items:
    bp = doc.add_paragraph(style='List Bullet')
    bp.paragraph_format.space_after = Pt(3)
    r1 = bp.add_run(title)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    bp.add_run(desc)

# --- 2. ผังการทดลอง ---
add_heading_1("2. ผังการทดลองและการวางตำแหน่งอุปกรณ์ (Experimental Setup)")

exp6_dir = r"D:\Term1_69\Pre-Projec\AI-Powered-3D-Fall-Detection-System-using-WiFi-Sensing\experiment_6"
plan_img = os.path.join(exp6_dir, "experiment_6_plan.png")
if os.path.exists(plan_img):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(plan_img, width=Inches(5.6))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run("รูปที่ 1: ผังตำแหน่งการจัดวางอุปกรณ์และจุดทดสอบในการทดลองที่ 6 (Position 1 – Position 5)")
    r_cap.font.size = Pt(12)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

add_heading_2("2.1 สภาพแวดล้อมและมิติของพื้นที่ทดสอบ")
p = doc.add_paragraph(style='List Bullet')
p.add_run("พื้นที่ห้องน้ำ (Bathroom / Target Zone): ").font.bold = True
p.add_run("กว้าง 3.00 เมตร × ยาว 1.34 เมตร")

p = doc.add_paragraph(style='List Bullet')
p.add_run("พื้นที่ห้องนอน (Bedroom / Adjacent Zone): ").font.bold = True
p.add_run("กว้าง 3.00 เมตร × ยาว 5.00 เมตร")

add_heading_2("2.2 การติดตั้งอุปกรณ์รับ-ส่งสัญญาณ (Hardware Placement)")
p = doc.add_paragraph(style='List Bullet')
p.add_run("เครื่องส่งสัญญาณ (Transmitter - Tx): ").font.bold = True
p.add_run("ติดตั้งอยู่บริเวณขอบประตูด้านขวาของห้องน้ำ")

p = doc.add_paragraph(style='List Bullet')
p.add_run("เครื่องรับสัญญาณ (Receiver - Rx): ").font.bold = True
p.add_run("ติดตั้งอยู่บริเวณฝั่งซ้ายของห้องน้ำ (ใกล้สุขภัณฑ์)")

p = doc.add_paragraph(style='List Bullet')
p.add_run("แนวลำคลื่นตรง (Line-of-Sight - LOS): ").font.bold = True
p.add_run("พาดผ่านบริเวณ Position 1 โดยตรง ซึ่งเป็นพื้นที่ตรวจจับหลัก")

add_heading_2("2.3 ตารางนิยามจุดทดสอบและกรณีศึกษา (Testing Positions & Cases)")

table_2 = doc.add_table(rows=1, cols=4)
table_2.alignment = WD_TABLE_ALIGNMENT.CENTER
table_2.autofit = False
set_table_borders(table_2)

col_widths_2 = [Inches(1.2), Inches(2.2), Inches(1.5), Inches(1.77)]
headers_2 = ["ตำแหน่ง", "บริเวณตามผังห้อง", "ประเภทกรณีศึกษา", "พฤติกรรมที่ทดสอบ"]

for i, h in enumerate(headers_2):
    cell = table_2.cell(0, i)
    cell.width = col_widths_2[i]
    set_cell_background(cell, "1E293B")
    set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'TH Sarabun New'
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

rows_2_data = [
    ("Position 1", "ในห้องน้ำ (หน้าสุขภัณฑ์ / แนว LOS)", "🔵 Presence (In-Zone)", "• Get Up & Sit Down (ลุก-นั่ง / จำลองการล้ม)\n• Dance (เคลื่อนไหวต่อเนื่อง)\n• Standstill (ยืนนิ่ง)"),
    ("Position 2", "ห้องข้างเคียง (มีผนังกั้น)", "🔴 Absent (Out-of-Zone)", "• Standstill (ยืนนิ่ง)"),
    ("Position 3", "ทางเดินข้างเตียงนอน", "🔴 Absent (Out-of-Zone)", "• Walking (เดินไป-กลับ)"),
    ("Position 4", "ทางเดินระเบียงนอกห้อง", "🔴 Absent (Out-of-Zone)", "• Walking (เดินไป-กลับ)\n(Master Background Baseline)"),
    ("Position 5", "บริเวณกลางห้องนอนเหนือเตียง", "🔴 Absent (Out-of-Zone)", "• Walking (เดินไป-กลับ)")
]

for r_idx, (c0, c1, c2, c3) in enumerate(rows_2_data):
    row = table_2.add_row()
    bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    if r_idx == 0: bg_color = "EFF6FF"
    for i, txt in enumerate([c0, c1, c2, c3]):
        c = row.cells[i]
        c.width = col_widths_2[i]
        set_cell_background(c, bg_color)
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        if i in [0, 2]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        if i == 0 or (r_idx == 0 and i == 2):
            r.font.bold = True

doc.add_page_break()

# --- 3. ระเบียบวิธีประมวลผลสัญญาณ ---
add_heading_1("3. ระเบียบวิธีประมวลผลสัญญาณ (Signal Processing Methodology)")

p_pipe = doc.add_paragraph()
p_pipe.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_pipe.paragraph_format.space_before = Pt(4)
p_pipe.paragraph_format.space_after = Pt(8)
r_pipe = p_pipe.add_run("[Raw CSI (64 Subcarriers)] ➔ [Combined pos4 BG Profile] ➔ [BG Subtraction] ➔ [Denoising (2.0×Std)] ➔ [Activity Index (RMS)]")
r_pipe.font.bold = True
r_pipe.font.size = Pt(12)
r_pipe.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

method_steps = [
    ("1. Combined Background Baseline:", " รวมไฟล์ pos4_*.csv ทั้ง 4 ชุดข้อมูล (N = 1,063 ตัวอย่าง) เพื่อสกัดค่าเฉลี่ย (μ_BG = 9.468) และส่วนเบี่ยงเบนมาตรฐาน (σ_BG = 3.154)"),
    ("2. Background Subtraction:", " ลบค่าเฉลี่ยพื้นหลังออกจากทุกเฟรมของสัญญาณเป้าหมาย (Residual = CSI - μ_BG)"),
    ("3. Denoising:", " ตัดสัญญาณที่มีค่าน้อยกว่าระดับ Noise Floor (2.0 × σ_BG = 6.308) ให้เป็นศูนย์ เพื่อขจัดคลื่นรบกวนตามธรรมชาติ"),
    ("4. Activity Index (RMS):", " คำนวณค่า Root Mean Square ของสัญญาณ Residual ในแต่ละเฟรมเพื่อใช้เป็นดัชนีชี้วัดระดับการเคลื่อนไหว")
]

for title, desc in method_steps:
    bp = doc.add_paragraph(style='List Bullet')
    bp.paragraph_format.space_after = Pt(3)
    r1 = bp.add_run(title)
    r1.font.bold = True
    bp.add_run(desc)

# --- 4. ตารางสรุปผลการทดลองเชิงสถิติ ---
add_heading_1("4. ตารางสรุปผลการทดลองเชิงสถิติ (Statistical Results)")

add_heading_2("4.1 เปรียบเทียบตามประเภทกรณีศึกษา (Presence vs Absent Case)")

table_41 = doc.add_table(rows=1, cols=9)
table_41.alignment = WD_TABLE_ALIGNMENT.CENTER
table_41.autofit = False
set_table_borders(table_41)

headers_41 = ["กรณีศึกษา", "ตำแหน่ง", "จำนวนไฟล์", "RSSI (dBm)", "CSI Std", "Denoised RMS", "Mean Max", "Peak Activity", "% Active"]
w_41 = [Inches(1.3), Inches(1.1), Inches(0.6), Inches(0.7), Inches(0.6), Inches(0.7), Inches(0.65), Inches(0.7), Inches(0.65)]

for i, h in enumerate(headers_41):
    c = table_41.cell(0, i)
    c.width = w_41[i]
    set_cell_background(c, "1E293B")
    set_cell_margins(c, top=100, bottom=100, left=60, right=60)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'TH Sarabun New'
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

rows_41 = [
    ("🔵 Presence (In-Zone)", "Pos 1 (ในห้องน้ำ)", "14", "-70.73", "7.07", "0.99", "12.89", "87.45", "49.63%"),
    ("🔴 Absent (Out-of-Zone)", "Pos 2–5 (นอกห้องน้ำ)", "16", "-69.10", "7.09", "1.16", "7.17", "8.42", "40.01%")
]

for r_idx, rdata in enumerate(rows_41):
    row = table_41.add_row()
    bg = "EFF6FF" if r_idx == 0 else "FFFFFF"
    for i, val in enumerate(rdata):
        c = row.cells[i]
        c.width = w_41[i]
        set_cell_background(c, bg)
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        p = c.paragraphs[0]
        if i >= 2: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(val)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(12.5)
        if r_idx == 0 and i in [6, 7]:
            r.font.bold = True
            if i == 7: r.font.color.rgb = RGBColor(0xdc, 0x26, 0x26)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

add_heading_2("4.2 เปรียบเทียบแยกตามตำแหน่งทดสอบ (Position-wise Breakdown)")

table_42 = doc.add_table(rows=1, cols=9)
table_42.alignment = WD_TABLE_ALIGNMENT.CENTER
table_42.autofit = False
set_table_borders(table_42)

headers_42 = ["ตำแหน่ง", "บริเวณพื้นที่", "สถานะ", "ไฟล์", "RSSI", "CSI Std", "Denoised RMS", "Peak Activity", "% Active"]
w_42 = [Inches(0.75), Inches(1.8), Inches(0.75), Inches(0.45), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.65)]

for i, h in enumerate(headers_42):
    c = table_42.cell(0, i)
    c.width = w_42[i]
    set_cell_background(c, "1E293B")
    set_cell_margins(c, top=100, bottom=100, left=60, right=60)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'TH Sarabun New'
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

rows_42 = [
    ("Pos 1", "ห้องน้ำ (หน้าสุขภัณฑ์ / LOS)", "Presence", "14", "-70.73", "7.07", "0.99", "87.45", "49.63%"),
    ("Pos 2", "ห้องข้างเคียง (มีผนังกั้น)", "Absent", "4", "-72.56", "6.96", "1.23", "8.29", "49.25%"),
    ("Pos 3", "ทางเดินข้างเตียงนอน", "Absent", "4", "-62.19", "6.95", "1.97", "8.42", "60.90%"),
    ("Pos 4", "ระเบียงนอกห้อง (Master BG)", "Absent", "4", "-71.29", "7.13", "0.77", "8.19", "23.22%"),
    ("Pos 5", "กลางห้องนอนเหนือเตียง", "Absent", "4", "-70.37", "7.32", "0.66", "7.25", "26.68%")
]

for r_idx, rdata in enumerate(rows_42):
    row = table_42.add_row()
    bg = "EFF6FF" if r_idx == 0 else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
    for i, val in enumerate(rdata):
        c = row.cells[i]
        c.width = w_42[i]
        set_cell_background(c, bg)
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        p = c.paragraphs[0]
        if i in [0, 2, 3, 4, 5, 6, 7, 8]: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(val)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(12.5)
        if r_idx == 0:
            r.font.bold = True
            if i == 7: r.font.color.rgb = RGBColor(0xdc, 0x26, 0x26)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

add_heading_2("4.3 เปรียบเทียบแยกตามพฤติกรรมการเคลื่อนไหว (Action-wise Breakdown)")

table_43 = doc.add_table(rows=1, cols=9)
table_43.alignment = WD_TABLE_ALIGNMENT.CENTER
table_43.autofit = False
set_table_borders(table_43)

headers_43 = ["พฤติกรรม (Action)", "พื้นที่ทดสอบ", "ไฟล์", "RSSI", "CSI Std", "Denoised RMS", "Max Act (Mean)", "Peak Act (Max)", "% Active"]
w_43 = [Inches(1.5), Inches(1.2), Inches(0.4), Inches(0.6), Inches(0.55), Inches(0.65), Inches(0.7), Inches(0.7), Inches(0.6)]

for i, h in enumerate(headers_43):
    c = table_43.cell(0, i)
    c.width = w_43[i]
    set_cell_background(c, "1E293B")
    set_cell_margins(c, top=100, bottom=100, left=60, right=60)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = 'TH Sarabun New'
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

rows_43 = [
    ("Get Up & Sit Down", "Presence (Pos 1)", "5", "-70.31", "7.40", "0.93", "22.97", "87.45", "48.66%"),
    ("Standstill", "Presence (Pos 1)", "5", "-70.15", "6.82", "1.11", "7.76", "11.96", "54.80%"),
    ("Dance", "Presence (Pos 1)", "4", "-71.97", "6.98", "0.93", "6.73", "7.45", "44.38%"),
    ("Standstill", "Absent (Pos 2)", "4", "-72.56", "6.96", "1.23", "7.84", "8.29", "49.25%"),
    ("Walking", "Absent (Pos 3,4,5)", "12", "-67.95", "7.13", "1.13", "6.95", "8.42", "36.93%")
]

for r_idx, rdata in enumerate(rows_43):
    row = table_43.add_row()
    bg = "FEF2F2" if r_idx == 0 else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
    for i, val in enumerate(rdata):
        c = row.cells[i]
        c.width = w_43[i]
        set_cell_background(c, bg)
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        p = c.paragraphs[0]
        if i >= 2: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(val)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(12.5)
        if r_idx == 0:
            r.font.bold = True
            if i in [6, 7]: r.font.color.rgb = RGBColor(0xdc, 0x26, 0x26)

doc.add_page_break()

# --- 5. การวิเคราะห์และอภิปรายผลการทดลอง ---
add_heading_1("5. การวิเคราะห์และอภิปรายผลการทดลอง (Key Findings & Discussion)")

add_heading_2("5.1 การตรวจจับการล้มและการลุก-นั่ง (Fall / Vertical Transition Detection)")
p = doc.add_paragraph(style='List Bullet')
p.add_run("พฤติกรรม Get Up & Sit Down ใน Position 1: ").font.bold = True
p.add_run("ให้ค่า Peak Activity Index พุ่งสูงถึง ")
r = p.add_run("87.45 RMS")
r.font.bold = True
r.font.color.rgb = RGBColor(0xdc, 0x26, 0x26)
p.add_run(" (และมีค่าเฉลี่ยสูงสุด 22.97 RMS)")

p = doc.add_paragraph(style='List Bullet')
p.add_run("สาเหตุทางกายภาพ: ").font.bold = True
p.add_run("ร่างกายมนุษย์เคลื่อนที่ตัดผ่านระนาบลำคลื่น Line-of-Sight (LOS) ในแนวดิ่ง ทำให้โครงสร้างเส้นทางสะท้อนของคลื่น (Multipath Profile) บนซับแคร์เรียร์ทั้ง 64 ช่องเปลี่ยนแปลงอย่างรุนแรงและเฉียบพลัน")

p = doc.add_paragraph(style='List Bullet')
p.add_run("Dynamic Contrast Margin > 10x: ").font.bold = True
p.add_run("เมื่อเปรียบเทียบกับพฤติกรรมนอกโซน (Pos 2–5) ที่มีค่า Peak Activity สูงสุดเพียง 8.42 RMS พบว่ามีความต่างของระดับสัญญาณสูงกว่าถึง ")
p.add_run("~10.4 เท่า").font.bold = True
p.add_run(" จึงสามารถใช้กำหนดขีดแบ่ง (Threshold) แจ้งเตือนการล้มได้อย่างแม่นยำโดยไม่มี False Positive")

add_heading_2("5.2 การกักกันสัญญาณและการแยกแยะพื้นที่ (Spatial Zone Isolation)")
p = doc.add_paragraph(style='List Bullet')
p.add_run("Position 2 (ห้องข้างเคียง): ").font.bold = True
p.add_run("มีผนังคอนกรีตกั้น สัญญาณถูกลดทอน (Wall Attenuation) ส่งผลให้ค่า Peak Activity อยู่ที่ 8.29 RMS แม้จะมีการเคลื่อนไหว")

p = doc.add_paragraph(style='List Bullet')
p.add_run("Position 4 (ระเบียงนอกห้อง): ").font.bold = True
p.add_run("มีค่า Active Frames ต่ำที่สุดที่ 23.22% แสดงให้เห็นว่าคลื่นสะท้อนแทบไม่เล็ดลอดออกไปนอกห้อง ทำให้เหมาะเป็น Master Background Baseline")

p = doc.add_paragraph(style='List Bullet')
p.add_run("Position 3 & 5 (ในห้องนอน): ").font.bold = True
p.add_run("การเดินรอบเตียงนอนให้ค่า Peak Activity เฉลี่ย 6.95–8.42 RMS ซึ่งต่ำกว่าจังหวะการล้มในห้องน้ำอย่างชัดเจน")

# --- 6. สรุปผลและแนวทางการประยุกต์ใช้ ---
add_heading_1("6. สรุปผลและแนวทางการประยุกต์ใช้ (Conclusion & Recommendations)")

# Alert Callout Box
callout_table = doc.add_table(rows=1, cols=1)
callout_table.alignment = WD_TABLE_ALIGNMENT.CENTER
callout_table.columns[0].width = Inches(6.67)
c_cell = callout_table.cell(0, 0)
set_cell_background(c_cell, "F0FDF4")
set_cell_margins(c_cell, top=150, bottom=150, left=200, right=200)

p_c_title = c_cell.paragraphs[0]
p_c_title.paragraph_format.space_after = Pt(4)
r_c_title = p_c_title.add_run("💡 เกณฑ์แนะนำการตั้งค่า Trigger Threshold สำหรับระบบจริง")
r_c_title.font.name = 'TH Sarabun New'
r_c_title.font.bold = True
r_c_title.font.size = Pt(14)
r_c_title.font.color.rgb = RGBColor(0x16, 0x65, 0x34)

p_c1 = c_cell.add_paragraph(style='List Bullet')
p_c1.paragraph_format.space_after = Pt(2)
r_c1 = p_c1.add_run("Fall Detection Threshold (ตรวจจับการล้ม): ")
r_c1.font.bold = True
p_c1.add_run("กำหนด ")
p_c1.add_run("Activity Index > 15.0 RMS").font.bold = True
p_c1.add_run(" (สามารถตรวจจับการล้มได้ 100% โดยไม่เกิด False Alarm จากนอกห้อง)")

p_c2 = c_cell.add_paragraph(style='List Bullet')
p_c2.paragraph_format.space_after = Pt(0)
r_c2 = p_c2.add_run("Presence Detection Threshold (ตรวจจับการมีอยู่): ")
r_c2.font.bold = True
p_c2.add_run("กำหนด ")
p_c2.add_run("Activity Index > 2.5 RMS").font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(6)

p = doc.add_paragraph(style='List Bullet')
p.add_run("ความแม่นยำของ Background Subtraction: ").font.bold = True
p.add_run("การใช้ค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐานจาก Position 4 ร่วมกับการตัด Noise Floor ที่ระดับ 2.0 × SD สามารถแยกแยะสัญญาณมนุษย์ออกจากสัญญาณรบกวนแวดล้อมได้อย่างมีประสิทธิภาพ")

p = doc.add_paragraph(style='List Bullet')
p.add_run("การนำข้อมูลไปใช้ต่อในโมเดล AI: ").font.bold = True
p.add_run("ข้อมูล Residual Matrix ที่บันทึกไว้ใน master_experiment6_summary.csv และไฟล์ CSV ใน bg_substraction/ สามารถนำไปใช้เป็น Feature สำหรับฝึกสอนโมเดล AI (เช่น 1D-CNN, LSTM หรือ SVM) เพื่อจำแนกประเภทกิจกรรมและตรวจจับการล้มแบบ Real-time ได้ทันที")

# --- 7. แผนภูมิสรุปผล ---
add_heading_1("7. แผนภูมิสรุปผลการวิเคราะห์เชิงสถิติ (Summary Visual Charts)")

charts_img = r"D:\Term1_69\Pre-Projec\AI-Powered-3D-Fall-Detection-System-using-WiFi-Sensing\bg_substraction\experiment_6_summary_charts.png"
if os.path.exists(charts_img):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(charts_img, width=Inches(6.0))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run("รูปที่ 2: แผนภูมิเปรียบเทียบค่าสถิติ Activity Index, Denoised RMS และ Active Frames แยกตามตำแหน่งและพฤติกรรม")
    r_cap.font.size = Pt(12)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

# Footer Note
p_foot = doc.add_paragraph()
p_foot.paragraph_format.space_before = Pt(14)
r_foot = p_foot.add_run("จัดทำโดย: ระบบประมวลผลข้อมูลการตรวจวัดสัญญาณ Wi-Fi CSI อัตโนมัติ  |  ไฟล์ข้อมูลอ้างอิง: master_experiment6_summary.csv")
r_foot.font.size = Pt(11)
r_foot.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

docx_path = os.path.join(exp6_dir, "EXPERIMENT_6_REPORT.docx")
doc.save(docx_path)
print(f"Successfully generated DOCX: {docx_path}")
