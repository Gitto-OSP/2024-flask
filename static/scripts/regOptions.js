document.getElementById('addOption').addEventListener('click', function () {
    const optionInput = document.getElementById('optionInput');
    const optionVal = optionInput.value;
    const container = document.getElementById('optionContainer');

    const optionDiv = document.createElement('div');
    optionDiv.className = 'gp-option';
    optionDiv.innerHTML = `
    <div>${optionInput.value}</div>
    `;

    const button = document.createElement('div');
    button.innerHTML = "x";
    button.className = 'remove-button-design';
    button.addEventListener('click', (event) => {
        const removeBtn = event.target;
        removeBtn.closest('.gp-option').remove();
    })

    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'options[]';
    hiddenInput.value = optionVal;

    optionDiv.appendChild(button);
    optionDiv.appendChild(hiddenInput);
    container.appendChild(optionDiv);

    optionInput.value = '';
});

document.getElementById('optionContainer').addEventListener('click', function (e) {
    if (e.target.classList.contains('remove-option')) {
        e.target.parentElement.remove();
    }
});