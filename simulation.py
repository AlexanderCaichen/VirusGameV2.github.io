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
		self.chance = vMutRate
		self.cooldown = cMutRate
		#startingCells
		self.crate = repCRate
		self.vrate = repVRate
		self.life = cLifeSpan
		self.dmg = dmg


		#initializing instance variables (placed inside in case character options change between games)
		self.characterDict = dict()
		for i in string.ascii_lowercase + string.digits:
			self.characterDict[i] = len(self.characterDict)

		#Note that modifying class variables (not instance variables) will also modify other instances of class
		self.Cells = pd.DataFrame(columns=["Gene", "Next Replication", "Life", "InfectedBy", "numbers"])
		#Free viruses
		self.FreeVirus = pd.DataFrame(columns=["Gene", "numbers"])
		#Summary stats of cells being infected. Add "InfectedBy"?
		self.InfectCell = pd.DataFrame(columns=["Gene", "Num Cell Infected", "numbers"])
		self.CellTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Alive"])
		self.VirusTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Existing"])
		#      Need row for total stats

		
		#Create startingCells cells, fill in Cells dataframe
		#TODO: Option to change string choice.
		numbersC = random.choices(string.ascii_lowercase + string.digits, k=geneCount)
		self.origin = ''.join(numbersC)
		#numbers = np.array(list(map(ord, numbers)))
		numbersC = np.array([self.characterDict.get(value, value) for value in numbersC])
		print("Starting genome: " + self.origin)



		#Create starting Virus that can infect cell at >50% rate, infect cell

		#For summary statistics (can delete)
		loops = 0
		summer = 0

		#When cellGene is randomized average chance (summer) is usually ~0.7. Need to make infection rate lower or make bounds more narrow
		#Note: lowest infection AVERAGE given thousands of attempts is ~0.51 (this is with cellGene all being 'a')
		chance = 1
		while 0.45 > chance or chance > 0.55:
		    newV = random.choices(string.ascii_lowercase + string.digits, k=geneCount)
		    numbersV = np.array([self.characterDict.get(value, value) for value in newV])
		    #Worry about mapping speed later.
		    #https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array
		    #sum((1-abs(numbersV - numbersC)/len(characterDict))/geneCount)
		    
		    chance = 1 - sum(abs(numbersV - numbersC))/(len(self.characterDict)*geneCount)
		    loops+=1
		    summer += chance
		    #print(newV, chance, loops, summer/loops)
		print("Average binding chance from {} attempts: {} (Final binding chance is {})".format(loops, summer/loops, chance))
		#print(newV, 1-abs(numbersV - numbersC)/len(characterDict)) 

		
		#Filling in initial tables


		#Cells
		#https://stackoverflow.com/a/76132725
		#"cheaper/faster to append to a list and create a DataFrame in one go."
		#In case the startingCells number is in the thousands
		temp = [{"Gene": self.origin, "Next Replication": self.crate, "Life": self.life, "InfectedBy": [], "numbers":numbersC}
		        for _ in range(startingCells)]

		#According to ChatGPT the for loop is better for very large datasets where memory efficiency may be an issue. 
		#Also simply doing `temp*startingCells` will create references to InfectedBy's list instead of making separate lists 
		#(pointer issue if you want to append to only 1 list)
		#Can do something like `Cells.at[6, "InfectedBy"] = Cells.at[7, "InfectedBy"] + [12]` but a simple append seems easier

		"""
		#Below code creates multiple new columns with a character in each for easier future calculations
		#Currently implementation has a single numpy array with all numbers under 1 column, which is simpler.
		numbersC = list(map(ord, numbersC))
		Cells = pd.concat([Cells, pd.DataFrame(temp)], axis=0)
		Cells = pd.concat([Cells, pd.DataFrame([numbersC]*startingCells)], axis=1)
		"""
		self.Cells = pd.concat([self.Cells, pd.DataFrame(temp)], axis=0, ignore_index=True)

		#NOTE THAT doing Cells.at[index, column] is faster than Cells["InfectedBy"][0] bracket notation due to no intermediate Series object
		self.Cells.at[0,"InfectedBy"].append(''.join(newV))

		#freeVirus doesn't exist: existing virus already infected cell (may change in future)

		#len(df.index)
		self.InfectCell.loc[0] = [self.origin, 1, numbersV]
		self.CellTotal.loc[0] = [self.origin, 1, startingCells]
		self.VirusTotal.loc[0] = [''.join(newV), 1, 1]


	#Perform 1 loop of simulation
	def forwardTime(self):
		"""
		self.Cells = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.FreeVirus = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.InfectCell = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.CellTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.VirusTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		"""
		return


	#Gives an array of infection chance (1xN) given two numpy arrays (1xN) each containing of genetic strings.
	def infectionChance(self, cellGene: str, virusGene:str) -> float:
		#https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array

		#TBA
		return 0.1


	#Update self.origin gene at position "index" with "newChar"
	def modifyGene(self, index: int, newChar: str):
		if (len(newChar) != 1):
			print("!!!REPORT THIS!!! Somehow obtained non-1 character input at once for modifyGene: " + newChar)
			return
		self.origin = self.origin[:index] + newChar + self.origin[index+1:]


