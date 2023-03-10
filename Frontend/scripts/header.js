let acc_panel_visible = false;

// shows buttons or user avatar
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

// shows or hides account panel(profile, settings, log out)s
function show_acc_panel(){
    if(acc_panel_visible){
        document.getElementsByClassName("acc_panel")[0].style = "display: none;";
        acc_panel_visible = false
    }
    else{
        document.getElementsByClassName("acc_panel")[0].style = "display: inline;";
        acc_panel_visible = true
    }
}
