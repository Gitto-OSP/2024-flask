function openTab(tabName) {
    document.querySelectorAll('.tab, .tabs').forEach(function(el) {
        el.classList.remove('on');
    });
    document.getElementById(tabName).classList.add('on');
    document.querySelector('.tabs[onclick="openTab(\'' + tabName + '\')"]').classList.add('on');
}