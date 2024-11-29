function addLink(linkName) {
    const inputWrapper = document.getElementById('snsInputs');
    const inputContainer = document.createElement('div');
    inputContainer.className = "input-container";

    const label = document.createElement('label');
    label.htmlFor = linkName;
    label.innerHTML = linkName;

    const input = document.createElement('input');
    input.type = "url";
    input.name = "socials";
    input.placeholder = "https://example.com";
    input.required = true;

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