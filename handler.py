#!/usr/bin/env python

#https://stackoverflow.com/questions/13175510/call-python-function-from-javascript-code
#^ Suggests to use NODE.js child processes that run python or a server to run python

# PyNode is also an option that allows python calls in JS
# PyNode might not work well with timing (since this is a simulation, asynchronous updating is desired)
# PyNode also won't work because we want python to continuously update to JS

#Decision: use server to run python code and POST to JS for data updates

# Issue: Python code needs to continue running simulation even if GET from JS
#  So: JS should call python code once and python code continuously POSTS to JS to print in HTML
# Solution: WebSocket to enable realtime communication without HTTP request/response

# Most of the base infrastructure is based on this tutorial:
#  https://websockets.readthedocs.io/en/stable/intro/tutorial1.html

# TBA: Deploy websocket server to Kubernetes or similar service.

import pandas as pd 
import numpy as np

import asyncio

import websockets

import json

import sys
#verification or else certain code (match) won't work.
assert sys.version_info >= (3, 10)

from simulation import Game

async def handler(websocket):
	#message = await websocket.recv()
	async for message in websocket:
		try:
			event = json.loads(message)

			if (event["type"] == "starting" and event["yes"]):
				game = Game()
				event = {
					"type": "baseGenome",
					"data": game.origin
				}
				print(game.origin)
				await websocket.send(json.dumps(event))
				await tablePrint(websocket, game)
		except json.JSONDecodeError as e:
			print("Invalid JSON format: " + message)

#TODO: create new connection in case `except websockets.ConnectionClosedOK:`
async def tablePrint(websocket, game):
	print("printing stuff")

	#Requiring a "confirmation message" from root.js allows more synchronization between the cloud and server.
	async for message in websocket:
		#print(message)
		try:
			event = json.loads(message)
		except json.JSONDecodeError as e:
			print("Invalid JSON format: " + message)
			continue
		#TODO: try event[type] or check to see if type even exists
		
		match event["type"]:
			case "starting":
				if ~event["yes"]:
					break
			case "continue":
				for i in ["Cells", "Virus", "InfectCell", "CellTotal", "VirusTotal"]:
					event = {
						"type": i,
						"table": pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD')).head(10).to_html()
					}
					await websocket.send(json.dumps(event))
					#await websocket.send("string thing")
			case _:
				print("TBA")

	print("Exiting game")

async def main():
	print("Starting...")
	async with websockets.serve(handler, "", 8001):
		await asyncio.Future()  # run forever

if __name__ == '__main__':
	asyncio.run(main())
