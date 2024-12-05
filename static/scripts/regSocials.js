function createStyledInputTypeText(name, placeholder) {
    const input = document.createElement('input');
    input.type = "text";
    input.name = name;
    input.placeholder = placeholder;
    input.required = true;
    input.className = "input-style";
    return input
}

function createLabel(forElement, text) {
    const label = document.createElement('label');
    label.htmlFor = forElement;
    label.innerHTML = text;
    return label;
}

function addLink(linkName, socialType) {
    const inputWrapper = document.getElementById('snsInputs');
    const inputContainer = document.createElement('div');
    inputContainer.className = "input-container";

    const label = (linkName === "기타링크") ? createStyledInputTypeText('etcName', '직접 입력') : createLabel(socialType, linkName);

    const placeholder = (linkName === "기타링크") ? "https://example.com" : "@example";
    const input = createStyledInputTypeText(socialType, placeholder);

    const button = document.createElement('div');
    button.innerHTML = "x";
    button.className = 'remove-button-design';
    button.addEventListener('click', (event) => {
        const removeBtn = event.target;
        removeBtn.closest('.input-container').remove();
    })

    inputContainer.appendChild(label);
    inputContainer.appendChild(input);
    inputContainer.appendChild(button);
    inputWrapper.appendChild(inputContainer);
}