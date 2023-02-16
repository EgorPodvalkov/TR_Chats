function addSomeThingToWorkplaces(){
    workplace = document.getElementsByClassName("workplaces_area")[0];
    workplace.innerHTML += "<button>new workplace</button>"
}
addSomeThingToWorkplaces()

function show_workplaces_adder(bool = true){
    if(bool){
        document.getElementsByClassName("adder_workplace")[0].style = "display: inline;"
    }
    else{
        document.getElementsByClassName("adder_workplace")[0].style = "display: none;"
    }
}









// setTimeout(() => {location.reload()}, 1000)
