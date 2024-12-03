function showCategory(category) {
    document.getElementById("used").style.display = "none";
    document.getElementById("group").style.display = "none";
    document.getElementById("brand").style.display = "none";

    document.getElementById(category).style.display = "block";
}

showCategory("used")