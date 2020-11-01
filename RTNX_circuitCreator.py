#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:22:06 2020

@author: Jacob  Widmann
"""

# from IHU_source import *
from RTNX_source import *


def createAndIntegrateCircuit(width,depth,boolInfo):
    filename = "Data/Circuit_"

    circ = Circuit(width)
    circ.fillOpenWiresAlphabetically(1)

    circE = Circuit(width)
    circE.fillOpenWiresAlphabetically(2)

    filename = filename + "Ato" + Circuit.getWireName(width-1)+"_"+ str(depth) + ".txt"


    for i in range(depth):
        startingWire = i%2
        while startingWire  < width:
            startingWirePlus = (startingWire+1)%width
            wireName1 = Circuit.getWireName(startingWire)
            wireName2 = Circuit.getWireName(startingWirePlus)

            uName  =  wireName1+wireName2+ str(i+1)+"_U"
            errName  =  wireName1+wireName2+ str(i+1)+"_E"
            errSName = errName+"*"

            #circ------------------
            newU,newUs     = circ.add_U_node(uName,1,[2,2],[2,2],4)
            circ.connectGateToWire(newU,[startingWire,startingWirePlus])
            circ.connectWireToGate(newUs,[startingWire,startingWirePlus])


            #circE-------------------
            newU_E,newUs_E = circ.add_U_node(uName,2,[2,2],[2,2],4)
            errNode = circE.add_node(errName,2)
            errSNode = circE.add_node(errSName,2)

            circE.connectGateToWire(errNode ,[startingWire,startingWirePlus])
            circE.connectGateToWire(newU_E    ,[startingWire,startingWirePlus])

            circE.connectWireToGate(errSNode,[startingWire,startingWirePlus])
            circE.connectWireToGate(newUs_E   ,[startingWire,startingWirePlus])

            startingWire += 2


    connectedCircuit = Circuit.connectCircuit(circ, circE)
    connectedCircuit.closeCircuit()
    integratedCircArray = connectedCircuit.getIntegratedRTNI_array()
    # for i in integratedCircArray:
        # print(i)
        # print(RTNx.mathematikaString(str(i)))
    # print(integratedCircArray)

    # print()
    print("Saved in file: " + filename)
    with open(filename, "wb") as fp:   #Pickling
        pickle.dump(integratedCircArray, fp)

    return connectedCircuit

# print("61")
# createAndIntegrateCircuit(6,1,False)
# print("62")
# createAndIntegrateCircuit(6,2,False)
# print("63")
createAndIntegrateCircuit(8,3,False)
# print("64")
# createAndIntegrateCircuit(6,4,False)



#How To add Circuits---------------------------------------------------------------------------
def someCircuitCreator(n):
	circ = Circuit(3)
	circ.fillOpenWiresAlphabetically(n)
	U1,Us1 = circ.add_U_node('1U',n,[2,2],[2,2],4)
	U2,Us2 = circ.add_U_node('2U',n+1,[2,2],[2,2],4)
	circ.connectWireToGate(Us1,[0,1])
	circ.connectGateToWire(U2,[1,2])
	return circ

# circ1 = someCircuitCreator(1)
# circ2 = someCircuitCreator(2)
# cirCon = Circuit.connectCircuit(circ1,circ2)
# ar = cirCon.getRTNI_string()
# print(ar)
#-------------------------------------------------------------------------------------------------------------------------------------
