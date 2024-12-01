const imgUploadContainer = document.querySelector('.side-adding-container');
const inputFile = document.getElementById('imageUpload');

let selectedFiles = [];

inputFile.addEventListener('change', function (event) {
    const files = event.target.files;

    Array.from(files).forEach(file => {
        const isDuplicate = selectedFiles.some(
            selectedFile =>
                selectedFile.name === file.name &&
                selectedFile.size === file.size
        );
        if (isDuplicate) return;

        if (file) {
            selectedFiles.push(file);
            console.log(selectedFiles);
            const reader = new FileReader();
            reader.onload = function (e) {
                const divPreviewContainer = document.createElement('div');
                divPreviewContainer.className = 'preview-container';
                divPreviewContainer.style.display = 'block';

                const imagePreview = document.createElement('img');
                imagePreview.src = e.target.result;
                imagePreview.className = "image-preview";
                imagePreview.alt = `${file.name}`;
                imagePreview.title = `${file.name}`;

                const removeButton = document.createElement('div');
                removeButton.className = "remove-button remove-button-design";
                removeButton.innerHTML = "X";
                removeButton.addEventListener('click', function (event) {
                    const removeBtn = event.target;
                    removeBtn.closest(".preview-container").remove();

                    const fileIndex = selectedFiles.indexOf(file);
                    if (fileIndex > -1) {
                        selectedFiles.splice(fileIndex, 1);
                    }
                    console.log(selectedFiles);
                });

                divPreviewContainer.appendChild(imagePreview);
                divPreviewContainer.appendChild(removeButton);

                imgUploadContainer.appendChild(divPreviewContainer);
            }
            reader.readAsDataURL(file);
        }
    });
});

const form = document.querySelector('form');
form.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('selectedFile', file);
    });

    const form = document.querySelector('form');
    const formInputData = new FormData(form);
    formInputData.forEach((value, key) => {
        formData.append(key, value);
    });

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())  // 응답이 HTML인 경우
        .then(data => {
            console.log('Response:', data); // HTML 데이터를 콘솔에 출력
            document.body.innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});