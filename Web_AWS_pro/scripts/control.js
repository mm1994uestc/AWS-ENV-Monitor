let myHeading = document.querySelector('h1');
myHeading.textContent = 'Hello world!';
alert('Wrong!');

function sum_func(num1, num2) {
	let result = num1 + num2;
	return result;
}

function setHeading(name) {
	let myHeading = document.querySelector('h1');
	myHeading.textContent = "Hello JS" + name + "!";
}

function setUserName() {
	let myName = prompt('Please enter your name:');
	localStorage.setItem('name',myName);
	setHeading(myName);
}

let storedName = localStorage.getItem('name');
if(!storedName) {
   setUserName();
} else {
   setHeading(storedName);
}

let myButton = document.querySelector('button'); 
myButton.onclick = setUserName;