# server.py (ตัวอย่างโค้ดสำหรับฝั่งเซิร์ฟเวอร์)
from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    if 'pdfFile' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file and allowed_file(file.filename):
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
        lines = text.split('\n') if text else []
        # ประมวลผลข้อมูลให้อยู่ในรูปแบบที่ต้องการ
        data_pairs = process_data(lines)
        return jsonify(data_pairs)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

def process_data(lines):
    data_pairs = {}
    for line in lines:
        parts = line.split(":")
        if len(parts) == 2:
            key = parts[0].replace(/\s+/g, "")
            value = parts[1].strip()
            data_pairs[key] = value
    return data_pairs

if __name__ == '__main__':
    app.run(debug=True)
