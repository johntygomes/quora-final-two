let googleAuthToken = "";
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  // console.log("ID:: ", profile.get_id());
  var id_token = googleUser.getAuthResponse().id_token;
  console.log("ID Token:: ", id_token);
  googleAuthToken = id_token;
  loginGoogle();
}
function loginGoogle() {
  console.log("google login called");
  let data = {
    auth_token: googleAuthToken,
  };
  fetch("http://127.0.0.1:8000/social-auth/google/", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // window.location.href = "/";
    })
    .catch((error) => {
      console.log(error);
    });
}
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log("User signed out.");
  });
  auth2.disconnect();
}

function onLoad() {
  gapi.load("auth2", function () {
    gapi.auth2.init();
  });
}

function logoutGoogle() {
  console.log("Logout Google called");
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log("User signed out.");
  });
  // document.location.href =
  // "https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8000/login-new";
  // "https://www.google.com/accounts/Logout?continue=http://localhost:8000/login-new";

  fetch("http://localhost:8000/social-auth/logout-google/", {})
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}
