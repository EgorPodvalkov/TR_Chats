// shows adders
function show_workplaces_adder(bool = true){
    // shows workplace adder
    if(bool && getSession() != null){
        document.getElementsByClassName("adder_workplace")[0].style = "display: inline;"
        document.getElementById("workplace_name").value = "";
        setInChatCookie();
        document.getElementById("workplace_name").focus();
    }
    else{
        document.getElementsByClassName("adder_workplace")[0].style = "display: none;"
        setInChatCookie("true");
    }
}
function show_channels_adder(bool = true){
    // shows channel adder
    if(bool && getSession() != null){
        document.getElementsByClassName("adder_channel")[0].style = "display: inline;"
        document.getElementById("channel_name").value = "";
        let status = document.getElementById("copy_status");
        status.innerHTML = ""
        setInChatCookie();
        document.getElementById("channel_name").focus();
    }
    else{
        document.getElementsByClassName("adder_channel")[0].style = "display: none;"
        setInChatCookie("true");
    }
}

// adds elem from panels
function add_workplace(){
    // adds workplace
    let workplace_name = document.getElementById("workplace_name").value;
    clearErrorsAndStatuses();

    // empty workplace_name
    if (workplace_name == ""){
        let err = document.getElementById("workplace_name_err")
        err.innerHTML = "Workplace name can`t be empty!"
        return
    }
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if(this.responseText == "Bad session code"){
            let err = document.getElementById("workplace_name_err")
            err.innerHTML = "Something wrong with your session code, try to login!"
            autoLogin()
        }
        else if(this.responseText == "Workplace name is already taken"){
            let err = document.getElementById("workplace_name_err")
            err.innerHTML = "Workplace name is already taken!"
        }
        else if(this.responseText == "Added"){
            show_workplaces_adder(false)
            getWorkplaces()
        }
    }

    xhttp.open("GET", back_url + "addWorkplace?name=" + workplace_name + "&session=" + getSession(), true);
    xhttp.send();
}
function add_channel(){
    // adds channel
    let channel_name = document.getElementById("channel_name").value;
    clearErrorsAndStatuses();

    // empty channel_name
    if (channel_name == ""){
        let err = document.getElementById("channel_name_err")
        err.innerHTML = "Channel name can`t be empty!"
        return
    }
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if(this.responseText == "Bad session code"){
            let err = document.getElementById("workplace_name_err")
            err.innerHTML = "Something wrong with your session code, try to login!"
            autoLogin()
        }
        else if(this.responseText == "Workplace name is already taken"){
            let err = document.getElementById("workplace_name_err")
            err.innerHTML = "Workplace name is already taken!"
        }
        else if(this.responseText == "Added"){
            show_channels_adder(false)
            getChannels(getWorkplaceCookie())
        }
    }

    xhttp.open("GET", `${back_url}addChannel?name=${channel_name}&workplace_id=${getWorkplaceCookie()}&session=${getSession()}`, true);
    xhttp.send();
   
}

// gives user invite link
function copyLink(){

    let status = document.getElementById("copy_status");
    let link = `${front_url}joinWorkplace?workplace_id=${getWorkplaceCookie()}`
    try{
        navigator.clipboard.writeText(link);
        status.innerHTML = "Copied!"
    }
    catch{
        status.style = "font-size: small;font-weight: 10;color: yellow;"
        status.innerHTML = "Your browser has prohibited copying, here is the link:<br>" + link;
    }
}
