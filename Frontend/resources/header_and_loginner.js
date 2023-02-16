avatar_visible = false;
acc_panel_visible = false;

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
}
function show_email_verif(){
    //shows email verif fields and hides telegram verif fields
    document.getElementsByClassName("email_sign_up")[0].style = "display: inline;";
    document.getElementsByClassName("telegram_sign_up")[0].style = "display: none;";
}
