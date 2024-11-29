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