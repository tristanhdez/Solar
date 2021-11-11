"use strict";
const input = document.getElementById("userQuestion");
function getResponse(data, normalData) {
    const messagesContainer = document.getElementById("messages");
    //let userText = $("#userQuestion").val();
    let userText = data;
    console.log(userText);
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "response";
    userDiv.innerHTML = `<span>${normalData}</span><img src="../static/images/icons/user_icon_fish.png" alt="Icon" height="50px" width="50px">`;
    messagesContainer.appendChild(userDiv);
    let botDiv = document.createElement("div");
    let botImg = document.createElement("img");
    let botText = document.createElement("span");
    messagesContainer.appendChild(botDiv);
    // Keep messages at most recent
    messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
    $.get("/get", { msg: userText }).done(function(data){
        botDiv.id = "bot";
        botImg.src = "../static/images/character/solar_icon.png";
        botImg.className = "avatar";
        botDiv.className = "bot response";
        botText.innerText = "Escribiendo...";
        botDiv.appendChild(botImg);
        botDiv.appendChild(botText);
        setTimeout(()=>{
        botText.innerText = `${data}`;
    },500)
    });
}

$("#userQuestion").keypress(function(e) {
//if enter key is pressed
    if(e.which == 13) {
        let value = $("#userQuestion").val();
        if(!value || /^\s*$/.test(value))
            return;
        talk(value)
        input.value = "";
    }
});

$("#btns").click(function(){
    let value = $("#userQuestion").val();
    if(!value || /^\s*$/.test(value))
        return;
    talk(value);
    input.value = "";
});


function talk(value){
    let data = value;
    let normalData = value;
    data = data.normalize("NFD").toLowerCase()
    .replace(/\s+/g,"") //replace whitespaces.
    .replace(/[\u0300-\u036f]/g, "") //replace accents.
    .replace(/[!@#$%^&*?¿,.;:]/g,""); //replace invalid characters.
    /*if(question in knowledge){
        answer = knowledge[question];
        addToChat(questionValue, answer);
    }else{
        answer = "Lo siento, no te entendí";
        addToChat(question, answer);
    }*/
    console.log(data, normalData);
    getResponse(data, normalData);
}

//Change theme
document.getElementById('buttonID').onclick = function () {
    if(count==0){
    document.getElementById('theme_css').href = '../static/css/index_dark.css';
    count++;
    }else{
        document.getElementById('theme_css').href = '../static/css/index.css';
        count--;
    }
};
