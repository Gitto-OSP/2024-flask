function openTab(tabName) {
    document.querySelectorAll('.tab, .tabs').forEach(function(el) {
        el.classList.remove('on');
    });
    document.getElementById(tabName).classList.add('on');
    document.querySelector('.tabs[onclick="openTab(\'' + tabName + '\')"]').classList.add('on');
}


function toggleDropdown(button) {
    const container = button.previousElementSibling; 
    container.style.display = container.style.display === 'none' || container.style.display === '' ? 'inline-block' : 'none';
}

function updateStatus(selectElement, name) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const selectedStatusId = selectedOption.id;

    // DB에 상태 저장 요청
    fetch(`/update_gpstatus`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: name,
            status: selectedStatusId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("공동구매 상태가 성공적으로 변경되었습니다!");
            
            // 상태 텍스트 업데이트 (선택한 상태를 화면에 반영)
            const statusText = selectElement.parentElement.previousElementSibling;
            statusText.textContent = `${selectedOption.textContent} 중`;
            
            // 드롭다운 숨김
            selectElement.style.display = 'none';
        } else {
            alert(`오류: ${data.error}`);
        }
    })

    // 드롭다운 숨김
    selectElement.style.display = 'none';
}


function updateOption(selectElement) {
    const selectedStatus = selectElement.value;
    const statusText = selectElement.parentElement.previousElementSibling;
    statusText.textContent = `${selectedStatus}`;
    selectElement.style.display = 'none';
    // DB 작업 추가
}

function fn_ExcelDown(){
//DB작업 이후 경로 업데이트
    var comSubmit = new ComSubmit();
    comSubmit.setUrl();
    comSubmit.submit();
}
