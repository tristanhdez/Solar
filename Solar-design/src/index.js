"use strict";
const btn = document.getElementById("btn");
const input = document.getElementById("userQuestion");
const messagesContainer = document.getElementById("messages");
let answer;
let count = 0;

var knowledge = {
    "hola":"¡Hola! Soy Solar, un gusto conocerte.",
    "comoestas":"Estoy contento de estar contigo",
    "reglamentodelaescuela": "En un momento te paso el reglamento de la escuela",
    "mitutor": "Tu tutor es:",
    "becas": "Las becas que puedes tomar son las siguientes",
    "convocatorias":"Las convocatorias se abren el próximo...",
    "talleres":"Los talleres existentes son...",
};

document.addEventListener("DOMContentLoaded", () => {
    input.addEventListener("keydown", (e) => {
      if (e.code === "Enter") {
        let question = input.value;
        input.value = "";
        talk(question);
      }
    });
});

//Selection if the user choose "others","Scholarship And Support", etc.
function selection(question){

}

function talk(question){
    let questionValue = question;
    question = question.normalize("NFD").toLowerCase()
    .replace(/\s+/g,"") //replace whitespaces.
    .replace(/[\u0300-\u036f]/g, "") //replace accents.
    .replace(/[!@#$%^&*?¿,.;:]/g,""); //replace invalid characters.

    if(question in knowledge){
        answer = knowledge[question];
        addToChat(questionValue, answer);
    }else{
        answer = "Lo siento, no te entendí";
        addToChat(question, answer);
    }
}

function addToChat(questionValue, answer){
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "response";
    userDiv.innerHTML = `<span>${questionValue}</span><img src="../static/images/icons/user_icon_fish.png" alt="Icon" height="50px" width="50px">`;
    messagesContainer.appendChild(userDiv);
    let botDiv = document.createElement("div");
    let botImg = document.createElement("img");
    let botText = document.createElement("span");
    botDiv.id = "bot";
    botImg.src = "../static/images/character/solar_icon.png";
    botImg.className = "avatar";
    botDiv.className = "bot response";
    botText.innerText = "Escribiendo...";
    botDiv.appendChild(botImg);
    botDiv.appendChild(botText);
    messagesContainer.appendChild(botDiv);
    // Keep messages at most recent
    messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;

    setTimeout(()=>{
        botText.innerText = `${answer}`;
    },200)
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
