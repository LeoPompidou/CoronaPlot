# Aufruf: python plot.py confirmed perc Italy France

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


if sys.argv[1] in ["confirmed", "deaths", "recovered"]:
	if sys.argv[1] == "recovered":
		url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

	if sys.argv[1] == "deaths":
		url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

	if sys.argv[1] == "confirmed":
		url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
else:
	sys.exit("\nKonnte keine Daten finden..\nBitte \"confirmed\", \"recovered\" oder \"deaths\" hinter plot.py angeben!")

if sys.argv[2] not in ["values", "diff", "perc"]:
	sys.exit("\nWelche Daten sollen angezeigt werden?\n" + 
		"Bitte \"diff\" für die täglichen Unterschiede, \"perc\" für prozentuale Unterschiede oder " + 
		"\"values\" für die absoluten Werte an zweiter Stelle angeben!")




df = pd.read_csv(url, index_col=False)


# Zeitraum einschränken
if "/" in sys.argv[3]:
	print("Datum verändert!")
	firstidx = list(df.columns).index(sys.argv[3])
	secondidx = list(df.columns).index(sys.argv[4])
	print(firstidx)
	print(secondidx)
	print([0,1,2,3] + list(range(firstidx, secondidx)))
	df = df.iloc[:, [0,1,2,3] + list(range(firstidx, secondidx+1))]
	print(df)
	spot = sys.argv[5:]
else:
	spot = sys.argv[3:]



df["Ort"] = df["Country/Region"] + "-" + df["Province/State"]
df['Ort'].replace(np.nan, df["Country/Region"], inplace=True)

print(df)

# China und USA Daten zsmfassen
if "China" in spot:
	df_a = df[df["Country/Region"] == "China"].sum()

	df_a.loc["Country/Region"] = "China"
	df_a.loc["Province/State"] = ""
	df_a.loc["Ort"] = "China"
	print(df_a)
	df = df[df["Country/Region"] != "China"]
	df = df.append(df_a.T, ignore_index=True)

if "US" in spot:
	df_a = df[df["Country/Region"] == "US"].sum()
	df_a.loc["Country/Region"] = "US"
	df_a.loc["Province/State"] = ""
	df_a.loc["Ort"] = "US"
	df = df[df["Country/Region"] != "US"]
	df = df.append(df_a.T, ignore_index=True)

if "Canada" in spot:
	df_a = df[df["Country/Region"] == "Canada"].sum()
	df_a.loc["Country/Region"] = "Canada"
	df_a.loc["Province/State"] = ""
	df_a.loc["Ort"] = "Canada"
	df = df[df["Country/Region"] != "Canada"]
	df = df.append(df_a.T, ignore_index=True)

if "United Kingdom" in spot:
	df_a = df[df["Country/Region"] == "United Kingdom"].sum()
	df_a.loc["Country/Region"] = "United Kingdom"
	df_a.loc["Province/State"] = ""
	df_a.loc["Ort"] = "United Kingdom"
	df = df[df["Country/Region"] != "United Kingdom"]
	df = df.append(df_a.T, ignore_index=True)

print(df.head())

cou = df.loc[df["Country/Region"].isin(spot)]



print(cou)

cou_t = cou.T
cou_t.drop(["Province/State", "Country/Region", "Lat", "Long"], 0,
           inplace = True)
print(cou_t.loc["Ort"])

cou_t.drop("Ort", 0, inplace = True)

if sys.argv[2] == "diff":
	data = cou_t.diff()

if sys.argv[2] == "perc":
	data = cou_t.pct_change()

if sys.argv[2] == "values":
	data = cou_t

print(data)

##if 1+1==2:
##    raise RuntimeError("Fehler in der Matrix!")


data.plot()

# Shrink current axis by 20%
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), labels = cou["Ort"])

#plt.legend(loc="best", labels = cou["Ort"])
plt.xlabel("Zeitpunkt")
plt.ylabel(sys.argv[1] + " - " + sys.argv[2])
plt.show()












