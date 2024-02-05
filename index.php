<!DOCTYPE html>
<html>

<head>
    <!-- เพิ่ม Bootstrap CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>

    <div class="container mt-5">
        <form id="uploadForm">
            <div class="form-group">
                <label for="pdfFile">Upload PDF File:</label>
                <input type="file" class="form-control-file" id="pdfFile" accept="application/pdf" />
            </div>
            <button type="button" class="btn btn-primary" onclick="uploadAndExtractPDF()">Upload and Extract</button>
        </form>

        <form id="dataForm" class="mt-4">
            <div class="form-group">
                <label for="PatientID">Patient ID:</label>
                <input type="text" class="form-control" id="PatientID" name="patient_id" placeholder="Enter Patient ID" />
            </div>
            <div class="form-group">
                <label for="DOB">Date of Birth:</label>
                <input type="text" class="form-control" id="DOB" name="dob" placeholder="Enter DOB" />
            </div>
            <div class="form-group">
                <label for="Age">Age:</label>
                <input type="text" class="form-control" id="Age" name="age" placeholder="Enter Age" />
            </div>
            <div class="form-group">
                <label for="usage">Usage:</label>
                <input type="text" class="form-control" id="usage" name="usage" placeholder="" />
            </div>
            <!-- เพิ่ม input อื่น ๆ ตามที่คุณต้องการ -->
            <button type="submit" class="btn btn-success">Save Data</button>
        </form>
    </div>

    <!-- เพิ่ม Bootstrap JS และ jQuery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="build/pdf.js"></script>
    <script src="build/pdf.worker.js"></script>
    <script src="script.js"></script>

</body>

</html>