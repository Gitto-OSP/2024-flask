const calYear = document.getElementById('selectedYear');
const calMonth = document.getElementById('selectedMonth');
const monthPrevBtn = document.getElementById('month-btn-prev');
const monthNextBtn = document.getElementById('month-btn-next');
const calendar = document.querySelector('.calendar');


const gp_item_ex = {
    'item1': {
        'seller': 'user1',
        'name': '학잠 공구',
        'startDate': '2024-12-10',
        'endDate': '2024-12-14',
    },
    'item2': {
        'seller': 'user2',
        'name': '돕바 공구',
        'startDate': '2024-12-11',
        'endDate': '2024-12-15',
    },
    'item3': {
        'seller': 'user3',
        'name': '배꽃봉 공구',
        'startDate': '2024-12-01',
        'endDate': '2024-12-09',
    },
    'item4': {
        'seller': 'user4',
        'name': '후리스 공구',
        'startDate': '2024-12-15',
        'endDate': '2024-12-16',
    },
}

document.addEventListener("DOMContentLoaded", function () {
    const currentDate = new Date()
    calYear.innerHTML = currentDate.getFullYear();
    calMonth.innerHTML = currentDate.getMonth() + 1;
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth() + 1);

    for (const item in gp_item_ex) {
        displayGpItemOnCalendar(gp_item_ex[item]);
    }
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
        const [y, m] = calcMonth(year, month - 1);
        prevDateDiv.id = `${y}-${String(m).padStart(2, '0')}-${String(lastDatePrevMonth - i).padStart(2, '0')}`;
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
        dateDiv.id = `${year}-${String(month).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
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
        const [y, m] = calcMonth(year, month + 1);
        nextDateDiv.id = `${y}-${String(m).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        const d = document.createElement('div');
        d.className = 'date-text';
        d.textContent = i;
        nextDateDiv.appendChild(d);
        calendar.appendChild(nextDateDiv);
    }
}

function addChildToElement(dateId, color) {
    const dateCell = document.getElementById(dateId);
    if (dateCell) {
        const task = document.createElement('div');
        task.className = "gp-date";
        task.style.backgroundColor = color;
        dateCell.appendChild(task);
    }
}

function generateRandomGreenGrayColor() {
    const green = Math.floor(Math.random() * 171);
    const red = Math.floor(Math.random() * green);
    const blue = Math.floor(Math.random() * green);

    return `rgb(${red}, ${green}, ${blue})`;
}

function displayGpItemOnCalendar(gp_item) {
    const startDateStr = gp_item.startDate; //표시용
    const endDateStr = gp_item.endDate;
    const startDate = new Date(startDateStr); //계산용
    const endDate = new Date(endDateStr);
    const color = generateRandomGreenGrayColor();

    let currentDate = startDate;
    currentDate.setDate(currentDate.getDate() + 1);
    while (currentDate < endDate) {
        const dateId = currentDate.toISOString().split('T')[0];
        console.log(dateId);
        addChildToElement(dateId, color);

        currentDate.setDate(currentDate.getDate() + 1);
    }

    const startCell = document.getElementById(startDateStr);
    const startTask = document.createElement('div');
    startTask.innerHTML = `${gp_item.seller}: ${gp_item.name}`
    startTask.className = 'gp-date gp-date-start';
    startTask.style.backgroundColor = color;
    startCell.appendChild(startTask);

    const endCell = document.getElementById(endDateStr);
    const endTask = document.createElement('div');
    endTask.className = 'gp-date gp-date-end';
    endTask.style.backgroundColor = color;
    endCell.appendChild(endTask);
}
