avatar_visible = false
acc_panel_visible = false

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



setTimeout(() => {location.reload()}, 1000)