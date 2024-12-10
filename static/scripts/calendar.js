const calYear = document.getElementById('selectedYear');
const calMonth = document.getElementById('selectedMonth');
const monthPrevBtn = document.getElementById('month-btn-prev');
const monthNextBtn = document.getElementById('month-btn-next');
const calendar = document.querySelector('.calendar');

document.addEventListener("DOMContentLoaded", function () {
    const currentDate = new Date()
    calYear.innerHTML = currentDate.getFullYear();
    calMonth.innerHTML = currentDate.getMonth() + 1;
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth() + 1);
});

function calcMonth(year, month) {
    if (month <= 0) return [year - 1, 12];
    if (month > 12) return [year + 1, 1];
    return [year, month];
}

monthPrevBtn.addEventListener("click", function () {
    calendar.innerHTML = '';
    const [year, month] = calcMonth(Number(calYear.innerHTML), Number(calMonth.innerHTML) - 1);
    calYear.innerHTML = year;
    calMonth.innerHTML = month;
    generateCalendar(year, month);
})

monthNextBtn.addEventListener("click", function () {
    calendar.innerHTML = '';
    const [year, month] = calcMonth(Number(calYear.innerHTML), Number(calMonth.innerHTML) + 1);
    calYear.innerHTML = year;
    calMonth.innerHTML = month;
    generateCalendar(year, month);
})

function generateCalendar(year, month) {
    const lastDatePrevMonth = new Date(year, month - 1, 0).getDate()
    const firstDay = new Date(year, month - 1, 1).getDay(); // 현재 달 첫 날 요일 (0: 일요일, 1: 월요일, ...)
    const lastDate = new Date(year, month, 0).getDate(); // 현재 달의 마지막 날짜

    const totalDays = firstDay + lastDate; // 총 날짜: 이전 빈 칸 포함
    const totalWeeks = Math.ceil(totalDays / 7); // 7일 기준으로 나눔
    for (let week = 1; week <= totalWeeks; week++) {
        const weekSummary = document.createElement('div');
        weekSummary.id = `week${week}`;
        weekSummary.className = 'week-sum';
        calendar.appendChild(weekSummary);
    }

    for (let i = firstDay - 1; i >= 0; i--) {
        const prevDateDiv = document.createElement('div');
        prevDateDiv.className = 'date prev-month';
        const d = document.createElement('div');
        d.className = 'date-text';
        d.textContent = lastDatePrevMonth - i; // 이전 달 날짜 계산
        prevDateDiv.appendChild(d);
        calendar.appendChild(prevDateDiv);
    }

    // 현재 달 날짜 추가
    for (let date = 1; date <= lastDate; date++) {
        const dateDiv = document.createElement('div');
        dateDiv.className = 'date';
        const d = document.createElement('div');
        d.className = 'date-text';
        d.textContent = date;
        dateDiv.appendChild(d);
        calendar.appendChild(dateDiv);
    }

    // 마지막 주에 다음 달 날짜 추가
    const remainingDays = (7 - ((firstDay + lastDate) % 7)) % 7;
    for (let i = 1; i <= remainingDays; i++) {
        const nextDateDiv = document.createElement('div');
        nextDateDiv.className = 'date next-month';
        const d = document.createElement('div');
        d.className = 'date-text';
        d.textContent = i;
        nextDateDiv.appendChild(d);
        calendar.appendChild(nextDateDiv);
    }
}

// 예시: 2024년 12월 달력을 생성

