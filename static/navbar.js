const account_in = document.getElementById("account_in");
const login_btn = document.getElementById("login_btn");
const account_out = document.getElementById("account_out");
const logout_btn = document.getElementById("logout_btn");

account_in.setAttribute("style","background-color:red");
account_out.setAttribute("style","background-color:red");

login_btn.addEventListener("click",login);
logout_btn.addEventListener("click",logout);

var login_info = false;
setNavAccount();

function login(){
    login_info = true;
    setNavAccount();
}

function logout(){
    login_info = false;
    setNavAccount();
}

function setNavAccount(){
    var on_obj;
    var off_obj;
    if(login_info){
        on_obj = account_in;
        off_obj = account_out;
    }
    else{
        on_obj = account_out;
        off_obj = account_in;
    }
    off_obj.setAttribute("style","display:none");
    on_obj.setAttribute("style","display:block");
}
