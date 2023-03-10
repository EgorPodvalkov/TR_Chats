const back_url = window.location.protocol + "//"+ window.location.hostname + ":8081/";
const front_url = window.location.protocol + "//" + window.location.hostname + ":8080/";

function getWorkplaceName(){
    let workplace_id = document.getElementById("id").innerText;
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad id"){
            goToMain();
        }
        else{
            let question = document.getElementById("question")
            question.innerHTML = `Do you want to join '${this.responseText}' workplace?`
        }
    } 

    xhttp.open("GET", `${back_url}getWorkplaceName?workplace_id=${workplace_id}`)
    xhttp.send();
}
function join(){
    let workplace_id = document.getElementById("id").innerText;
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(this.responseText == "Bad session code"){
            alert("You should be logged in your account🫤")
        }
        else {
            alert(this.responseText)
        }
        goToMain();
    } 

    xhttp.open("GET", `${back_url}joinWorkplace?workplace_id=${workplace_id}&session=${getSession()}`)
    xhttp.send();
}
function goToMain(){
    window.location.href = front_url;
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
getWorkplaceName();