let acc_panel_visible = false;

let front_url = window.location.protocol + "//" + window.location.hostname + ":8080/";
let back_url = window.location.protocol + "//"+ window.location.hostname + ":8081/";

function show_buttons(){
    // shows buttons, hides avatar
        document.getElementById("avatar_in_header").style = "display: none;";
        document.getElementById("log_in_buttons").style = "display: inline;";
}

function show_avatar(){
    // hides buttons, shows avatar
        document.getElementById("log_in_buttons").style = "display: none;";
        document.getElementById("avatar_in_header").style = "display: inline;";
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

function clearErrorsAndStatuses(){
    // clears errors and statuses
    let errors = document.getElementsByClassName("errors");
    for(let index = 0; index < errors.length; index++){
        errors[index].innerHTML = "";
    }
    let statuses = document.getElementsByClassName("status");
    for(let index = 0; index < statuses.length; index++){
        statuses[index].innerHTML = "";
    }
}

function reg_validation(){
    // returns true if user data is valid
    let good = true;
    let login = document.getElementById("reg_login").value;
    let nickname = document.getElementById("reg_nickname").value;
    let password1 = document.getElementById("reg_password1").value;
    let password2 = document.getElementById("reg_password2").value;
    let telegram = document.getElementById("reg_auth_code_tg").value;
    let email = document.getElementById("reg_auth_code_email").value;
    
    // errors clearing
    clearErrorsAndStatuses()

    // empty login
    if(login == ""){
        let err = document.getElementById("reg_login_err");
        err.innerHTML = "Login can`t be empty!";
        good = false;
    }

    // empty nickname
    if(nickname == ""){
        let err = document.getElementById("reg_nickname_err");
        err.innerHTML = "NickName can`t be empty!";
        good = false;
    }

    // empty password1
    if(password1 == ""){
        let err = document.getElementById("reg_password1_err");
        err.innerHTML = "Password can`t be empty!";
        good = false;
    }

    // empty password2
    if(password2 == ""){
        let err = document.getElementById("reg_password2_err");
        err.innerHTML = "Password confirmation can`t be empty!";
        good = false;
    }

    // passwords are mismatched
    if(password1 != password2){
        let err = document.getElementById("reg_password2_err");
        err.innerHTML = "Password mismatch!";
        good = false;
    }

    // empty autentication code or email
    if(telegram == "" && email == ""){
        let err = document.getElementById("reg_auth_code_tg_err");
        err.innerHTML = "Authentication code can`t be empty!";
        err = document.getElementById("reg_auth_code_email_err");
        err.innerHTML = "Email can`t be empty!";
        good = false;
    }

    // bad email
    if(email != "" && email.indexOf("@") == -1){
        let err = document.getElementById("reg_auth_code_email_err");
        err.innerHTML = "This is not Email👀!";
        good = false;
    }

    return good
}

function log_validation(){// returns true if user data is valid
    let good = true;
    let login = document.getElementById("log_login").value;
    let password = document.getElementById("log_password").value;
        
    // errors clearing
    clearErrorsAndStatuses();

    // empty login
    if(login == ""){
        let err = document.getElementById("log_login_err");
        err.innerHTML = "Login can`t be empty!";
        good = false;
    }

    // empty password1
    if(password == ""){
        let err = document.getElementById("log_password_err");
        err.innerHTML = "Password can`t be empty!";
        good = false;
    }

    return good
}

function getVerifCode_reg(){
    // sends verification code to user
    if(reg_validation()){
        const xhttp_for_unique_login_and_auth = new XMLHttpRequest();
        
        let telegram = document.getElementById("reg_auth_code_tg").value;
        let email = document.getElementById("reg_auth_code_email").value; 
        let login = document.getElementById("reg_login").value;

        xhttp_for_unique_login_and_auth.onload = function() {
            let good = true;

            // not unique login
            if(this.responseText == "Login is already taken"){
                let err = document.getElementById("reg_login_err");
                err.innerHTML = "Login is already taken!";
                good = false;
            }

            // not unique email or authentication code
            if(this.responseText == "Authentication name is already taken"){
                let err = document.getElementById("reg_auth_code_tg_err");
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
                        let err = document.getElementById("reg_auth_code_tg_err");
                        err.innerHTML = "Something wrong with authentication code!";
                        err = document.getElementById("reg_auth_code_email_err");
                        err.innerHTML = "Something wrong with email!";
                    }
                    else if(this.responseText == "Email sended"){
                        let status_message = document.getElementById("get_code_status_email")
                        status_message.innerHTML = "Code is sended to your email!"
                    }
                    else if(this.responseText == "Tg sended"){
                        let status_message = document.getElementById("get_code_status_tg")
                        status_message.innerHTML = "Code is sended to your telegram!"
                    }
                }
   
                xhttp.open("GET", back_url + "getVerifCodeReg?authentication=" + email + telegram, true);
                xhttp.send();
            }

        }
        xhttp_for_unique_login_and_auth.open("GET", back_url + "checkVerlidation?login=" + login + "&authentication=" + email + telegram, true);
        xhttp_for_unique_login_and_auth.send();
    }
}

