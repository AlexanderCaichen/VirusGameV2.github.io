// Set up connection to Websocket + send/receive behaviors
window.onload = Init

window.addEventListener("DOMContentLoaded", () => {
	const websocket = new WebSocket("ws://localhost:8001/");
	receiveTable(websocket);
})

function receiveTable(websocket) {
	websocket.addEventListener("message", (data) => {
		document.getElementById("tableTest").innerHTML = data.data;
	})
}

//Called when need to go to main menu. 
function Init() {
	//Might take up more memory by not calling Home() but on the other hand will increase speed.
	document.getElementById("Interface").innerHTML = "<div class = \"centered\"><div id = \"menu\"><h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button></div></div>"
}

// Display Setting interface
function Set() {
	document.getElementById("menu").innerHTML = "<h1> Settings </h1><br><br><p style=\"color:white\">Nothing to see here for now</p><button class=\"button\" onclick=\"Home()\">Back</button>"
}

function Home() {
	//Flex attempts to split Centered container into (number of elements) areas horizontally. div below "centered" prevents horizontal distribution/splitting
	document.getElementById("menu").innerHTML = "<h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button>"
}

// Display game interface
function StartGame() {
	//document.getElementById("Interface").innerHTML = 
	End()
}

// Interface when game ends
function End() {
	document.getElementById("Interface").innerHTML = "<button class=\"button\" onclick=\"Init()\">Return to Main Menu</button>"
}
