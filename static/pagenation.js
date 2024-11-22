const page_btn = document.querySelectorAll(".page_btn");
const prev_btn = document.getElementById("prev_btn");
const next_btn = document.getElementById("next_btn");

for(var i = 0; i<page_btn.length; i++){
    page_btn[i].addEventListener("click",pageClick);
}

prev_btn.addEventListener("click",prevClick);
next_btn.addEventListener("click",nextClick);

var curr_page = window.location.search.split('=')[1];
var curr_idx = 0;
var max_page = 13;  // 나중에 DB 데이터 양으로 계산하는 코드 추가 필요
var page_len = page_btn.length;

var btn = document.getElementById("page"+curr_page);
btn.setAttribute("style","color:green; text-decoration-line: underline; text-decoration-thickness: 1px; text-underline-offset: 2px;");

function pageClick(){
    var pg_num = Number(this.getAttribute("id").split("page")[1]);
    setPage(pg_num);
    // 이후 DB와 연동할 때 list obj 교체하는 코드 추가 필요
}

function setPage(pg){
    curr_page = pg;
    var btn = document.getElementById("page"+curr_page);
    btn.setAttribute("style","color:green; text-decoration-line: underline; text-decoration-thickness: 1px; text-underline-offset: 2px;");
    for(var i = 1; i<=page_len;i++){
        if(i==curr_page || curr_idx*page_len+i>max_page){
            continue;
        }
        document.getElementById("page"+i).setAttribute("style","text-decoration-line:none");
    }
}

function prevClick(){
    if(curr_idx==0){
        return;
    }
    curr_idx--;
    setIndex();
    setPage(1);
}

function nextClick(){
    if((curr_idx+1)*page_len>max_page){
        return;
    }
    curr_idx++;
    setIndex();
    setPage(1);
}

function setIndex(){
    for(var i = 0; i<page_len; i++){
        page_btn[i].setAttribute("style","display:block");
        var new_page = curr_idx*page_len+i+1;
        page_btn[i].innerHTML = new_page;
        if(new_page>max_page){
            page_btn[i].setAttribute("style","display:none");
        }
    }
}