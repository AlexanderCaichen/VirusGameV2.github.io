// Set up connection to Websocket + send/receive behaviors
window.onload = Init

var gameStart = false
var count = 0

const websocket = new WebSocket("ws://localhost:8001/");

window.addEventListener("DOMContentLoaded", () => {
	receiveTable(websocket);
})

function receiveTable(websocket) {
	websocket.addEventListener("message", ({data}) => {
		if (gameStart) {
			try {
				//document.getElementById("tableTest").innerHTML = data.data; <= (data)
				const message = JSON.parse(data);
				document.getElementById(message.type).innerHTML = message.table;
			} catch (e) {
				console.log("Message '" + String(data) + "' is not in accepted format (Cannot be parsed)");
			}
			count++;
			//Send "Continue" every 5 table updates or else message queue will be backed up
			if (count == 5) {
				//console.log("continue")
				const event = {type: "continue", num: count}; 
				websocket.send(JSON.stringify(event));
				count = 0;
			}
		}
	})
}

//Called when need to go to main menu. 
function Init() {
	//Might take up more memory by not calling Home() but on the other hand will increase speed.

	//Stop game from running if a game has already started.
	if (gameStart) {
		const event = {type: "starting", value: false}; 
		websocket.send(JSON.stringify(event));
	}
	gameStart = false;
	console.log("stop")

	//TODO: Send signal for handler to stop simulation if gameStart=True
	document.getElementById("Game").innerHTML = ""
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
	End() //Clear screen and print "return" button

	//Starting game
	gameStart = true;
	const event = {type: "starting", value: true};
	websocket.send(JSON.stringify(event));
	const event2 = {type: "continue"}; 
	websocket.send(JSON.stringify(event2));


	document.getElementById("Game").innerHTML = "<div class=\"row\"><div class=\"column\" id = \"Cells\"></div><div class=\"column\" id = \"Virus\"></div><div class=\"column\" id = \"InfectCell\"></div><div class=\"column\" id = \"CellTotal\"></div><div class=\"column\" id = \"VirusTotal\"></div></div>"
}

// Interface when game ends
function End() {
	document.getElementById("Interface").innerHTML = "<button class=\"button\" style=\"width:150px\" onclick=\"Init()\">Return to Main Menu</button>"
}
