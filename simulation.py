#!/usr/bin/env python

#For handling game logic

import pandas as pd 
import numpy as np

#time it takes for infected cell to pop out a virus (per virus infecting cell)
virusMakeTime = 5
#chance for new virus to mutate each part of genome
mutationRate = 0.01


#time it takes for cell to divide. Slower than virus
cellMakeTime = 10
#amount of time a cell lives for
cellLife = 30
#time to create new cell (*cooldown)
newGenomeTime = 5


Cells = pd.DataFrame(columns=["Gene", "Next Replication", "Life", "InfectedBy"])
Virus = pd.DataFrame(columns=["Gene", "Next Infection Chance"])
InfectCell = pd.DataFrame(columns=["Gene", "Cell Infected"])
CellTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Alive"])
VirusTotal = pd.DataFrame(columns=["Gene", "Percent of Population", "Number Existing"])
