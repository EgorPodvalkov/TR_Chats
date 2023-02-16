function add_workplace(name = "New Workplace"){
    workplace = document.getElementsByClassName("workplaces_area")[0];
    workplace.innerHTML += "<button>" + name + "</button>";
}
add_workplace("Test")
function show_workplaces_adder(bool = true){
    if(bool){
        document.getElementsByClassName("adder_workplace")[0].style = "display: inline;"
    }
    else{
        document.getElementsByClassName("adder_workplace")[0].style = "display: none;"
    }
}
function scrollToBottom(){
    element = document.getElementsByClassName("messages")[0]
    element.scrollTop = element.scrollHeight
}

scrollToBottom()






// setTimeout(() => {location.reload()}, 1000)
