function handleInput(event) {
    const inputValue = event.target.value;
    const container = document.getElementById('image-upload-wrapper');

    const currentItems = container.children.length;

    if (inputValue > currentItems) {
        for (let i = currentItems; i < inputValue; i++) {
            const newItem = generateImageElement(i);
            container.appendChild(newItem);
        }
    }
    else if (inputValue < currentItems) {
        for (let i = currentItems; i > inputValue; i--) {
            container.removeChild(container.lastChild);
        }
    }
}

function generateImageAddElement(i) {
    const divContainer = document.createElement('div');
    divContainer.className = 'image-upload-container';

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.name = `boothProductImg${i}`;
    fileInput.className = 'image-file-input';
    fileInput.accept = "image/*";

    const plusSpan = document.createElement('span');
    plusSpan.innerHTML = "+";
    plusSpan.className = "add-button";

    const addImageLabel = document.createElement('label');
    addImageLabel.className = "add-image-label";
    addImageLabel.appendChild(plusSpan);
    addImageLabel.appendChild(fileInput);

    const divPreviewContainer = document.createElement('div');
    divPreviewContainer.className = 'preview-container';

    const imagePreview = document.createElement('img');
    imagePreview.className = "image-preview";
    imagePreview.alt = "Preview";

    const removeButton = document.createElement('div');
    removeButton.className = "remove-button";
    removeButton.innerHTML = "X";

    divPreviewContainer.appendChild(imagePreview);
    divPreviewContainer.appendChild(removeButton);

    divContainer.appendChild(addImageLabel);
    divContainer.appendChild(divPreviewContainer);

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.src = e.target.result;
                divPreviewContainer.style.display = 'block';
                addImageLabel.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }
    });

    removeButton.addEventListener('click', function () {
        fileInput.value = '';
        imagePreview.src = '';
        divPreviewContainer.style.display = 'none';
        addImageLabel.style.display = 'flex';
    });

    return divContainer;
}

function generateImageElement(i) {
    const div = document.createElement('div');
    div.className = "regSeasonImgContainer";

    const addBtn = generateImageAddElement(i);

    const nameLabel = document.createElement('label');
    nameLabel.innerHTML = '상품 이름';
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.name = `product${i}Name`;
    nameInput.id = `product${i}Name`;
    nameLabel.appendChild(nameInput);

    const priceLabel = document.createElement('label');
    priceLabel.innerHTML = '상품 가격';
    const priceInput = document.createElement('input');
    priceInput.type = 'number';
    priceInput.name = `product${i}Price`;
    priceInput.id = `product${i}Price`;
    priceLabel.appendChild(priceInput);

    div.appendChild(addBtn);
    div.appendChild(nameLabel);
    div.appendChild(priceLabel);

    return div;
}