#!/usr/bin/env python

# Most of the base infrastructure is based on this tutorial:
#  https://websockets.readthedocs.io/en/stable/intro/tutorial1.html

#Temporary. Will be removed when Game logic stuff is complete.
import pandas as pd 
import numpy as np

#Handles game logic
from simulation import Game

import asyncio

import websockets

import json

#For checking python version
import sys
#verification or else certain code (match) won't work.
assert sys.version_info >= (3, 10)

#For deploying to Heroku
import os
import signal

async def handler(websocket):
	#message = await websocket.recv()
	async for message in websocket:
		try:
			event = json.loads(message)

			#Start game and begin simulation
			if (event["type"] == "starting" and event["yes"]):
				game = Game()
				event = {
					"type": "baseGenome",
					"data": game.origin
				}

				await websocket.send(json.dumps(event))
				await tablePrint(websocket, game)
		except json.JSONDecodeError as e:
			print("Invalid JSON format: " + message)

#TODO: create new connection in case `except websockets.ConnectionClosedOK:`
async def tablePrint(websocket, game):
	print("printing stuff")
	paused = False

	#Requiring a "confirmation message" from root.js allows more synchronization between the cloud and server.
	async for message in websocket:
		try:
			event = json.loads(message)
		except json.JSONDecodeError as e:
			print("Invalid JSON format: " + message)
			continue
		#TODO: try event[type] or check to see if type even exists
		
		match event["type"]:
			case "starting":
				if not event["yes"]:
					break
			case "continue":
				#Reminder that ~False = -1 and ~True = -2
				for i in ["Cells", "Virus", "InfectCell", "CellTotal", "VirusTotal"]:
					event = {
						"type": i,
						"table": pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD')).head(10).to_html()
					}
					await websocket.send(json.dumps(event))
					#await websocket.send("string thing")
				await asyncio.sleep(1)
			case "keyMod":
				game.modifyGene(event["index"], event["newChar"])
				print(game.origin)
			case "pause":
				paused = event["yes"]
			case _:
				print(event)

	print("Exiting game")

async def main():
	print("Starting...")
	# Set the stop condition when receiving SIGTERM.
	loop = asyncio.get_running_loop()
	stop = loop.create_future()
	loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

	port = int(os.environ.get("PORT", "8001"))
	async with websockets.serve(handler, "", port):
		await stop  # run forever

if __name__ == '__main__':
	asyncio.run(main())
