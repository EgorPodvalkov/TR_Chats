const front_url = window.location.protocol + "//" + window.location.hostname + ":8080/";
const back_url = window.location.protocol + "//"+ window.location.hostname + ":8081/";
document.cookie = "channel=no;max-age=0";

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



// add elems of blocks
function add_workplace(){
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
            getChannels(getCookieWorkplace())
        }
    }

    xhttp.open("GET", `${back_url}addChannel?name=${channel_name}&workplace_id=${getCookieWorkplace()}&session=${getSession()}`, true);
    xhttp.send();
   
}




// shows adders
function show_workplaces_adder(bool = true){
    if(bool && getSession() != null){
        document.getElementsByClassName("adder_workplace")[0].style = "display: inline;"
        document.getElementById("workplace_name").value = "";
        document.cookie = "inChat=no;max-age=0";
    }
    else{
        document.getElementsByClassName("adder_workplace")[0].style = "display: none;"
        document.cookie = "inChat=true"
    }
}

function show_channels_adder(bool = true){
    if(bool && getSession() != null){
        document.getElementsByClassName("adder_channel")[0].style = "display: inline;"
        document.getElementById("channel_name").value = "";
        let status = document.getElementById("copy_status");
        status.innerHTML = ""
        document.cookie = "inChat=no;max-age=0";
    }
    else{
        document.getElementsByClassName("adder_channel")[0].style = "display: none;"
        document.cookie = "inChat=true"
    }
}

// getting blocks
function getWorkplaces(){
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            let workplaces = document.getElementsByClassName("workplaces_area")[0]
            workplaces.innerHTML = "<button>Something wrong with your session code, try to login!</button>"
            autoLogin()
        }
        else{
            let workplaces = document.getElementsByClassName("workplaces_area")[0]
            workplaces.innerHTML = this.responseText
        }
    }

    xhttp.open("GET", back_url + "getWorkplaces?session=" + getSession());
    xhttp.send();
}

function getChannels(workplaces_id){
    document.cookie = `workplace=${workplaces_id}`
    document.cookie = `channel=no;max-age=0`
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            let workplaces = document.getElementsByClassName("channels")[0]
            workplaces.innerHTML = '<h3>Channels</h3><div class="channels_area"><button>Something wrong with your session code, try to login!</button></div>'
            autoLogin()
        }
        else if(this.responseText == "No access"){
            let workplaces = document.getElementsByClassName("channels")[0]
            workplaces.innerHTML = '<h3>Channels</h3><div class="channels_area"><button>Select workplace to see channels!</button></div>'
        }
        else{
            let workplaces = document.getElementsByClassName("channels")[0]
            workplaces.innerHTML = this.responseText
        }
    }

    xhttp.open("GET", `${back_url}getChannels?workplace_id=${workplaces_id}&session=${getSession()}`)
    xhttp.send();
    
}

function getChat(channel_id, bottom = false){
    document.cookie = `channel=${channel_id}`
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            let chat = document.getElementsByClassName("chat")[0]
            chat.innerHTML = "<h4>Try to log in!</h4>"
            autoLogin()
            
        }
        else if(this.responseText == "No access"){
            let chat = document.getElementsByClassName("chat")[0]
            chat.innerHTML = "<h4>You haven`t access to this chat🫤</h4>"
        }
        else{
            let mes = document.getElementsByClassName("messages")[0]
            let top
            if(mes) {
                top = mes.scrollTop;
                bottom = mes.scrollHeight - mes.scrollTop === mes.clientHeight;
            }
            
            let chat = document.getElementsByClassName("chat")[0]
            chat.innerHTML = this.responseText
            document.getElementsByClassName("send_area")[0].style.display = "inline";
            

            if(mes){
                mes = document.getElementsByClassName("messages")[0]
                mes.scrollTop = top 
            }
            if (bottom){
                scrollToBottom()
            }
            if(getCookieInChat()){
                let message_area = document.getElementById("message_text_area");
                message_area.focus();
            } 
        }
    }
    xhttp.open("GET", `${back_url}getChat?channel_id=${channel_id}&workplace_id=${getCookieWorkplace()}&session=${getSession()}`);
    xhttp.send();
}


function sendMessage(){
    text = document.getElementById("message_text_area").value;
    if (text == "") return

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            let chat = document.getElementsByClassName("chat")[0]
            chat.innerHTML = "<h4>Try to log in!</h4>"
            autoLogin()
        }
        else if(this.responseText == "No access"){
            let chat = document.getElementsByClassName("chat")[0]
            chat.innerHTML = "<h4>You haven`t access to this chat🫤</h4>"
        }
        else if(this.responseText == "Success"){
            getChat(getCookieChannel(), true)
            document.getElementById("message_text_area").value = "";


        }        
    }
    xhttp.open("GET", `${back_url}sendMessage?text=${text}&workplace_id=${getCookieWorkplace()}&channel_id=${getCookieChannel()}&session=${getSession()}`)
    xhttp.send();
}

function scrollToBottom(){
    element = document.getElementsByClassName("messages")[0]
    element.scrollTop = element.scrollHeight
}


function copyLink(){
    // gives user invite link

    let status = document.getElementById("copy_status");
    let link = `${front_url}joinWorkplace?workplace_id=${getCookieWorkplace()}`
    try{
        navigator.clipboard.writeText(link);
        status.innerHTML = "Copied!"
    }
    catch{
        status.style = "font-size: small;font-weight: 10;color: yellow;"
        status.innerHTML = "Your browser has prohibited copying, here is the link:<br>" + link;
    }
}

document.addEventListener("keydown", function(event) {
    if (event.code === "Enter") {
      sendMessage();
    }
});

function getSession(){
    // returns session from cookies, or null if not found
    let sessionKey = "session=";
    let cookies = document.cookie;
    if (cookies.includes(sessionKey)) {
      let startIndex = cookies.indexOf(sessionKey) + sessionKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let sessionValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return sessionValue || null;
    }
    return null;
}
function getCookieWorkplace(){
    // returns session from cookies, or null if not found
    let sessionKey = "workplace=";
    let cookies = document.cookie;
    if (cookies.includes(sessionKey)) {
      let startIndex = cookies.indexOf(sessionKey) + sessionKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let sessionValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return sessionValue || null;
    }
    return null;
}
function getCookieChannel(){
    // returns session from cookies, or null if not found
    let sessionKey = "channel=";
    let cookies = document.cookie;
    if (cookies.includes(sessionKey)) {
      let startIndex = cookies.indexOf(sessionKey) + sessionKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let sessionValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return sessionValue || null;
    }
    return null;
}
function getCookieInChat(){
    // returns session from cookies, or null if not found
    let sessionKey = "inChat=";
    let cookies = document.cookie;
    if (cookies.includes(sessionKey)) {
      let startIndex = cookies.indexOf(sessionKey) + sessionKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let sessionValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return sessionValue || null;
    }
    return null;
}

setInterval(() => {
    if(getCookieChannel()) getChat(getCookieChannel());
}, 400)
