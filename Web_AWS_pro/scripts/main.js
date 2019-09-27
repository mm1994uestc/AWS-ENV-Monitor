document.getElementById("emailinput").oninput = function() {function_emailinput()};
function function_emailinput()
{
	// alert("Some thing changed!");
	var emailin = document.getElementById("emailinput");
	emailin.style.backgroundColor = "#FFFFFF";
}

document.getElementById("passwdinput").oninput = function() {function_passwdinput()};
function function_passwdinput()
{
	// alert("Some thing changed!");
	var passwdin = document.getElementById("passwdinput");
	passwdin.style.backgroundColor = "#FFFFFF";
}

document.getElementById("sign-button").onclick = function() {function_signin_click()};
function function_signin_click()
{
	// alert("Sign IN.");
	var email_val = document.getElementById("emailinput").value;
	var passwd_val = document.getElementById("passwdinput").value;
	var info = "Email:"+email_val+ " Password:"+passwd_val;
	// alert(info);
	if(email_val === "547238541@qq.com" && passwd_val === "123456") {
		// alert(info);
		// window.open("./control.html")
		window.location.href="./control.html"
	}else {
		alert("Wrong Email or Password!");
	}
}