function getVerifCode_log(){
    // sends verification code to user
    if(log_validation()){
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {

            // not something wrong with email or authentication code
            if(this.responseText == "No login"){
                let err = document.getElementById("log_login_err")
                err.innerHTML = "No such login, try to sign up!"
            }
            else if(this.responseText == "Bad password"){
                let err = document.getElementById("log_password_err")
                err.innerHTML = "Bad password!"
            }
            else if(this.responseText == "Email sended"){
                let status_message = document.getElementById("get_code_status_login")
                status_message.innerHTML = "Code is sended to your email!"
            }
            else if(this.responseText == "Tg sended"){
                let status_message = document.getElementById("get_code_status_login")
                status_message.innerHTML = "Code is sended to your telegram!"
            }
            else if(this.responseText == "Error"){
                console.log("something wrong")
            }
        }
        let login = document.getElementById("log_login").value;
        let password = document.getElementById("log_password").value;
        xhttp.open("GET", back_url + "getVerifCodeLog?login=" + login + "&password=" + password, true);
        xhttp.send();

    }
}


function createAccount(){
    // creates account
    if(reg_validation()){
        let verif_tg = document.getElementById("reg_verif_code_tg").value;
        let verif_email = document.getElementById("reg_verif_code_email").value;
        
        // empty verif code
        if(verif_email + verif_tg == ""){
            let err = document.getElementById("reg_verif_tg_err");
            err.innerHTML = "Verification code can`t be empty!";
            err = document.getElementById("reg_verif_email_err");
            err.innerHTML = "Verification code can`t be empty!";
            
        }

        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            
            // verif code mismatch
            if(this.responseText == "verif code mismatch"){
                let err = document.getElementById("reg_verif_tg_err");
                err.innerHTML = "Wrong verification code!";
                err = document.getElementById("reg_verif_email_err");
                err.innerHTML = "Wrong verification code!";
            }
            else if(this.responseText.startsWith("account created,")){
                show_signup_panel(false);

                let session = this.responseText.substring("account created,".length);
                document.cookie = "session=" + session + ";max-age=" + (60 * 60 * 24 * 100);
                autoLogin()
            }
        };

        let login = document.getElementById("reg_login").value;
        let nickname = document.getElementById("reg_nickname").value;
        let password1 = document.getElementById("reg_password1").value;
        let telegram = document.getElementById("reg_auth_code_tg").value;
        let email = document.getElementById("reg_auth_code_email").value;    
        
        xhttp.open("GET", back_url + "createAccount?login=" + login + "&nickname=" + nickname + "&password=" + password1 + "&authentication=" + telegram + email + "&verification=" + verif_tg + verif_email, true);
        xhttp.send();
    }
}

function logInAccount(){
    if(log_validation){
        let good = true;
        let login = document.getElementById("log_login").value;
        let password = document.getElementById("log_password").value;
        let verif = document.getElementById("log_verif").value;

        // empty verif code
        if (verif == ""){
            let err = document.getElementById("log_verif_err");
            err.innerHTML = "Verification code can`t be empty!"
            good = false;
        }

        if(good){
            xhttp = new XMLHttpRequest();
            xhttp.onload = function(){
                
                // not something wrong with email or authentication code
                if(this.responseText == "No login"){
                    let err = document.getElementById("log_login_err")
                    err.innerHTML = "No such login, try to sign up!"
                }
                else if(this.responseText == "Bad password"){
                    let err = document.getElementById("log_password_err")
                    err.innerHTML = "Bad password!"
                }
                else if(this.responseText == "Bad verif"){
                    let err = document.getElementById("log_verif_err")
                    err.innerHTML = "Bad Verification code!"
                }
                else if(this.responseText.startsWith("login successfully,")){
                    show_login_panel(false);

                    let session = this.responseText.substring("login successfully,".length);
                    document.cookie = "session=" + session + ";max-age=" + (60 * 60 * 24 * 100);
                    autoLogin()
                }

            }
            xhttp.open("GET", back_url + "logIn?login=" + login + "&password=" + password + "&verification=" + verif, true);
            xhttp.send();
        }

    }
}


function deleteSession(){
    // deletes session from cookies
    document.cookie = "session=" + "d" + ";max-age=0";
    show_buttons();
    acc_panel_visible = true;
    show_acc_panel();
}


function getSession(){
    // returns session from cookies
    let session_str = "session="
    let my_cookie = document.cookie
    if(my_cookie.includes(session_str)){
        let start_point = my_cookie.indexOf(session_str) + session_str.length
        my_cookie = my_cookie.substring(start_point)
        let end_point = my_cookie.indexOf(";")
        if(end_point == -1){
            return my_cookie;
        }
        else {
            return my_cookie.substring(0, end_point);
        }
    }
    return null
}


function autoLogin(){
    let session = getSession();
    if (session != null){
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            if(this.responseText == "None"){
                show_buttons();
                deleteSession();
            }
            else{
                show_avatar();

            }
        }

        xhttp.open("GET", back_url + "checkSession?session=" + session, true);
        xhttp.send();
    }
    else{
        show_buttons();
    }
}

autoLogin()
