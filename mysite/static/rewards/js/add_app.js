function addPoints() {
    let pointsButton = document.getElementById("addPointsBtn");
    let pointsInput = document.getElementById("pointsInput"); // Get the hidden input field

    let addedPoints = prompt("Enter Points to Add:", "10");

    if (addedPoints !== null && !isNaN(addedPoints) && addedPoints.trim() !== "") {
        pointsButton.textContent = addedPoints + " POINTS"; // Show points on the button
        pointsInput.value = addedPoints; // Update hidden input value
    }
}



function previewLogo(event) {
    let file = event.target.files[0];  // Get uploaded file
    if (file) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let preview = document.getElementById("logoPreview");
            let uploadIcon = document.getElementById("uploadIcon");

            preview.src = e.target.result;  // Set image source
            preview.classList.remove("hidden");  // Show image
            uploadIcon.classList.add("hidden");  // Hide icon
        };
        reader.readAsDataURL(file);
    }
}

function validateForm() {
    let name = document.querySelector("input[name='name']").value.trim();
    let link = document.querySelector("input[name='link']").value.trim();
    let category = document.querySelector("select[name='category']").value;
    let subcategory = document.querySelector("select[name='subcategory']").value;
    let points = document.getElementById("pointsInput").value.trim();
    let logo = document.getElementById("logoInput").files.length;

    let errorMessage = "";

    if (logo === 0) errorMessage += "Please upload a logo.\n";
    if (name === "") errorMessage += "Please enter an app name.\n";
    if (link === "") errorMessage += "Please enter an app link.\n";
    if (category === "App Category") errorMessage += "Please select a category.\n";
    if (subcategory === "Sub Category") errorMessage += "Please select a subcategory.\n";
    if (points === "0" || points === "") errorMessage += "Please add points.\n";

    if (errorMessage !== "") {
        alert(errorMessage);
        return false;  // Prevent form submission
    }
    return true;  // Allow form submission
}