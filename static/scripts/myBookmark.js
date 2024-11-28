function showCategory(category) {
    // Hide all sections
    document.getElementById("used").style.display = "none";
    document.getElementById("group").style.display = "none";
    document.getElementById("brand").style.display = "none";

    // Show the selected section
    document.getElementById(category).style.display = "block";
}

// Initially show all sections or just one, like '중고거래'
showCategory('used');
