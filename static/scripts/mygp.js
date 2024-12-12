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

function fn_ExcelDown(value) {
    if (!value || !value.name) {
        console.error("Invalid value object. Ensure 'value.name' is provided.");
        return;
    }

    // Firebase 데이터베이스 경로 정의 (value.name 사용)
    var databaseRef = firebase.database().ref(value.name + "/participants");

    // 데이터를 읽어온 후 Excel로 변환
    databaseRef.once("value").then((snapshot) => {
        var data = [];
        snapshot.forEach((childSnapshot) => {
            var participant = childSnapshot.val();
            data.push({
                email: participant.email || "",
                option: participant.option || "",
                user_id: participant.user_id || "",
                price: participant.price || ""
            });
        });

        // JSON 데이터를 워크시트로 변환
        var worksheet = XLSX.utils.json_to_sheet(data);

        // 워크북 생성
        var workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Participants");

        // Excel 파일 다운로드 (value.name 기반으로 파일명 설정)
        XLSX.writeFile(workbook, `${value.name}_participants.xlsx`);
    }).catch((error) => {
        console.error(`Error fetching participants data for ${value.name}:`, error);
    });
}
