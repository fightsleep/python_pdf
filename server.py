from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # เพิ่ม CORS

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    if 'pdfFile' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
        lines = text.split('\n') if text else []

        # ตรวจสอบบริษัทและดึงข้อมูลจาก PDF
        company = determine_company(text)
        data = extract_data_from_pdf(file, company)

        return jsonify(data)

def extract_info_by_regex(text, pattern):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1) if match else None

def determine_company(text):
    if "Encore Basic" in text:
        return "mic"
    elif "ResMed AirView version" in text:
        return "resmed"
    return None

def extract_data_from_pdf(pdf_file, company):
    if company == "mic":
        patterns = patterns_mic
        model = "MIC"
    elif company == "resmed":
        patterns = patterns_resmed
        model = "Resmed"
    else:
        return None

    with pdfplumber.open(pdf_file) as pdf:
        text = pdf.pages[0].extract_text()

    data = {key: extract_info_by_regex(text, pattern) for key, pattern in patterns.items()}
    data['Company'] = company
    data['Model'] = model
    return data

# ตั้งค่า regex patterns สำหรับทั้งสองบริษัท
patterns_mic = {
    "Patient ID": r'Patient ID:\s+(\d+)',
    "Model": 'MIC',
    "Compliance Report Date Range": r'Date Range\s+(\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4})',
    "Usage days": r'Days with Device Usage\s+(\d+ days)',
    "without Usage days": r'Days without Device Usage\s+(\d+ days)',
     "Percent Days with Device Usage": r'Percent Days with Device Usage\s+([\d.]+%)',
    ">= 4 hours": r'Percent of Days with Usage >= 4 Hours\s+([\d.]+%)',
       
}

patterns_resmed = {
    "Patient ID": r'Patient ID:\s+(\d+)',
    "Model": 'saintmed',
    "DOB": r'DOB:\s+(\d{2}/\d{2}/\d{4})',
    "Age": r'Age:\s+(\d+ years)',
    "Compliance Report Date Range": r'Usage\s+(\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4})',
    "Usage days": r'Usage days\s+(\d+/\d+ days \(\d+%\))',
    ">= 4 hours": r'>= 4 hours\s+(\d+ days \(\d+%\))',
    "< 4 hours": r'< 4 hours\s+(\d+ days \(\d+%\))',
    "Usage hours": r'Usage hours\s+(\d+ hours \d+ minutes)',
    "Average usage (total days)": r'Average usage \(total days\)\s+(\d+ hours \d+ minutes)',
    "Average usage (days used)": r'Average usage \(days used\)\s+(\d+ hours \d+ minutes)',
    "Median usage (days used)": r'Median usage \(days used\)\s+(\d+ hours \d+ minutes)',
    "Total used hours (since last reset)": r'Total used hours \(value since last reset - \d{2}/\d{2}/\d{4}\)\s+(\d+ hours)',
    "Serial number": r'Serial number\s+(\d+)',
    "Mode": r'Mode\s+(\w+)',
    "Set pressure": r'Set pressure\s+(\d+ cmH2O)',
    "EPR": r'EPR\s+(\w+)',
    "EPR level": r'EPR level\s+(\d+)',
    "Leaks - L/min Median": r'Leaks - L/min Median:\s+(\d+.\d+)',
    "95th percentile": r'95th percentile:\s+(\d+.\d+)',
    "Maximum": r'Maximum:\s+(\d+.\d+)',
    "Events per hour AI": r'Events per hour AI:\s+(\d+.\d+)',
    "HI": r'HI:\s+(\d+.\d+)',
    "AHI": r'AHI:\s+(\d+.\d+)',
    "Apnoea Index Central": r'Central:\s+(\d+.\d+)',
    "Obstructive": r'Obstructive:\s+(\d+.\d+)',
    "Unknown": r'Unknown:\s+(\d+.\d+)',
    "Cheyne-Stokes respiration": r'Cheyne-Stokes respiration \(average duration per night\)\s+(\d+ minutes \(0%\))'
}
def process_all_pdfs(folder_path):
    all_data = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            with pdfplumber.open(pdf_path) as pdf:
                if "mic" in file:
                    page = pdf.pages[8]
                else:
                    page = pdf.pages[0]
                text = page.extract_text()

            company = determine_company(text)
            extracted_data = extract_data_from_pdf(pdf_path, company)
            if extracted_data:
                all_data.append(extracted_data)

    return pd.DataFrame(all_data)

if __name__ == '__main__':
    app.run(debug=True)
