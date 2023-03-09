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
