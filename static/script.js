document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('upload-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData();
        var fileInput = document.getElementById('file-input');
        formData.append('file', fileInput.files[0]);
        
        // Display the selected image
        displayImage(fileInput.files[0]);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            displayResult(data.result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function displayImage(file) {
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = document.createElement('img');
        img.src = event.target.result;
        img.width = 300; // Adjust image width as needed
        var imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = ''; // Clear previous image
        imageContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
}

function displayResult(result) {
    var resultDiv = document.getElementById('result');
    resultDiv.innerText = result;
    resultDiv.classList.add('visible');
}
