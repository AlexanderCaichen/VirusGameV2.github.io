#!/usr/bin/env python

#For handling game logic

import pandas as pd 
import numpy as np

import string
import random

import sys

#GAME IS WON WHEN VIRUSES CAN'T INFECT CELLS (For set amount of time?)
#Virus gets killed if not infect? 
#Virus factory mode (infected cells, if divide, can make new viruses)

class Game:
	#Game setup
	#geneCount: length of gene
	#vMutRate: chance of each virus gene to mutate when replicating
	#cMutRate: time it takes to change a genome/CREATE A NEW CELL (cooldown)
	#startingCells: number of cells you start with
	#repCRate: time it takes for each of your cells to replicate
	#repVRate: time it takes for each virus to replicate after infecting cell
	#???repVRate2: How many viruses replicate
	#cLifeSpan: how long it takes for your cell to die (life)
	#???vLifeSpan: how long it takes for your virus to die if not infect cell (see it as immune system naturally clearing foreign bodies???)
	#dmg: how much damage virus does to cell each replication
	def __init__(self, geneCount: int = 5, vMutRate: float = 0.2, cMutRate: float = 5, startingCells: int = 4, repCRate: int = 5, repVRate: int = 3, vLifeSpan: int = 15, lifeSpan: int = 30, dmg: int = 1):
		self.geneCount = geneCount
		self.mutateChance = vMutRate
		self.cooldown = cMutRate
		#startingCells
		self.crate = repCRate
		self.vrate = repVRate
		self.life = lifeSpan
		self.dmg = dmg


		#initializing instance variables (placed inside in case character options change between games)
		self.characterDict = dict()
		for i in string.ascii_lowercase + string.digits:
			self.characterDict[i] = len(self.characterDict)
		self.reverseDict = np.array([char for char in string.ascii_lowercase + string.digits])

		#Note that modifying class variables (not instance variables) will also modify other instances of class
		self.Cells = pd.DataFrame(columns=["Gene", "Next Replication", "Life", "InfectedBy", "numbers", "ID"])
		self.FreeVirus = pd.DataFrame(columns=["Gene", "numbers"])
		#Summary stats of cells being infected. Add "InfectedBy"?
		self.InfectCell = pd.DataFrame(columns=["Gene", "Num Cell Infected", "numbers"])
		#Viruses infecting cell
		self.InVirus = pd.DataFrame(columns=["Gene", "cellID", "next", "numbers"])
		self.CellTotal = pd.DataFrame(columns=["Gene", "Total Exist", "Curr Alive"]).set_index('Gene')
		self.VirusTotal = pd.DataFrame(columns=["Gene", "Total Exist", "Curr Existing"]).set_index('Gene')
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
		print("Average binding chance from {} attempts: {} (Final binding chance is {})".format(loops, round(summer/loops, 3), round(chance, 3)))
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
		self.Cells["ID"] = np.random.randint(sys.maxsize, size=startingCells)

		#NOTE THAT doing Cells.at[index, column] is faster than Cells["InfectedBy"][0] bracket notation due to no intermediate Series object
		newVName = ''.join(newV)
		self.Cells.at[0,"InfectedBy"].append(newVName)

		#FreeVirus doesn't contain data yet: existing virus already infected cell (may change in future)

		self.InVirus.loc[0] = [newVName, self.Cells.at[0, "ID"], self.vrate, numbersV]

		#len(df.index)
		self.InfectCell.loc[0] = [self.origin, 1, numbersC]
		self.CellTotal.loc[self.origin] = [startingCells, startingCells]
		self.VirusTotal.loc[newVName] = [1, 1]


	#Perform 1 loop of simulation
	def forwardTime(self):
		"""
		self.Cells = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.FreeVirus = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.InfectCell = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.CellTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		self.VirusTotal = pd.DataFrame(np.random.randint(0,50,size=(50, 4)), columns=list('ABCD'))
		"""
		self.Cells["Life"] -= 1

		self.InVirus["next"] -= 1
		#Get replicating viruses (note that dead cells shouldn't produce viruses)
		#Can drop "next" column for temp
		temp = self.InVirus.loc[self.InVirus["next"] <= 0]
		if not temp.empty:
		    #Cells have life -dmg*viruses replicating
		    #https://stackoverflow.com/questions/41340341/how-to-determine-the-length-of-lists-in-a-pandas-dataframe-column
		    #Cells["Life"] -= (np.array([len(x) for x in Cells["InfectedBy"]]) * dmg) <<< issue: some viruses aren't replicating now
		    #Get number of replicating viruses in relavent cells
		    temp2 = temp["cellID"].value_counts()
		    #Cells.loc[Cells["ID"].isin(temp2.index), "Life"] -= temp2.values*dmg <<< issue: subtracted value might not match cells
		    #Merge based on cellID ensures replicating-virus counts are matched to ID when subracting
		    self.Cells["Life"] -= pd.merge(self.Cells["ID"], temp2, left_on="ID", right_index=True, how="left")["count"].fillna(0).astype(int) * self.dmg
		    
		    #Create a new virus with `self.mutateChance` mutation:
		    #For each virus generate np.array with geneCount floats (column via np.random.rand(size)). 
		    #Apply a value comparison to create a mask that says whether a spot in a gene will mutate or not.
		    temp["mask"] = pd.Series([np.random.rand(self.geneCount) for _ in range(len(self.InVirus.index))]).apply(lambda x: x< self.mutateChance)

		    # Function to replace specific values with random values based on a mask of True/False values
		    #numbers and mask should be numpy arrays of same size
		    def mutateSelected(numbers, mask):
		        # Generate random values of the same shape as the array
		        #print(numbers[mask])
		        if (mask.any()):
		            numbers[mask] = np.random.randint(len(self.characterDict), size=mask.sum())
		        return numbers

		    # Apply the function to the DataFrame
		    #row['numbers'].copy() because copy(deep=True) doesn't actually deep copy numpy array within the column 
		    #so changes to `temp`'s numpy arrays will result corresponding arrays in InVirus also changing. 
		    temp["numbers"] = temp.apply(lambda row: mutateSelected(row['numbers'].copy(), row['mask']), axis=1)


		    #convert np.array of numbers to characters, then string for virus name
		    #https://stackoverflow.com/a/41678874
		    #display(temp["numbers"].apply(lambda x: map(reverseDict, x)))
		    #https://stackoverflow.com/a/55950051
		    """mapping_ar = np.zeros(numb.max()+1,dtype=alph.dtype)
		    mapping_ar[numb] = alph
		    display(mapping_ar[temp["numbers"][0]])"""
		    temp["Gene"] = temp["numbers"].apply(lambda x: ''.join(self.reverseDict[x]))
		    
		    #Add viruses to freeVirus 
		    #(TODO: Start new infections with freeVirus before or after replicating???)
		    self.FreeVirus = pd.concat([self.FreeVirus, temp[["Gene", "numbers"]]], axis=0, ignore_index=True)
		    
		    
		    #reset temp virus "next" to vrate
		    self.InVirus.loc[self.InVirus["next"] <= 0, "next"] = self.vrate

		    
		    #TODO: Add numbers to respective VirusTotal["Total Exist"]

		##########################################
		#check for dead cells (Note that virus replication may kill cells)

		#Get dead cells
		temp = self.Cells.loc[self.Cells["Life"] <= 0]
		if not temp.empty:
		    #Removing dead cells
		    self.Cells.drop(list(temp.index), inplace=True)
		    
		    #Removing Viruses infecting those cells (drop viruses that have same ID as dropped cells)
		    self.InVirus.drop(self.InVirus["cellID"].isin(temp["ID"]).index, inplace=True)
		    
		    #(Not needed?) Reduce "Num Cell Infected" in InfectCell


		##########################################
		#Infection time
		#New dataset: column of np.random.randint(Cell.index) to determine which cell to infect
		#New dataset: merge Cells and freeVirus based on index and column being equal
		#New column infectchance = 1 - sum(abs(numbersV - numbersC))/(len(characterDict)*geneCount)
		#New column of np.random.rand. If value <= infectchance then proceed with infection
		#Add viruses to InVirus and Cells["Infected By"]

		#freeVirus 
		#using random.choice instead of random.randint in the case there are holes in index number for whatever reason
		#temp["nextCell"] = np.random.choice(Cells.index, size=len(freeVirus.index))


		##########################################
		#Replicating Cells
		#Cells["Next Replication"] -= 1
		#temp = Cells.loc[Cells["Life"] <= 0]
		#if not temp.empty:
		    #create another cell for each Cell (duplicate selected rows)
		    #make "InfectedBy" = blank numpy array
		    #modify cell ID np.random.randint(sys.maxsize, size=10)
		    #concat table to current table. 

		#Add new cell counts to CellTotal["Total Exist"]

		##########################################
		#Update summary
		    #Update Alive count in CellTotal
		    #***Update later***
		    #Cells.groupby("Gene").count()
		    #Cells["Gene"].value_counts()
		    
		    #Update Virus count in Virus Total["Curr Existing"]
		    
		    #Set InfectCells as   Select Cells[Infected By != empty], groupby "Gene"

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


