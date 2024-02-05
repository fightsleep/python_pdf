async function uploadAndExtractPDF() {
  const file = document.getElementById("pdfFile").files[0];
  if (file) {
    const formData = new FormData();
    formData.append("pdfFile", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/extract-pdf", {
        method: "POST",
        body: formData
      });
      const data = await response.json();
      console.log(data); // เพื่อดูโครงสร้างของข้อมูล

      // ประมวลผลและแสดงผลข้อมูลบนหน้าเว็บ
      for (const key in data) {
        if (data.hasOwnProperty(key)) {
          fillFormData(key, data[key]);
        }
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
}

function fillFormData(key, value) {
  if (key === "Patient ID") {
    document.getElementById("PatientID").value = value;
  } else if (key === "DOB") {
    document.getElementById("DOB").value = value;
  } else if (key === "Age") {
    document.getElementById("Age").value = value;
  } else if (key === "Compliance Report Date Range") {
    let usageDates = value.match(/\d{2}\/\d{2}\/\d{4} - \d{2}\/\d{2}\/\d{4}/);
    if (usageDates && usageDates.length > 0) {
      document.getElementById("usage").value = usageDates[0];
    }
  }
  // คุณสามารถเพิ่มเงื่อนไขอื่นๆ ตามข้อมูลที่คุณต้องการเติม
}
