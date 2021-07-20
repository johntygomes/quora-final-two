function go_to_register() {
  window.location.href = "/register-new";
}

const messageDiv_2 = document.getElementById("messages");

async function login() {
  console.log("Login");
  if (
    document.getElementById("email").validity.valid &&
    document.getElementById("password").validity.valid
  ) {
    document.getElementById("loader").style.display = "block";
    const data = {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    };

    fetch("http://127.0.0.1:8000/auth/login/", {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.detail === "email not verified") {
          document.getElementById("loader").style.display = "none";
          document.getElementById("messages").innerHTML = "email not verified";
        } else if (data.detail === "Invalid Credentials Try Again") {
          document.getElementById("loader").style.display = "none";
          document.getElementById("messages").innerHTML =
            "Invalid Credentials Try Again";
        } else if (data.password) {
          if (
            data.password[0] ===
            "Ensure password field has at least 6 characters."
          ) {
            document.getElementById("loader").style.display = "none";
            document.getElementById("messages").innerHTML =
              "Ensure password field has at least 6 characters.";
          }
        } else {
          document.getElementById("loader").style.display = "none";
          document.getElementById("messages").innerHTML =
            "Successfully Logged In";
          localStorage.setItem("token_access", data.tokens.access);
          localStorage.setItem("token_refresh", data.tokens.refresh);
          window.location.href = "/";
        }
      })
      .catch((error) => {
        document.getElementById("loader").style.display = "none";
        console.error(error);
      });
  } else {
    document.getElementById("loader").style.display = "none";
    document.getElementById("messages").innerHTML = "Invalid Email I guess";
  }
}
