avatar_visible = false;
acc_panel_visible = false;

front_url = window.location.protocol + "//" + window.location.hostname + ":8080/";
back_url = window.location.protocol + "//"+ window.location.hostname + ":8081/";

function show_buttons(){
    // shows buttons, hides avatar
    if (avatar_visible){
        document.getElementById("avatar_in_header").style = "display: none;";
        document.getElementById("log_in_buttons").style = "display: inline;";
        avatar_visible = false;
    }
}

function show_avatar(){
    // hides buttons, shows avatar
    if (!avatar_visible){
        document.getElementById("log_in_buttons").style = "display: none;";
        document.getElementById("avatar_in_header").style = "display: inline;";
        avatar_visible = true;
    }

}

function show_acc_panel(){
    // shows or hides account panel(profile, settings, log out)
    if(acc_panel_visible){
        document.getElementsByClassName("acc_panel")[0].style = "display: none;";
        acc_panel_visible = false
    }
    else{
        document.getElementsByClassName("acc_panel")[0].style = "display: inline;";
        acc_panel_visible = true
    }
}

function show_login_panel(bool = true){
    //shows or hides login panel
    if(bool){
        document.getElementsByClassName("loginer")[0].style = "display: inline;";
    }
    else{
        document.getElementsByClassName("loginer")[0].style = "display: none;";
    }
}

function show_signup_panel(bool = true){
    //shows or hides sign up panel
    if(bool){
        document.getElementsByClassName("registrator")[0].style = "display: inline;";
    }
    else{
        document.getElementsByClassName("registrator")[0].style = "display: none;";
        document.getElementsByClassName("telegram_sign_up")[0].style = "display: none;";
        document.getElementsByClassName("email_sign_up")[0].style = "display: none;";
    }
}

function show_telegram_verif(){
    //shows telegram verif fields and hides email verif fields
    document.getElementsByClassName("telegram_sign_up")[0].style = "display: inline;";
    document.getElementsByClassName("email_sign_up")[0].style = "display: none;";
    document.getElementById("reg_auth_code_email").value = "";
    document.getElementById("reg_verif_code_email").value = "";
}
function show_email_verif(){
    //shows email verif fields and hides telegram verif fields
    document.getElementsByClassName("email_sign_up")[0].style = "display: inline;";
    document.getElementsByClassName("telegram_sign_up")[0].style = "display: none;";
    document.getElementById("reg_auth_code_tg").value = "";
    document.getElementById("reg_verif_code_tg").value = "";
}

function validation(){
    // returns true if user data is valid
    good = true;
    login = document.getElementById("reg_login").value;
    nickname = document.getElementById("reg_nickname").value;
    password1 = document.getElementById("reg_password1").value;
    password2 = document.getElementById("reg_password2").value;
    telegram = document.getElementById("reg_auth_code_tg").value;
    email = document.getElementById("reg_auth_code_email").value;
    
    // errors clearing
    errors = document.getElementsByClassName("errors");
    for(let index = 0; index < errors.length; index++){
        errors[index].innerHTML = "";
    }

    // empty login
    if(login == ""){
        err = document.getElementById("reg_login_err");
        err.innerHTML = "Login can`t be empty!";
        good = false;
    }

    // empty nickname
    if(nickname == ""){
        err = document.getElementById("reg_nickname_err");
        err.innerHTML = "NickName can`t be empty!";
        good = false;
    }

    // empty password1
    if(password1 == ""){
        err = document.getElementById("reg_password1_err");
        err.innerHTML = "Password can`t be empty!";
        good = false;
    }

    // empty password2
    if(password2 == ""){
        err = document.getElementById("reg_password2_err");
        err.innerHTML = "Password confirmation can`t be empty!";
        good = false;
    }

    // passwords are mismatched
    if(password1 != password2){
        err = document.getElementById("reg_password2_err");
        err.innerHTML = "Password mismatch!";
        good = false;
    }

    // empty autentication code or email
    if(telegram == "" && email == ""){
        err = document.getElementById("reg_auth_code_tg_err");
        err.innerHTML = "Authentication code can`t be empty!";
        err = document.getElementById("reg_auth_code_email_err");
        err.innerHTML = "Email can`t be empty!";
        good = false;
    }

    // bad email
    if(email != "" && email.indexOf("@") == -1){
        err = document.getElementById("reg_auth_code_email_err");
        err.innerHTML = "This is not Email👀!";
        good = false;
    }

    return good
}

