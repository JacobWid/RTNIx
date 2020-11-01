#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:38:14 2020

@author: Jacob  Widmann
"""


import csv
from IHU_source import *
import pickle
import re




class mathemathikaFunction:



    def __init__(self,integratedTN):
         self.AnalyzedTN = []
         self.mathStringArray = []
         self.usedFactor = [False,False,False,False,False,False,False]
         self.pArr = []

         #Assuring only nonzero entrys are considered
         for i in range(len(integratedTN)):
             if(integratedTN[i][1] !=0):
                 self.AnalyzedTN.append(integratedTN[i])



         pNumber = 0
         regexExp = "\[\[\'([A-Z,a-z]+)\', ([1-2]), 'out', 1\], \[\'\\1\', \\2, 'in', 1\]\]"
         replaceString = "Tr("+"\\1"+"\\2"+")"
         mathExp = "1"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 1
         regexExp = "\[\['(([A-Z]{2}\d+)\_E)\*', 2, 'out', 1\], \['\\1', 2, 'in', 1\]\], \[\['\\1\*', 2, 'out', 2\], \['\\1', 2, 'in', 2\]\], \[\['\\1\*', 2, 'in', 1\], \['\\1', 2, 'out', 1\]\], \[\['\\1\*', 2, 'in', 2\], \['\\1', 2, 'out', 2\]\]"
         replaceString = "Tr("+"\\1"+")"
         mathExp = "Tr[ConjugateTranspose[e].e]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 2
         regexExp = "\[\['([A-Z])', 2, 'out', 1\], \['(([A-Z]{2}\d+)\_E)\*', 2, 'in', 1\]\], \[\['\\1', 2, 'in', 1\], \['\\2', 2, 'out', 1\]\]. \[\['\\2\*', 2, 'out', 1\], \['\\2', 2, 'in', 1\]\], \[\['\\2\*', 2, 'out', 2\], \['\\2', 2, 'in', 2\]\],.\[\['\\2\*', 2, 'in', 2], \['([A-Z])', 2, 'out', 1\]\], \[\['\\2', 2, 'out', 2\], \['\\4', 2, 'in', 1\]\]"
         replaceString = "Tr(\\3_E*.(\\1x\\4).\\3_E))"
         mathExp = "Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 3
         regexExp = "\[\['(([A-Z]{2}\d+)\_E)\*', 2, 'out', 1\], \['\\1\*', 2, 'in', 1\]\], \[\['\\1\*', 2, 'out', 2\], \['\\1\*', 2, 'in', 2\]\], \[\['\\1', 2, 'out', 1\], \['\\1', 2, 'in', 1\]\], \[\['\\1', 2, 'out', 2\], \['\\1', 2, 'in', 2\]\]"
         replaceString = "Tr(\\1*)Tr(\\1)"
         mathExp = "Tr[e\[ConjugateTranspose]]*Tr[e]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 4
         regexExp = "\[\['([A-Z])', 1, 'out', 1\], \['(([A-Z]{2}\d+)\_E)', 2, 'in', 1\]\], \[\['\\1', 1, 'in', 1\], \['\\2\*', 2, 'out', 1\]\], \[\['\\1', 2, 'out', 1\], \['\\2\*', 2, 'in', 1\]\], \[\['\\1', 2, 'in', 1\], \['\\2', 2, 'out', 1\]\], \[\['\\2\*', 2, 'out', 2\], \['([A-Z])', 1, 'in', 1\]\], \[\['\\2\*', 2, 'in', 2\], \['([A-Z])', 2, 'out', 1\]\], \[\['\\2', 2, 'out', 2\], \['\\5', 2, 'in', 1\]\], \[\['\\2', 2, 'in', 2\], \['\\5', 1, 'out', 1\]\]"
         replaceString = "Tr((\\1x\\5).\\2*.(\\1x\\5).\\2)"
         mathExp ="Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 5
         regexExp = "\[\['(([A-Z]{2}\d+)\_E)\*', 2, 'out', 1\], \['\\1', 2, 'in', 1\]\], \[\['\\1\*', 2, 'out', 2\], \['\\1\*', 2, 'in', 2\]\], \[\['\\1\*', 2, 'in', 1\], \['\\1', 2, 'out', 1\]\], \[\['\\1', 2, 'out', 2\], \['\\1', 2, 'in', 2\]\]"
         replaceString = "Tr(Tr2(\\1*).Tr2(\\1))"
         mathExp = "Tr[TraceSystem[e\[ConjugateTranspose],{2}].TraceSystem[e,{2}]]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])

         pNumber = 6
         regexExp = "\[\['(([A-Z]{2}\d+)\_E)\*', 2, 'out', 1\], \['\\1\*', 2, 'in', 1\]\], \[\['\\1\*', 2, 'out', 2\], \['\\1', 2, 'in', 2\]\], \[\['\\1\*', 2, 'in', 2\], \['\\1', 2, 'out', 2\]\], \[\['\\1', 2, 'out', 1\], \['\\1', 2, 'in', 1\]\]"
         replaceString = "Tr(Tr1(\\1*).Tr1(\\1))"
         mathExp = "Tr[TraceSystem[e\[ConjugateTranspose],{1}].TraceSystem[e,{1}]]"
         self.pArr.append([pNumber,regexExp,replaceString,mathExp])


         for i in range(len(self.AnalyzedTN)):
             self.mathStringArray.append([])
             s = str(self.AnalyzedTN[i][0])
             for j in self.pArr:
                 s = self.pGeneral(s,i,j[0],j[1],j[2],j[3])
         return

    def pGeneral(self,s,i,pNumber,regExp,replaceString,mathExp):
            p = re.compile(regExp)
            sNew = p.sub(replaceString,s)

            if(self.usedFactor[pNumber] or p.search(s) != None):
                self.usedFactor[pNumber] = True

            self.AnalyzedTN[i][0] = sNew

            FindArray = p.findall(s)

            for j in range(len(FindArray)):
                self.mathStringArray[i].append(mathExp)

            return sNew

    def createSum(self):

        sges = "0"

        for i in range(len(self.AnalyzedTN)):
            factor = str(self.AnalyzedTN[i][1])
            productS = "1"

            for j in self.mathStringArray[i]:
                productS = productS + "*" + str(j)


            sges = sges + "+" + factor + "*("+productS+")"
        return sges







#Start------------------------------------------------------------------------

width = 8
depth = 2

def getWireName(n):
        return str(chr(n+65))

filename = "Data/Circuit_"
filename = filename + "Ato" + getWireName(width-1)+"_"+ str(depth)

filename1 = filename + ".txt"
print("Loading from " + filename1)
with open(filename1,"rb") as fp:    #Unpickling
    integratedTN = pickle.load(fp)

AnalyzedObject = mathemathikaFunction(integratedTN)


#Saving summand in csv file---------------------------------------------
filename2 = filename + "_Analys.csv"
with open(filename2, 'w') as csvfile:
    fields = ["Network","Factor"]
    AnalyzedTN = AnalyzedObject.AnalyzedTN
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(AnalyzedTN)
print("Saved to " + filename2)


#Saving Sum in nb file for mathematika-------------------------------------------
filename3 = filename + "_AnalysCircuitSum.m"
print("Sum saved to Mathematika File: " + os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'MATHEMATICA',filename3)))
filename3 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'MATHEMATICA',filename3))
with open(filename3,"w") as file:
    circuitSum =  AnalyzedObject.createSum()

    file.write('BeginPackage["circuitSum'+"Ato" + getWireName(width-1)+ str(depth)+'`"]\n')
    file.write("\n")
    file.write("CircuitSum"+str(width)+"w"+str(depth)+"d::usage = \n" + '"SumOfCircuit"\n\n' )
    file.write('Begin[ "Private`"]\n\n')
    file.write('Import["/home/jacob/SynologyDrive/Universität/QuantenInfo/Bachelorarbeit/RTNI-master/MATHEMATICA/Data/PartialTrace.m"]\n')
    file.write("CircuitSum"+str(width)+"w"+str(depth)+"d[ e_, A_] :=\n")
    file.write("Module[ {sum},\n")
    file.write("      sum = "+circuitSum+";\n")
    file.write("      Simplify[sum]\n")
    file.write("]\n")
    file.write("End[]\n")
    file.write("EndPackage[]\n")
    # print(s)


print(AnalyzedObject.usedFactor)
