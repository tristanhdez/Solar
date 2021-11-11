function sendEmail(){
    Email.send({
        Host : "smtp.gmail.com",
        Username : "soyelbotsolar@gmail.com",
        Password : "djyxcblyscuuiiki",
        To : 'soyelbotsolar@gmail.com',
        From : "soyelbotsolar@gmail.com",
        Subject : "This is the subject",
        Body : "And this is the body"
    }).then(
      message => alert(message)
    );
}
