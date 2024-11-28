const previewContainer = document.getElementById('previewContainer');

document.getElementById('imageUpload').addEventListener('change', function (event) {
    const files = event.target.files;

    previewContainer.innerHTML = '';

    Array.from(files).forEach(file => {
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.maxWidth = '160px';  // 미리보기 이미지 크기 제한
                img.style.maxHeight = '160px'; // 미리보기 이미지 크기 제한
                previewContainer.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });
});