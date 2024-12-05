const previewContainer = document.getElementById('previewContainer');

document.getElementById('imageUpload').addEventListener('change', function (event) {
    const files = event.target.files;

    previewContainer.innerHTML = '';

    Array.from(files).forEach(file => {
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewContainer.setAttribute('src',e.target.result)
            }
            reader.readAsDataURL(file);
        }
    });
});