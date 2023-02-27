// session cookie
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
function setSession(session = ""){
    // changes cookie if session or deletes it if no sesion
    if (session) document.cookie = "session=" + session + ";max-age=" + (60 * 60 * 24 * 100);
    else document.cookie = "session=no;max-age=0";
}

// workplace cookie
function getWorkplaceCookie(){
    // returns session from cookies, or null if not found
    let workplaceKey = "workplace=";
    let cookies = document.cookie;
    if (cookies.includes(workplaceKey)) {
      let startIndex = cookies.indexOf(workplaceKey) + workplaceKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let workplaceValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return workplaceValue || null;
    }
    return null;
}
function setWorkplaceCookie(workplace_id = ""){
    // changes cookie if workplace_id or deletes it if no workplace_id
    if (workplace_id) document.cookie = `workplace=${workplace_id}`;
    else document.cookie = "workplace=no;max-age=0";
}

// channel cookie
function getChannelCookie(){
    // returns session from cookies, or null if not found
    let channelKey = "channel=";
    let cookies = document.cookie;
    if (cookies.includes(channelKey)) {
      let startIndex = cookies.indexOf(channelKey) + channelKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let channelValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return channelValue || null;
    }
    return null;
}
function setChannelCookie(channel_id = ""){
    // changes cookie if channel_id or deletes it if no channel_id
    if (channel_id) document.cookie = `channel=${channel_id}`;
    else document.cookie = "channel=no;max-age=0";
}

// in chat cookie
function getInChatCookie(){
    // returns session from cookies, or null if not found
    let inChatKey = "inChat=";
    let cookies = document.cookie;
    if (cookies.includes(inChatKey)) {
      let startIndex = cookies.indexOf(inChatKey) + inChatKey.length;
      let endIndex = cookies.indexOf(";", startIndex);
      let inChatValue = (endIndex === -1) ? cookies.substring(startIndex) : cookies.substring(startIndex, endIndex);
      return inChatValue || null;
    }
    return null;
}
function setInChatCookie(inChat = false){
    // changes cookie if inChat or deletes it if not inChat
    if (inChat) document.cookie = `channel=${inChat}`;
    else document.cookie = "inChat=no;max-age=0";
}
