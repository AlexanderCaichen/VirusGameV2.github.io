#!/usr/bin/env python

#For handling game logic

import pandas as pd 
import numpy as np

import string
import random

#GAME IS WON WHEN VIRUSES CAN'T INFECT CELLS (For set amount of time?)
#Virus gets killed if not infect? 
#Virus factory mode (infected cells, if divide, can make new viruses)

class Game:

	Cells = pd.DataFrame(columns=["Gene", "Next Replication", "Life", "InfectedBy"])
	Virus = pd.DataFrame(columns=["Gene", "Next Infection Chance"])
	InfectCell = pd.DataFrame(columns=["Gene", "Cell Infected"])
	CellTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Alive"])
	VirusTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Existing"])

	#Game setup
	#geneCount: length of gene
	#vMutRate: chance of each virus gene to mutate when replicating
	#cMutRate: time it takes to change a genome (cooldown)
	#startingCells: number of cells you start with
	#repCRate: time it takes for each of your cells to replicate
	#repVRate: time it takes for each virus to replicate after infecting cell
	#repVRate2: How many viruses replicate
	#lifeSpan: how long it takes for your cell to die (life)
	#dmg: how much damage virus does to cell each replication
	def __init__(self, geneCount: int = 5, vMutRate: float = 0, cMutRate: float = 5, startingCells = 4, repCRate = 5, repVRate = 3, cLifeSpan = 15, lifeSpan = 15, dmg = 1):
		#TODO: Option to change string choice.
		self.origin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=geneCount))
		self.chance = vMutRate
		self.cooldown = cMutRate
		#startingCells
		self.crate = repCRate
		self.vrate = repVRate
		self.life = cLifeSpan
		self.dmg = dmg

		#Create startingCells cells, fill in Cells dataframe
		#Create starting Virus that can infect cell at >50% rate, infect cell
			#Add virus to Virus
			#Generate VirusTotal
			#Add cell to InfectCell




