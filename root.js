﻿// Set up connection to Websocket + send/receive behaviors
window.onload = Init;

var gameStart = false;
var count = 0;
var tick = 0;
var pause = false;

var primed = null;
var primeFunc = null;

// Variables for setting game initial states
var geneCount = 5
var vMutRate = 0.2
var cMutRate = 5 
var startingCells = 4
var repCRate = 5
var repVRate = 3
var vLifeSpan = 15
var lifeSpan = 10
var dmg = 1

//const websocket = new WebSocket("ws://localhost:8001/");
//https://stackoverflow.com/questions/34589488/es6-immediately-invoked-arrow-function
//Doesn't make sense to make defining "websocket" a separate function if the function won't be used ever again.
const websocket = new WebSocket((function() {
	console.log("Connecting to " + String(window.location.host) + "...");
	if (window.location.host === "alexandercaichen.github.io") {
		//Reminder that full link is "https://alexandercaichen.github.io/root.html"
		return "wss://virus-game-v2.fly.dev";
	} else if (window.location.pathname.slice(-9) == "root.html") {
		//For local testing purposes. 
		return "ws://localhost:8001/";
	} else {
		throw new Error("Unknown host: " + String(window.location.host));
	}
})());

window.addEventListener("DOMContentLoaded", () => {
	receiveMessage(websocket);
})

function receiveMessage(websocket) {
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
			case "table":
				if (gameStart) {
					document.getElementById(message.name).innerHTML = message.data;
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
		gameStart = false;
		//Send signal to stop game
		const event = {type: "starting", yes: false}; 
		websocket.send(JSON.stringify(event));
		tick = 0;
		count = 0;
		pause = false;
	}

	//Erase game interface
	document.getElementById("Game").innerHTML = "";

	//Create main menu interface
	document.getElementById("Interface").innerHTML = "<div class = \"centered\"><div id = \"menu\"><h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button></div></div>";
}

// Display Setting interface. Requires Init() to be called beforehand.
function Set() {
	let settings = "<h1> Settings </h1><br><br>";

	/*
	var varlist = [geneCount, vMutRate, cMutRate, startingCells, repCRate, repVRate, vLifeSpan, lifeSpan, dmg]
	for (var i in varlist) {
		settings += "<body><label for='" + Object.keys({i})[0] + "'>" + Object.keys({i}) + ": </label><input type='number' id='" + Object.keys({i})[0] + "' name='quantity' min='0' step='1' value='" + i.toString() + "'></body><br>"
	} */
	settings += "<body><label for='geneCount'>Length of Cell Gene: </label><input type='number' id='geneCount' name='quantity' min='0' step='1' value='" + geneCount + "'></body><br>";
	settings += "<body><label for='vMutRate'>Mutation rate of virus: </label><input type='number' id='vMutRate' name='quantity' min='0' step='0.1' value='" + vMutRate + "'></body><br>";
	settings += "<body><label for='cMutRate'>Cooldown to mutate cell: </label><input type='number' id='cMutRate' name='quantity' min='0' step='1' value='" + cMutRate + "'></body><br>";
	settings += "<body><label for='startingCells'>Number of starting cells: </label><input type='number' id='startingCells' name='quantity' min='0' step='1' value='" + startingCells + "'></body><br>";
	settings += "<body><label for='repCRate'>Time for cells to replicate: </label><input type='number' id='repCRate' name='quantity' min='0' step='1' value='" + repCRate + "'></body><br>";
	settings += "<body><label for='repVRate'>Time for virus to replicate: </label><input type='number' id='repVRate' name='quantity' min='0' step='1' value='" + repVRate + "'></body><br>";
	settings += "<body><label for='vLifeSpan'>How long viruses survive outside cells (UNIMPLEMENTED): </label><input type='number' id='vLifeSpan' name='quantity' min='0' step='1' value='" + vLifeSpan + "'></body><br>";
	settings += "<body><label for='lifeSpan'>How long cells live: </label><input type='number' id='lifeSpan' name='quantity' min='0' step='1' value='" + lifeSpan + "'></body><br>";
	settings += "<body><label for='dmg'>Amount of damage virus deals to cell upon replication: </label><input type='number' id='dmg' name='quantity' min='0' step='1' value='" + dmg + "'></body><br>";

	document.getElementById("menu").innerHTML = settings + "<button class=\"button\" onclick=\"saveAll();Home();\">Back</button>";
}


//Puts main menu interface in HTML. Requires Init() to be called beforehand.
function Home() {
	//Flex attempts to split Centered container into (number of elements) areas horizontally. div below "centered" prevents horizontal distribution/splitting
	document.getElementById("menu").innerHTML = "<h1> Virus Simulator </h1><button class=\"button\" onclick=\"StartGame()\">Start Game</button><br><button class=\"button\" onclick=\"Set()\">Settings</button>";
}

//Saves all settings
function saveAll() {
	geneCount = document.getElementById("geneCount").value;
	vMutRate = document.getElementById("vMutRate").value;
	cMutRate = document.getElementById("cMutRate").value;
	startingCells = document.getElementById("startingCells").value;
	repCRate = document.getElementById("repCRate").value;
	repVRate = document.getElementById("repVRate").value;
	vLifeSpan = document.getElementById("vLifeSpan").value;
	lifeSpan = document.getElementById("lifeSpan").value;
	dmg = document.getElementById("dmg").value;
}

// Display game interface
function StartGame() {
	End() //Clear screen and print "return" button

	document.getElementById("Game").innerHTML = "<div id = \"GameInterface\"><button id=\"Pause\" class=\"button\" style=\"width:150px\" onclick=\"Pause(true)\">Pause</button><div id=\"tick\"></div></div><div id = \"GameTable\"></div><div id = \"GameInterface2\"</div>";

	document.getElementById("GameTable").style.border = "1px limegreen solid";
	document.getElementById("GameTable").innerHTML = "<div class=\"row\"><div class=\"column\">Cells<div id = \"Cells\">TBA</div></div><div class=\"column\">Free Floating Viruses<div id = \"FreeVirus\">TBA</div></div><div class=\"column\">Infecting Viruses<div id = \"InVirus\">TBA</div></div><div class=\"column\">Cell Totals<div id = \"CellTotal\">TBA</div></div><div class=\"column\">Virus Totals<div id = \"VirusTotal\">TBA</div></div></div>";

	//Starting game
	const event = {type: "starting", yes: true, geneCount: geneCount, vMutRate: vMutRate, cMutRate: cMutRate, startingCells: startingCells, repCRate: repCRate, repVRate: repVRate, vLifeSpan: vLifeSpan, lifeSpan: lifeSpan, dmg: dmg};
	websocket.send(JSON.stringify(event));
}

// Interface when game ends
function End() {
	document.getElementById("Interface").innerHTML = "<button class=\"button\" style=\"width:150px; float:left\" onclick=\"Init()\">Return to Main Menu</button>";
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

