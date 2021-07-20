function go_to_login() {
  window.location.href = "/login-new";
}
const messageDiv = document.getElementById("messages");

async function register() {
  messageDiv.innerHTML = "";
  const messagesArr = [];
  console.log("Register");
  if (
    document.getElementById("username").validity.valid &&
    document.getElementById("email").validity.valid &&
    document.getElementById("password").validity.valid
  ) {
    document.getElementById("loader").style.display = "block";
    const data = {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    };

    fetch("http://127.0.0.1:8000/auth/register/", {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.errors) {
          Object.entries(data.errors).forEach(([key, value]) => {
            console.log(`${key}: ${value}`);
            messagesArr.push(value);
          });
          document.getElementById("loader").style.display = "none";
          messagesArr.forEach((message) => {
            messageDiv.innerHTML += `<div>${message}</div>`;
          });
        } else if (data.data) {
          console.log(data);
          document.getElementById("loader").style.display = "none";
          document.getElementById("messages").innerHTML =
            "Successfully Registered. Verification Link Has Been Sent To Email.";
        }
      })
      .catch((error) => {
        document.getElementById("loader").style.display = "none";
        console.error(error);
      });
  } else {
    document.getElementById("loader").style.display = "none";
    document.getElementById("messages").innerHTML = "Invalid Email I Guess";
  }
}
