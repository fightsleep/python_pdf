from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber

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
        return jsonify(lines)

if __name__ == '__main__':
    app.run(debug=True)