### Übung 9 ###

### Aufgabe 1 ### 


##def transitionMatrix(cTable):
##    probs = []
##    cRowSum = []
##    cList = list(cTable.keys())
##    #print(cList)
##    i = 0
##    for _ in range(16):
##        cRowSum.append(cTable[cList[i]] + cTable[cList[i+1]] + cTable[cList[i+2]]+ cTable[cList[i+3]])
##        i += 4
##    j = 0
##    for c in cList: 
##        probs.append(cTable[c] / cRowSum[j//4])
##        j += 1
##    #print(cRowSum)
##    return np.asarray(probs)
##
##            
##
##
##def countCodons(inputFileName):
##    """Returns a dictionary containing all 64 codons with
##    their number of occurences in inputFileName"""
##    cTable = emptyCodonTable()
##    with open(inputFileName, "r") as f:
##        for line in f:
##            startPos = 0
##            if line[0] == ">":
##                newSeq = True
##            elif newSeq:
##                prevC = line[:3]
##                cTable[prevC] += 1
##                startPos = 3
##                newSeq = False
##            if not newSeq:
##                for i in range(startPos, len(line.rstrip())):
##                    c = prevC[1:] + line[i]
##                    cTable[c] += 1
##                    prevC = c
##    return cTable
##
##
##def emptyCodonTable():
##    """Returns a dictionary containing all 64 codons with value 0"""
##    cTable = {}
##    alphabet = ["a", "c", "g", "t"]
##    for i in alphabet:
##        for j in alphabet:
##            for k in alphabet:
##                cTable[i+j+k] = 0
##    return cTable
##
##
##def loglike(inputFileName, fenetra):
##    with open(inputFileName, "r") as f:
##        for line in f:
##            if line[0] != ">":
##                logar = []
##                cList = list(gCoTa.keys())
##                i = 2
##                sAR = []
##                while  i < len(line.rstrip()) - fenetra + 1:
##                    """ calculate all values in reading frame"""
##                    if i == 2:
##                        for j in range(0, fenetra-1):
##                            gVal = gMatrix[cList.index(line[(i+j)-2]+line[(i+j)-1]+line[i+j])]
##                            ncVal = ncMatrix[cList.index(line[(i+j)-2]+line[(i+j)-1]+line[i+j])]
##                            sAR.append(np.log(gVal / ncVal))
##                    """ delete first value and add new """
##                    if i > 2:
##                        sAR.pop(0)
##                        gVal = gMatrix[cList.index(line[i+fenetra-3]+line[i+fenetra-2]+line[i+fenetra-1])]
##                        ncVal = ncMatrix[cList.index(line[i+fenetra-3]+line[i+fenetra-2]+line[i+fenetra-1])]
##                        sAR.append(np.log(gVal / ncVal))
##                    logar.append(sum(sAR))
##                    i += 1
##    return logar
##
##
##def writeSeq(seqStr, fileName):
##    """Writes Log-Likelihood-Ratio to file."""
##    with open(fileName, "w") as f:
##        for item in seqStr:
##            f.write("%s\n" % item)
##    	
##
##cwd = os.getcwd()
##os.chdir(cwd)
##gCoTa = countCodons("y_genes.txt")
##gMatrix = transitionMatrix(gCoTa)
###print(gCoTa)
##print("Transitionsmatrix (G-Modell):\n")
##print(np.round(gMatrix.reshape(16,4), 3))
##ncCoTa = countCodons("y_ncregions.txt")
##ncMatrix = transitionMatrix(ncCoTa)
###print(ncCoTa)
##print("\nTransitionsmatrix (NC-Modell):\n")
##print(np.round(ncMatrix.reshape(16,4), 3))
##logar = loglike("test.txt", 1000)
##
##writeSeq(logar, "Log-Likelihood-Ratio.txt")
##
##
##plt.plot(logar)
##plt.show()
##
##
##


















