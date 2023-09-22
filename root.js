// Set up connection to Websocket + send/receive behaviors
window.addEventListener("DOMContentLoaded", () => {
	const websocket = new WebSocket("ws://localhost:8001/");
	receiveTable(websocket);
})

function receiveTable(websocket) {
	websocket.addEventListener("message", (data) => {
		document.getElementById("tableTest").innerHTML = data.data;
	})
}

// Change screen
function Start() {

}

function Set() {

}

function Home() {

}

function Exit() {

}
