
var items = document.querySelectorAll('item');

items.forEach(item => {
    item.addEventListener('mouseover', () => {
        item.style.backgroundColor = 'gray';
    });

    // 마우스를 떼면 원래 색으로 돌아갑니다.
    item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = '#F1F5F2';
    });
});

