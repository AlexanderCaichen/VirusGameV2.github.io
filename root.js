setInterval(randomBackground, 1000);

function randomBackground() {
	const randomColor = Math.floor(Math.random()*16777215).toString(16);
	document.body.style.backgroundColor = "#" + randomColor;
	document.getElementById("asdf").innerHTML = "<p>"+randomColor+"</p>";
}

// TODO: separate files for different functions eventually

window.addEventListener("DOMContentLoaded", () => {
	const websocket = new WebSocket("ws://localhost:8001/");
	receiveTable(websocket);
})

function receiveTable(websocket) {
	websocket.addEventListener("message", (data) => {
		document.getElementById("tableTest").innerHTML = data.data;
	})
}