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
		try {
			//document.getElementById("tableTest").innerHTML = data.data; <= (data)
			var message = JSON.parse(data);
		} catch (e) {
			console.log("Message '" + String(data) + "' is not in accepted format (Cannot be parsed)");
		}

		if (gameStart) {
			document.getElementById(message.type).innerHTML = message.table;
			count++;
			//Send "Continue" every 5 table updates or else message queue will be backed up
			if (count == 5) {
				//console.log("continue")
				const event = {type: "continue", num: count}; 
				websocket.send(JSON.stringify(event));
				count = 0;
			}
		} else if (message["type"] == "baseGenome") {
			//Setting up buttons
			//So I don't need to constantly call "getElementById" in for loop
			let tempRef = document.getElementById("GameInterface2");
			tempRef.innerHTML = "<br><h4>Base Cell Genome</h4><p>Click then press keyboard to change character in slot</p>"
			let gene = message.data;
			let length = gene.length;
			for (let i = 0; i < length; i++) {
				tempRef.innerHTML += "<button id=\"tbu" + String(i) + "\" onclick=\"Primed(" + String(i) + ")\">" + gene.charAt(i) + "</button>"
			}

			const event2 = {type: "continue"}; 
			websocket.send(JSON.stringify(event2));
			gameStart = true;
		} else {
			console.log(message);
		}
	})
}

//Called when need to go to main menu. 
function Init() {
	//Might take up more memory by not calling Home() but on the other hand will increase speed.

	//Stop game from running if a game has already started.
	if (gameStart) {
		//Send signal to stop game
		const event = {type: "starting", yes: false}; 
		websocket.send(JSON.stringify(event));
		//Erase game interface
		document.getElementById("Game").innerHTML = "<div id = \"GameInterface\"></div><div id = \"GameTable\"></div><div id = \"GameInterface2\"</div>"
		gameStart = false;
	}

	//
	document.getElementById("Interface").innerHTML = "<div class = \"centered\"><div id = \"menu\"><h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button></div></div>"
}

// Display Setting interface. Requires Init() to be called beforehand.
function Set() {
	document.getElementById("menu").innerHTML = "<h1> Settings </h1><br><br><p style=\"color:white\">Nothing to see here for now</p><button class=\"button\" onclick=\"Home()\">Back</button>"
}


//Puts main menu interface in HTML. Requires Init() to be called beforehand.
function Home() {
	//Flex attempts to split Centered container into (number of elements) areas horizontally. div below "centered" prevents horizontal distribution/splitting
	document.getElementById("menu").innerHTML = "<h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button>"
}

// Display game interface
function StartGame() {
	End() //Clear screen and print "return" button
	document.getElementById("GameTable").style.border = "1px limegreen solid";
	document.getElementById("GameTable").innerHTML = "<div class=\"row\"><div class=\"column\" id = \"Cells\">TBA</div><div class=\"column\" id = \"Virus\">TBA</div><div class=\"column\" id = \"InfectCell\">TBA</div><div class=\"column\" id = \"CellTotal\">TBA</div><div class=\"column\" id = \"VirusTotal\">TBA</div></div>"


	//Starting game
	const event = {type: "starting", yes: true};
	websocket.send(JSON.stringify(event));
}

// Interface when game ends
function End() {
	document.getElementById("Interface").innerHTML = "<button class=\"button\" style=\"width:150px\" onclick=\"Init()\">Return to Main Menu</button>"
}

function Primed(index) {
	let a = 123;
}

