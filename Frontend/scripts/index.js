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
        let chatName = document.getElementsByClassName("chat_name")[0];
        let status = document.getElementsByClassName("chat_status")[0];
        let mes = document.getElementsByClassName("messages")[0];
        chatName.innerHTML = "Channel Name"
        status.innerHTML = "Choose Channel to start chatting"
        mes.innerHTML = ""
        document.getElementsByClassName("send_area")[0].style = "display: none;";
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
            let status = document.getElementsByClassName("chat_status")[0];
            status.innerText = "Try to log in!";
            autoLogin();
            
        }
        else if(this.responseText == "No access"){
            let status = document.getElementsByClassName("chat_status")[0];
            status.innerText = "You haven`t access to this chat"
        }
        else{
            let chatName = document.getElementsByClassName("chat_name")[0];
            let newChatName = this.responseText.substring(0, this.responseText.indexOf("<>"));
            console.log(newChatName)
            let mes = document.getElementsByClassName("messages")[0];
            let newMes = this.responseText.substring(this.responseText.indexOf("<>") + 2);
            
            if (chatName.innerText != newChatName){
                chatName.innerText = newChatName;
                let status = document.getElementsByClassName("chat_status")[0];
                status.innerHTML = "";
                document.getElementsByClassName("send_area")[0].style = "display: inline;";
            }
            if(mes.innerHTML != newMes){
                console.log(newMes)
                let top
                top = mes.scrollTop;
                bottom = mes.scrollHeight - mes.scrollTop <= mes.clientHeight;
                console.log(`Top: ${top}\nscrollHeight: ${mes.scrollHeight}\nclientHeight: ${mes.clientHeight}`)

                if (newMes.startsWith(mes.innerHTML)){
                    mes.innerHTML += newMes.substring(mes.innerHTML.length);
                }
                else{
                    mes.innerHTML = newMes;
                }
                
                // document.getElementsByClassName("send_area")[0].style.display = "inline";
                // if(getInChatCookie()){
                //     let message_area = document.getElementById("message_text_area");
                //     message_area.focus();
                // } 


                // if(mes){
                //     mes = document.getElementsByClassName("messages")[0]
                //     mes.scrollTop = top 
                // }
                if (bottom){
                    scrollToBottom()
                }
            }
        }
    }
    xhttp.open("GET", `${back_url}getChat?channel_id=${channel_id}&workplace_id=${getWorkplaceCookie()}&session=${getSession()}`);
    xhttp.send();
}

// sends message
function sendMessage(){
    
    textElem = document.getElementById("message_text_area");
    text = textElem.value.trim();
    if (text == "") return
    textElem.innerHTML = "";
    
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            let status = document.getElementsByClassName("chat_status")[0];
            status.innerText = "Try to log in!";
            autoLogin()
        }
        else if(this.responseText == "No access"){
            let status = document.getElementsByClassName("chat_status")[0];
            status.innerText = "You haven`t access to this chat";
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
