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
	#???repVRate2: How many viruses replicate
	#cLifeSpan: how long it takes for your cell to die (life)
	#???cLifeSpan: how long it takes for your virus to die if not infect cell (see it as immune system naturally clearing foreign bodies???)
	#dmg: how much damage virus does to cell each replication
	def __init__(self, geneCount: int = 5, vMutRate: float = 0, cMutRate: float = 5, startingCells: int = 4, repCRate: int = 5, repVRate: int = 3, cLifeSpan: int = 15, lifeSpan: int = 15, dmg: int = 1):
		#TODO: Option to change string choice.
		self.origin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=geneCount))
		self.chance = vMutRate
		self.cooldown = cMutRate
		#startingCells
		self.crate = repCRate
		self.vrate = repVRate
		self.life = cLifeSpan
		self.dmg = dmg

		#TBA

		#Create starting Virus that can infect cell at >50% rate, infect cell
		#Use list due to datasize being small.

			#Add virus to Virus
			#Generate VirusTotal
			#Add cell to InfectCell


	#Perform 1 loop of simulation
	def forwardTime(self):
		self.Cells = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.Virus = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.InfectCell = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.CellTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.VirusTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))


	#Gives an array of infection chance (1xN) given two numpy arrays (1xN) each containing of genetic strings.
	def infectionChance(self, cellGene: str, virusGene:str) -> float:
		#https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array

		#IN DEVELOPMENT
		return 0.1


	#Update self.origin gene at position "index" with "newChar"
	def modifyGene(self, index: int, newChar: str):
		if (len(newChar) != 1):
			print("!!!REPORT THIS!!! Somehow obtained non-1 character input at once for modifyGene: " + newChar)
			return
		self.origin = self.origin[:index] + newChar + self.origin[index+1:]


