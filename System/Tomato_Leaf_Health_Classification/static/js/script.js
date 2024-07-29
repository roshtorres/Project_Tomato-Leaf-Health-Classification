const uploadedImage = document.getElementById("imgData");
const formOrigin = document.querySelector(".form-origin");
const fullName = document.getElementById("name");
const email = document.getElementById("email");
const subject = document.getElementById("subject");
const mess = document.getElementById("message");


/* ***********Contact*********** */

/* https://smtpjs.com/ */
function sendEmail() {
    const bodyMessage = `Full Name: ${fullName.value} <br> Email Address: ${email.value} <br> Message: <br> ${mess.value}`;

    Email.send({
        SecureToken: "ddcc23b2-2f4e-4f16-8a12-a4017d9c0efc",
        /* Host : "smtp.elasticemail.com",
           Username : "roshtorres.thesis@gmail.com", */
        Password: "7AF02415F2BE5C95C17CD4F0815317738DA9",
        To: 'roshtorres.thesis@gmail.com',
        From: "roshtorres.thesis@gmail.com",
        Subject: subject.value,
        Body: bodyMessage
    }).then(
        message => {
            if (message == "OK") {
                Swal.fire({
                    title: "Success!",
                    text: "Message sent successfully!",
                    icon: "success"
                });
            }
        }
    );
}

/* https://sweetalert2.github.io/ */
function checkInputs() {
    const items = document.querySelectorAll(".form-control");

    for (const item of items) {
        if (item.value == "") {
            item.classList.add("error");
            item.parentElement.classList.add("error");
        }

        if (items[1].value != "") {
            checkEmail();
        }

        items[1].addEventListener("keyup", () => {
            checkEmail();
        });

        item.addEventListener("keyup", () => {
            if (item.value != "") {
                item.classList.remove("error");
                item.parentElement.classList.remove("error");
            }
            else {
                item.classList.add("error");
                item.parentElement.classList.add("error");
            }
        });

    }
}

function checkEmail() {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    const errorTxtEmail = document.querySelector(".error-txt.email");

    if (!email.value.match(emailRegex)) {
        email.classList.add("error");
        email.parentElement.classList.add("error");

        if (email.value != "") {
            errorTxtEmail.innerText = "Enter a valid email address.";
        }
        else {
            errorTxtEmail.innerText = "Email Address can't be blank.";
        }
    }
    else {
        email.classList.remove("error");
        email.parentElement.classList.remove("error");
    }
}

formOrigin.addEventListener("submit", (e) => {
    e.preventDefault();
    checkInputs();

    if (!fullName.classList.contains("error") &&
        !email.classList.contains("error") &&
        !subject.classList.contains("error") &&
        !mess.classList.contains("error")) {
        sendEmail();

        formOrigin.reset();
        return false;
    }
});