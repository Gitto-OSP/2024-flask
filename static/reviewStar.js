const stars = document.querySelectorAll('.starLabel');
let currentRating = '';

stars.forEach((star, index) => {
    star.addEventListener('mouseenter', () => {
        fillStarts(index);
    });
    star.addEventListener('mouseleave', () => {
        clearStars();
    });
    star.addEventListener('click', (e) => {
        selectStars(e);
    })
});

function selectStars(e) {
    const target = e.target.id;
    currentRating = target.slice(-1);
}

function fillStarts(index) {
    for (let i = 0; i <= index; i++) {
        stars[i].classList.add('filledStar');
    }
}

function clearStars() {
    stars.forEach(star => star.classList.remove('filledStar'));
    if (currentRating) fillStarts(currentRating - 1);
}