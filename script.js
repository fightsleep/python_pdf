async function uploadAndExtractPDF() {
  const file = document.getElementById("pdfFile").files[0];
  if (file) {
    const formData = new FormData();
    formData.append("pdfFile", file);

    try {
      const response = await fetch("https://sleepqueue.com/extract-pdf", {
        method: "POST",
        body: formData
      });
      

      const lines = await response.json();

      // ประมวลผลและแสดงผลข้อมูลบนหน้าเว็บ
      lines.forEach((line) => {
        let parts = line.split(":");
        if (parts.length === 2) {
          let key = parts[0].trim();
          let value = parts[1].trim();
          fillFormData(key, value);
        }
      });
    } catch (error) {
      console.error("Error:", error);
    }
  }
}

function fillFormData(key, value) {
  if (key.includes("Patient ID")) {
    document.getElementById("PatientID").value = value.split(" ").pop(); // เอาเฉพาะหมายเลข
  } else if (key.includes("DOB")) {
    document.getElementById("DOB").value = value;
  } else if (key.includes("Age")) {
    document.getElementById("Age").value = value.split(" ")[0]; // เอาเฉพาะตัวเลขอายุ
  } else if (key.includes("Usage") && !key.includes("days")) {
    let usageDates = value.match(/\d{2}\/\d{2}\/\d{4} - \d{2}\/\d{2}\/\d{4}/); // ใช้ regular expression เพื่อหาวันที่
    if (usageDates && usageDates.length > 0) {
      document.getElementById("usage").value = usageDates[0];
    }
  }
  // คุณสามารถเพิ่มเงื่อนไขอื่นๆ ตามข้อมูลที่คุณต้องการเติม
}
