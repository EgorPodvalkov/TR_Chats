// gets data from backend and displays it
function getWorkplaces(){
    // gets and displays workplaces
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
    // gets and displays channels
    if(getWorkplaceCookie() != workplaces_id){
        setWorkplaceCookie(workplaces_id);
        setChannelCookie();
    }
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
    // gets and displays chat
    setChannelCookie(channel_id)
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
            if(getInChatCookie()){
                let message_area = document.getElementById("message_text_area");
                message_area.focus();
            }
        }
    }
    xhttp.open("GET", `${back_url}getChat?channel_id=${channel_id}&workplace_id=${getWorkplaceCookie()}&session=${getSession()}`);
    xhttp.send();
}

// sends message
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
            getChat(getChannelCookie(), true)
            document.getElementById("message_text_area").value = "";


        }        
    }
    xhttp.open("GET", `${back_url}sendMessage?text=${text}&workplace_id=${getWorkplaceCookie()}&channel_id=${getChannelCookie()}&session=${getSession()}`)
    xhttp.send();
}

// scrolls chat if need
function scrollToBottom(){
    element = document.getElementsByClassName("messages")[0]
    element.scrollTop = element.scrollHeight
}

// sends messages on Enter button
document.addEventListener("keydown", function(event) {
    if (event.code === "Enter") {
      sendMessage();
    }
});
