setChannelCookie();
autoLogin();

// chat update
setInterval(() => {
    if(getChannelCookie()) getChat(getChannelCookie());
}, 400)

// channels update
setInterval(() => {
    if(getWorkplaceCookie()) getChannels(getWorkplaceCookie());
}, 10000)

// sends messages on Enter button
document.addEventListener("keydown", function(event) {
    if (event.code === "Enter") {
      sendMessage();
    }
});

// manages showing and hiding of bottom button
document.getElementsByClassName("messages")[0].addEventListener('scroll', function() {
    let mes = document.getElementsByClassName("messages")[0];
    // if on bottom
    if (mes.scrollHeight - mes.scrollTop <= mes.clientHeight) {
        document.getElementById("to_bottom_button").style.display = "none";
    }
    else{
        document.getElementById("to_bottom_button").style.display = "inline";
    }
});