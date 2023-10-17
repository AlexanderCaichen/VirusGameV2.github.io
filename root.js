// Set up connection to Websocket + send/receive behaviors
window.onload = Init;

var gameStart = false;
var count = 0;
var tick = 0;
var pause = false;
var primed = null;
var primeFunc = null;

//const websocket = new WebSocket("ws://localhost:8001/");
//https://stackoverflow.com/questions/34589488/es6-immediately-invoked-arrow-function
//Doesn't make sense to make defining "websocket" a separate function if the function won't be used ever again.
const websocket = new WebSocket((function() {
	console.log("Connecting to " + String(window.location.host) + "...");
	if (window.location.host == "alexandercaichen.github.io") {
		//Reminder that full link is "https://alexandercaichen.github.io/root.html"
		return "wss://virus-game-v2.fly.dev";
	} else if (window.location.pathname.slice(-9) == "root.html") {
		//For local testing purposes. 
		return "ws://localhost:8001/";
	} else {
		throw new Error("Unknown host: " + String(window.location.host));
	}
	console.log("Success");
})());

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

		switch (message["type"]) {
			case "baseGenome":
				//Setup for baseGenome display at bottom of screen.
				//Display for buttons.
				//So I don't need to constantly call "getElementById" in for loop
				let tempRef = document.getElementById("GameInterface2");
				tempRef.innerHTML = "<br><h3>Base Cell Genome</h4><p>Click a slot then press keyboard to change the character in slot</p>";
				let gene = message.data;
				let length = gene.length;
				for (let i = 0; i < length; i++) {
					//"onclick" instead of "onmouseup" allows Primed() to be called as long as mouse is held down. In other words, color changes after mouse is lifted but while it is pushed down one can type as many letters as they like.
					tempRef.innerHTML += "<button id=\"tbu" + String(i) + "\" onmouseup=\"Primed(" + String(i) + ")\">" + gene.charAt(i) + "</button>";
				}

				const event = {type: "continue"}; 
				websocket.send(JSON.stringify(event));
				gameStart = true;
				break;
			case "Cells":
			case "Virus":
			case "InfectCell":
			case "CellTotal":
			case "VirusTotal":
				if (gameStart) {
					document.getElementById(message.type).innerHTML = message.table;
					count++;
					//Send "Continue" every 5 table updates or else message queue will be backed up
					if (count >= 5) {
						//console.log("continue")
						if (!pause) {
							const event = {type: "continue", num: count}; 
							websocket.send(JSON.stringify(event));
						}
						count = 0;

						document.getElementById("tick").innerHTML = "<h2>Tick " + String(tick) + "</h2>";
						tick++;
					}
				} else {
					console.log("Game already ended (this probably happened because game was ended before table data were received from latest tick)")
				}
				break;
			default:
				console.log("Unknown message: " + message);
		}
	})
}

//############################
//HTML
//############################

//Called when need to go to main menu. 
function Init() {
	//Might take up more memory by not calling Home() but on the other hand will increase speed.

	//Stop game from running if a game has already started.
	if (gameStart) {
		//Send signal to stop game
		const event = {type: "starting", yes: false}; 
		websocket.send(JSON.stringify(event));
		tick = 0;
		count = 0;
		pause = false;
		gameStart = false;
	}

	//Erase game interface
	document.getElementById("Game").innerHTML = "";

	//Create main menu interface
	document.getElementById("Interface").innerHTML = "<div class = \"centered\"><div id = \"menu\"><h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button></div></div>";
}

// Display Setting interface. Requires Init() to be called beforehand.
function Set() {
	document.getElementById("menu").innerHTML = "<h1> Settings </h1><br><br><p style=\"color:white\">Nothing to see here for now</p><button class=\"button\" onclick=\"Home()\">Back</button>";
}


//Puts main menu interface in HTML. Requires Init() to be called beforehand.
function Home() {
	//Flex attempts to split Centered container into (number of elements) areas horizontally. div below "centered" prevents horizontal distribution/splitting
	document.getElementById("menu").innerHTML = "<h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button>";
}

// Display game interface
function StartGame() {
	End() //Clear screen and print "return" button

	document.getElementById("Game").innerHTML = "<div id = \"GameInterface\"><button id=\"Pause\" class=\"button\" style=\"width:150px\" onclick=\"Pause(true)\">Pause</button><div id=\"tick\"></div></div><div id = \"GameTable\"></div><div id = \"GameInterface2\"</div>";

	document.getElementById("GameTable").style.border = "1px limegreen solid";
	document.getElementById("GameTable").innerHTML = "<div class=\"row\"><div class=\"column\" id = \"Cells\">TBA</div><div class=\"column\" id = \"Virus\">TBA</div><div class=\"column\" id = \"InfectCell\">TBA</div><div class=\"column\" id = \"CellTotal\">TBA</div><div class=\"column\" id = \"VirusTotal\">TBA</div></div>";


	//Starting game
	const event = {type: "starting", yes: true};
	websocket.send(JSON.stringify(event));
}

// Interface when game ends
function End() {
	document.getElementById("Interface").innerHTML = "<button class=\"button\" style=\"width:150px\" onclick=\"Init()\">Return to Main Menu</button>";
}

//############################
//FUNCTIONALITIES 
//############################

//Changes button behavior to accept keyboard inputs.
function Primed(index) {
	//reset any buttons that were primed but not set
	if (primed) {
		primed.style = "";
		primed.removeEventListener("keypress", primeFunc);
		//console.log("reset")
	}
	
	const tempRef = document.getElementById("tbu" + String(index));
	tempRef.style = "color:yellow; background:red";

	primeFunc = (event) => {SetKey(event, index)};
	tempRef.addEventListener("keypress", primeFunc);
	primed = tempRef;
	//console.log("primed" + String(index));
}

function SetKey(event, index) {
	const tempRef = document.getElementById("tbu" + String(index));
	// TODO: Verify if pressed key is valid choice.\
	tempRef.innerHTML = event.key;
	websocket.send(JSON.stringify({type: "keyMod", index: index, newChar: event.key}));
	tempRef.style = "";
	tempRef.removeEventListener("keypress", primeFunc);
	/*
	//For bug where mouse and key click are in quick succession of each other (in that order):
	//Previous primed button does not reset color because code here is called first and sets "primed" to -999, so when Primed() runs next the color reset does not occur. 
	if (primed) {
		primed.style = "";
		primed.removeEventListener("keypress", event => SetKey(event, primed));
		console.log("reset" + String(primed))
	}*/
	primed = null;
	// console.log("remove" + String(index));
}

function Pause(truth) {
	//Pausing game
	pause = truth
	const event = {type: "pause", yes: truth};
	websocket.send(JSON.stringify(event));

	//Create a different id?
	const tempPointer = document.getElementById("Pause");
	tempPointer.onclick = function() { Pause(!truth) };
	if (truth) {
		tempPointer.innerHTML = "Unpause";
		tempPointer.style = "width:150px; color:yellow; background:red"
	} else {
		tempPointer.innerHTML = "Pause";
		tempPointer.style = "width:150px";

		websocket.send(JSON.stringify({type: "continue", num: count}));
	}
}

