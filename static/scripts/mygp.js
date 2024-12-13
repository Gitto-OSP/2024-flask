mygp.js
//참여자 정보 다운로드
document.addEventListener('DOMContentLoaded', function () {
    // 모든 다운로드 버튼을 찾기
    const buttons = document.querySelectorAll('.btn'); // 모든 버튼에 클래스 .btn 적용

    if (buttons.length === 0) {
        console.error("다운로드 버튼을 찾을 수 없습니다.");
        return;
    }

    console.log("찾은 다운로드 버튼 개수:", buttons.length);

    // 각 버튼에 대해 클릭 이벤트 리스너 등록
    buttons.forEach(button => {
        console.log("버튼:", button); // 각 버튼 객체 확인

        button.addEventListener('click', function () {
            const name = button.getAttribute('data-value');
            if (!name) {
                console.error("data-value 속성이 없습니다.");
                return;
            }

            console.log("버튼 클릭됨, data-value 값:", name);

            // Firebase REST API URL
            const databaseURL = "https://gitto2024-830e9-default-rtdb.firebaseio.com/";
            const apiURL = `${databaseURL}gp_item/${name}/participants.json`;

            console.log("API URL:", apiURL);

            // Firebase에서 데이터 가져오기
            fetch(apiURL)
                .then(response => response.json())
                .then(data => {
                    console.log("API 응답 데이터:", data);

                    if (!data) {
                        alert("참여자 데이터가 없습니다.");
                        return;
                    }

                    const participants = Object.values(data).map(participant => ({
                        이메일: participant.email || "",
                        옵션: participant.option || "",
                        사용자ID: participant.user_id || "",
                    }));

                    if (participants.length === 0) {
                        alert("참여자 데이터가 비어 있습니다.");
                        return;
                    }

                    // 엑셀 파일 생성 및 다운로드
                    const worksheet = XLSX.utils.json_to_sheet(participants);
                    const workbook = XLSX.utils.book_new();
                    XLSX.utils.book_append_sheet(workbook, worksheet, "Participants");
                    XLSX.writeFile(workbook, `${name}_participants.xlsx`);

                    console.log("엑셀 다운로드 완료");
                })
                .catch(error => {
                    console.error("API 요청 실패:", error);
                    alert("데이터를 가져오는 중 오류가 발생했습니다.");
                });
        });
    });
});



// 엑셀 파일 생성 및 다운로드 함수
function generateExcel(data, filename) {
    const worksheet = XLSX.utils.json_to_sheet(data); // JSON -> Worksheet 변환
    const workbook = XLSX.utils.book_new(); // 워크북 생성
    XLSX.utils.book_append_sheet(workbook, worksheet, "Participants"); // 시트 추가
    XLSX.writeFile(workbook, filename); // 파일 저장
}


// data.status 값에 따라 width를 동적으로 설정
const statusToWidthMapping = {
    "모집": "20%",
    "주문": "40%",
    "수취": "60%",
    "배부": "80%",
    "마감": "100%"
  };
  
 // 프로그래스 바 업데이트 함수
function updateProgressBar() {
    const progressBar = document.querySelector('.listobj_pbar');
    if (progressBar) {
        // data-status 속성 값 가져오기
        const status = progressBar.getAttribute('data-status');
        // 매핑된 width 가져오기 (기본값 20%)
        const newWidth = statusToWidthMapping[status] || '20%';
        // 프로그래스 바의 width 업데이트
        progressBar.style.width = newWidth;
    }
}

// DOMContentLoaded 이벤트 후 업데이트 실행
document.addEventListener('DOMContentLoaded', updateProgressBar);