function getVerifCode(){
    // sends verification code to user
    if(validation()){
        const xhttp_for_unique_login_and_auth = new XMLHttpRequest();
        xhttp_for_unique_login_and_auth.onload = function() {
            good = true;

            // not unique login
            if(this.responseText == "Login is already taken"){
                err = document.getElementById("reg_login_err");
                err.innerHTML = "Login is already taken!";
                good = false;
            }

            // not unique email or authentication code
            if(this.responseText == "Authentication name is already taken"){
                err = document.getElementById("reg_auth_code_tg_err");
                err.innerHTML = "Authentication code is already taken!";
                err = document.getElementById("reg_auth_code_email_err");
                err.innerHTML = "Email is already taken!";
                good = false;
            }

            if(good){
                const xhttp = new XMLHttpRequest();
                xhttp.onload = function() {

                    // not something wrong with email or authentication code
                    if(this.responseText == "Error"){
                        err = document.getElementById("reg_auth_code_tg_err");
                        err.innerHTML = "Something wrong with authentication code!";
                        err = document.getElementById("reg_auth_code_email_err");
                        err.innerHTML = "Something wrong with email!";
                    }
                    else if(this.responseText == "Email sended"){
                        status_message = document.getElementById("get_code_status_email")
                        status_message.innerHTML = "Code is sended to your email!"
                    }
                    else if(this.responseText == "Tg sended"){
                        status_message = document.getElementById("get_code_status_tg")
                        status_message.innerHTML = "Code is sended to your telegram!"
                    }
                }

                telegram = document.getElementById("reg_auth_code_tg").value;
                email = document.getElementById("reg_auth_code_email").value;    
                xhttp.open("GET", back_url + "getVerifCode?authentication=" + email + telegram, true);
                xhttp.send();
            }

        }
        xhttp_for_unique_login_and_auth.open("GET", back_url + "checkVerlidation?login=" + login + "&authentication=" + email + telegram, true);
        xhttp_for_unique_login_and_auth.send();
    }
}


function createAccount(){
    // creates account
    if(validation()){
        verif_tg = document.getElementById("reg_verif_code_tg").value;
        verif_email = document.getElementById("reg_verif_code_email").value;
        
        // empty verif code
        if(verif_email + verif_tg == ""){
            err = document.getElementById("reg_verif_tg_err");
            err.innerHTML = "Verification code can`t be empty!";
            err = document.getElementById("reg_verif_email_err");
            err.innerHTML = "Verification code can`t be empty!";
            
        }

        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            
            // verif code mismatch
            if(this.responseText == "verif code mismatch"){
                err = document.getElementById("reg_verif_tg_err");
                err.innerHTML = "Wrong verification code!";
                err = document.getElementById("reg_verif_email_err");
                err.innerHTML = "Wrong verification code!";
            }
            else if(this.responseText == "account created"){
                show_signup_panel(false);
            }
        };

        login = document.getElementById("reg_login").value;
        nickname = document.getElementById("reg_nickname").value;
        password1 = document.getElementById("reg_password1").value;
        password2 = document.getElementById("reg_password2").value;
        telegram = document.getElementById("reg_auth_code_tg").value;
        email = document.getElementById("reg_auth_code_email").value;    
        
        xhttp.open("GET", back_url + "createAccount?login=" + login + "&nickname=" + nickname + "&password=" + password1 + "&authentication=" + telegram + email + "&verification=" + verif_tg + verif_email, true);
        xhttp.send();
    }
}
