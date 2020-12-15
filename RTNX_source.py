#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 14:16:47 2020

@author:  Jacob  Widmann
"""

from IHU_source import *
import re
import csv
import pickle
import time
import networkx as nx
import matplotlib.pyplot as plt

class RTNx:

    def __init__(self):
       self.mulDiG = nx.MultiDiGraph()
       self.integrationNodeArray = []



    def setMuldigAndIntegrationNodeArray(self,muldig,integrationNodeArray):
        self.mulDiG = muldig
        self.integrationNodeArray = integrationNodeArray

    def union(tnx1,tnx2):
        # print(self.mulDiG.nodes)
        # print(tnx.mulDiG.nodes)
        unionGraph = nx.union(tnx1.mulDiG,tnx2.mulDiG)
        unionTnx= RTNx()
        newIntegrationNodeArray = tnx1.integrationNodeArray + tnx2.integrationNodeArray
        unionTnx.setMuldigAndIntegrationNodeArray(unionGraph,newIntegrationNodeArray)

        return unionTnx


    def add_node(self,name,ID):
       node = RtnxNode(name,ID)
       self.mulDiG.add_node(node)
       return node


    def add_U_node(self,name,ID,inDims,outDims,totalDims):

        #inDims,outDims and totalDims needed for Integration
        uNode = RtnxNode(name,ID,inDims,outDims,totalDims)
        usNode = RtnxNode(name+"*",ID)
        self.integrationNodeArray.append(uNode)

        return uNode,usNode

    def add_edge(self,node1,node2,node1Leg,node2Leg):

        if not isinstance(node1,RtnxNode):
            raise TypeError("Node must be RtnxNode. It is of type ",type(node1))

        if not isinstance(node2,RtnxNode):
            raise TypeError("Node must be RtnxNode. It is of type ",type(node2))

        edge = self.mulDiG.add_edge(node1,node2,leg1 = node1Leg,leg2 = node2Leg)
        return edge

    def getRTNI_string(self):
        edgeStringArray = []

        # print(self.mulDiG.edges(data=True))

        for i in self.mulDiG.edges(data=True):
            # print(i)
            # print(i[0])
            # print(i[0].name)
            edgeStringArray.append([ [i[0].name,i[0].ID,"out",i[2]['leg1']] ,  [i[1].name,i[1].ID,"in",i[2]['leg2']] ] )

        return edgeStringArray

    def getIntegratedRTNI_array(self):
        integrationStringArray = []
        dimArray = []

        for node in self.integrationNodeArray:
            if(node != []):
                if node.name in integrationStringArray:
                    pass
                else:
                    integrationStringArray.append(node.name)
                    dimArray.append([node.name,node.inDims,node.outDims,node.totalDims])


        integratedRTNI_array = [self.getRTNI_string(),1]

        #Umsortieren
        dimArrLen = len(integrationStringArray)
        newNumberOrderArray = []
        if(dimArrLen%2==1):
            dimArrLenEven = dimArrLen -1
        else:
            dimArrLenEven = dimArrLen

        i = 0
        while i < dimArrLenEven/2:
            newNumberOrderArray.append(int(dimArrLenEven/2+i))
            newNumberOrderArray.append(int(dimArrLenEven/2-i-1))
            i += 1

        if(dimArrLen%2==1):
            newNumberOrderArray.append(dimArrLen -1)
        print(newNumberOrderArray)


        j = 1
        for i in newNumberOrderArray:
            print("Integrating over " + str(j)+ " of " + str(len(integrationStringArray)) + " Unitaries")
            start_time = time.time()
            # print(integrationStringArray[i])
            # print(dimArray[i])
            integratedRTNI_array = integrateHaarUnitary(integratedRTNI_array,dimArray[i])
            # integratedRTNI_array = integrateHaarUnitary(integratedRTNI_array,dimArray[int((dimArrLen/2+i)%dimArrLen)])
            # print(integratedRTNI_array)
            elapsed_time = float(time.time()-start_time)
            elapsed_time = '%.3f'%(elapsed_time)
            print("Elapsed time: " + str(elapsed_time)+ " seconds")
            print()
            j +=1

        return integratedRTNI_array



    def __str(self):
        s = self.getRTNI_string()
        return str(s)

    def __repr__(self):
        return str(self.getRTNI_string())

    def mathematikaString(string = None):

        mathString = str(string)
        mathString = re.sub("\[", "{", mathString)
        mathString = re.sub("\]", "}", mathString)
        mathString = re.sub("\'", '"', mathString)
        print(mathString)

class Circuit(RTNx):

    def __init__(self,n):
        self.mulDiG = nx.MultiDiGraph()
        self.integrationNodeArray = []
        self.openDecInArray  = []
        self.openDecOutArray = []
        self.addWire(n)

    def setDecorations(self,openDecInArray,openDecOutArray):
        self.openDecInArray = openDecInArray
        self.openDecOutArray = openDecOutArray

    def addWire(self,n):
        for i in range(n):
            self.openDecInArray.append([])
            self.openDecOutArray.append([])

    def fillEmptyWire(self,node,wireNumberArray):
        #Not Implemented Yet
        return

    def fillOpenWiresAlphabetically(self,ID):
        for i in range(len(self.openDecInArray)):
            wireName = Circuit.getWireName(i)
            if(self.openDecInArray[i] == []):
                wireNode = self.add_node(wireName,ID)
                self.openDecInArray[i] = [wireNode,1]
                self.openDecOutArray[i] = [wireNode,1]

    def connectWireToGate(self,gateS,wireNumberArray):
        # print("WireToGate")
        # print(self)
        for i in range(len(wireNumberArray)):
            # print(self.openDecOutArray)
            j = wireNumberArray[i]
            wireNode = self.openDecOutArray[j][0]
            wireDecNumber = self.openDecOutArray[j][1]
            self.add_edge(wireNode,gateS,wireDecNumber,i+1)
            self.openDecOutArray[j] = [gateS,i+1]
        # print(self)
        return

    def connectGateToWire(self,gate,wireNumberArray):
        # print("GateToWire")
        # print(self)
        for i in range(len(wireNumberArray)):
            j = wireNumberArray[i]
            wireNode = self.openDecInArray[j][0]
            wireDecNumber = self.openDecInArray[j][1]
            self.add_edge(gate,wireNode,i+1,wireDecNumber)
            self.openDecInArray[j] = [gate,i+1]
        # print(self)
        return

    def getWireName(n):
        return str(chr(n+65))

    def connectCircuit(circ1,circ2):

        # print(RTNx.mathematikaString(circ2.getRTNI_string()))


        if(circ1.getWireNumber() != circ2.getWireNumber()):
            raise ValueError("Both circuits must have the same amount of Wires!")

        try:
            connectedCirc_mulDiG = nx.union(circ1.mulDiG,circ2.mulDiG)
        except nx.NetworkXError:
            raise nx.NetworkXError("The two circuits cant have the same nodes.","('The node sets of G and H are not disjoint.', 'Use appropriate rename=(Gprefix,Hprefix)or use disjoint_union(G,H).')")


        connectedCircuit= Circuit(0)
        newIntegrationNodeArray = circ1.integrationNodeArray + circ2.integrationNodeArray


        connectedCircuit.setMuldigAndIntegrationNodeArray(connectedCirc_mulDiG,newIntegrationNodeArray)

        for i in range(len(circ1.openDecOutArray)):
            circ1WireGate = circ1.openDecOutArray[i][0]
            circ1Dec      = circ1.openDecOutArray[i][1]
            circ2WireGate = circ2.openDecInArray[i][0]
            circ1Dec      = circ1.openDecOutArray[i][1]
            connectedCircuit.add_edge(circ1WireGate,circ2WireGate,circ1Dec,circ1Dec)

        connectedCircuit.setDecorations(circ1.openDecInArray,circ2.openDecOutArray)

        return connectedCircuit

    def closeCircuit(self):
        for i in range(len(self.openDecOutArray)):
            circ1WireGate = self.openDecOutArray[i][0]
            circ1Dec      = self.openDecOutArray[i][1]
            circ2WireGate = self.openDecInArray[i][0]
            circ1Dec      = self.openDecOutArray[i][1]
            self.add_edge(circ1WireGate,circ2WireGate,circ1Dec,circ1Dec)

            # print(RTNx.mathematikaString(self.getRTNI_string()))

        return

    def getWireNumber(self):
        if(len(self.openDecInArray) != len(self.openDecOutArray)):
            raise ValueError("openDecInArray and openDecOutArray have different lengths!!")
        return len(self.openDecOutArray)


    #Following Functions are unused, but should be functional. Can be used to connect multiple gates at once to the circuit
    # def addLayerOfGatesS(self,gateS_WireNumberArray):
    #     #gate_WireNumberArray Should have the Form [[gate1,[i1,j1,k1,...]],[gate2,i2,j2,k2,...]] each integer Array refers to the wirenumber where the respespective gates should connect
    #     for gateS_WireNumber in range(len(gateS_WireNumberArray)):
    #         self.connectWireToGate(gateS_WireNumber[0],gateS_WireNumber[1])

    # def addLayerOfGates(self,gate_WireNumberArray):
    #     #gate_WireNumberArray Should have the Form [[gate1,[i1,j1,k1,...]],[gate2,i2,j2,k2,...]] each integer Array refers to the wirenumber where the respespective gates should connect
    #     for gate_WireNumber in range(len(gate_WireNumberArray)):
    #         self.connectGateToWire(gate_WireNumber[0],gate_WireNumber[1])


class RtnxNode():

    def __init__(self,name,ID,inDims = None,outDims = None,totalDims = None):
        self.name = name
        self.ID = ID
        self.inDims = inDims
        self.outDims = outDims
        self.totalDims = totalDims

    def __str__(self):
        return str(self.name)+"_"+str(self.ID)

    def __repr__(self):
        return str(self.name)+"_"+str(self.ID)




# s = [[[['A', 1, 'out', 1], ['AB1_U*', 1, 'in', 1]], [['B', 1, 'out', 1], ['AB1_U*', 1, 'in', 2]], [['C', 1, 'out', 1], ['CD1_U*', 1, 'in', 1]], [['D', 1, 'out', 1], ['CD1_U*', 1, 'in', 2]], [['AB1_U', 1, 'out', 1], ['A', 1, 'in', 1]], [['AB1_U', 1, 'out', 2], ['B', 1, 'in', 1]], [['AB1_U*', 1, 'out', 2], ['BC2_U*', 1, 'in', 1]], [['AB1_U*', 1, 'out', 1], ['DA2_U*', 1, 'in', 2]], [['CD1_U', 1, 'out', 1], ['C', 1, 'in', 1]], [['CD1_U', 1, 'out', 2], ['D', 1, 'in', 1]], [['CD1_U*', 1, 'out', 1], ['BC2_U*', 1, 'in', 2]], [['CD1_U*', 1, 'out', 2], ['DA2_U*', 1, 'in', 1]], [['BC2_U', 1, 'out', 1], ['AB1_U', 1, 'in', 2]], [['BC2_U', 1, 'out', 2], ['CD1_U', 1, 'in', 1]], [['BC2_U*', 1, 'out', 1], ['AB3_U*', 1, 'in', 2]], [['BC2_U*', 1, 'out', 2], ['CD3_U*', 1, 'in', 1]], [['DA2_U', 1, 'out', 1], ['CD1_U', 1, 'in', 2]], [['DA2_U', 1, 'out', 2], ['AB1_U', 1, 'in', 1]], [['DA2_U*', 1, 'out', 2], ['AB3_U*', 1, 'in', 1]], [['DA2_U*', 1, 'out', 1], ['CD3_U*', 1, 'in', 2]], [['AB3_U', 1, 'out', 1], ['DA2_U', 1, 'in', 2]], [['AB3_U', 1, 'out', 2], ['BC2_U', 1, 'in', 1]], [['AB3_U*', 1, 'out', 1], ['AB3_U', 2, 'in', 1]], [['AB3_U*', 1, 'out', 2], ['AB3_U', 2, 'in', 2]], [['CD3_U', 1, 'out', 1], ['BC2_U', 1, 'in', 2]], [['CD3_U', 1, 'out', 2], ['DA2_U', 1, 'in', 1]], [['CD3_U*', 1, 'out', 1], ['CD3_U', 2, 'in', 1]], [['CD3_U*', 1, 'out', 2], ['CD3_U', 2, 'in', 2]], [['A', 2, 'out', 1], ['AB1_E*', 2, 'in', 1]], [['B', 2, 'out', 1], ['AB1_E*', 2, 'in', 2]], [['C', 2, 'out', 1], ['CD1_E*', 2, 'in', 1]], [['D', 2, 'out', 1], ['CD1_E*', 2, 'in', 2]], [['AB1_E', 2, 'out', 1], ['A', 2, 'in', 1]], [['AB1_E', 2, 'out', 2], ['B', 2, 'in', 1]], [['AB1_E*', 2, 'out', 1], ['AB1_U*', 2, 'in', 1]], [['AB1_E*', 2, 'out', 2], ['AB1_U*', 2, 'in', 2]], [['AB1_U', 2, 'out', 1], ['AB1_E', 2, 'in', 1]], [['AB1_U', 2, 'out', 2], ['AB1_E', 2, 'in', 2]], [['AB1_U*', 2, 'out', 2], ['BC2_E*', 2, 'in', 1]], [['AB1_U*', 2, 'out', 1], ['DA2_E*', 2, 'in', 2]], [['CD1_E', 2, 'out', 1], ['C', 2, 'in', 1]], [['CD1_E', 2, 'out', 2], ['D', 2, 'in', 1]], [['CD1_E*', 2, 'out', 1], ['CD1_U*', 2, 'in', 1]], [['CD1_E*', 2, 'out', 2], ['CD1_U*', 2, 'in', 2]], [['CD1_U', 2, 'out', 1], ['CD1_E', 2, 'in', 1]], [['CD1_U', 2, 'out', 2], ['CD1_E', 2, 'in', 2]], [['CD1_U*', 2, 'out', 1], ['BC2_E*', 2, 'in', 2]], [['CD1_U*', 2, 'out', 2], ['DA2_E*', 2, 'in', 1]], [['BC2_E', 2, 'out', 1], ['AB1_U', 2, 'in', 2]], [['BC2_E', 2, 'out', 2], ['CD1_U', 2, 'in', 1]], [['BC2_E*', 2, 'out', 1], ['BC2_U*', 2, 'in', 1]], [['BC2_E*', 2, 'out', 2], ['BC2_U*', 2, 'in', 2]], [['BC2_U', 2, 'out', 1], ['BC2_E', 2, 'in', 1]], [['BC2_U', 2, 'out', 2], ['BC2_E', 2, 'in', 2]], [['BC2_U*', 2, 'out', 1], ['AB3_E*', 2, 'in', 2]], [['BC2_U*', 2, 'out', 2], ['CD3_E*', 2, 'in', 1]], [['DA2_E', 2, 'out', 1], ['CD1_U', 2, 'in', 2]], [['DA2_E', 2, 'out', 2], ['AB1_U', 2, 'in', 1]], [['DA2_E*', 2, 'out', 1], ['DA2_U*', 2, 'in', 1]], [['DA2_E*', 2, 'out', 2], ['DA2_U*', 2, 'in', 2]], [['DA2_U', 2, 'out', 1], ['DA2_E', 2, 'in', 1]], [['DA2_U', 2, 'out', 2], ['DA2_E', 2, 'in', 2]], [['DA2_U*', 2, 'out', 2], ['AB3_E*', 2, 'in', 1]], [['DA2_U*', 2, 'out', 1], ['CD3_E*', 2, 'in', 2]], [['AB3_E', 2, 'out', 1], ['DA2_U', 2, 'in', 2]], [['AB3_E', 2, 'out', 2], ['BC2_U', 2, 'in', 1]], [['AB3_E*', 2, 'out', 1], ['AB3_U*', 2, 'in', 1]], [['AB3_E*', 2, 'out', 2], ['AB3_U*', 2, 'in', 2]], [['AB3_U', 2, 'out', 1], ['AB3_E', 2, 'in', 1]], [['AB3_U', 2, 'out', 2], ['AB3_E', 2, 'in', 2]], [['AB3_U*', 2, 'out', 1], ['AB3_U', 1, 'in', 1]], [['AB3_U*', 2, 'out', 2], ['AB3_U', 1, 'in', 2]], [['CD3_E', 2, 'out', 1], ['BC2_U', 2, 'in', 2]], [['CD3_E', 2, 'out', 2], ['DA2_U', 2, 'in', 1]], [['CD3_E*', 2, 'out', 1], ['CD3_U*', 2, 'in', 1]], [['CD3_E*', 2, 'out', 2], ['CD3_U*', 2, 'in', 2]], [['CD3_U', 2, 'out', 1], ['CD3_E', 2, 'in', 1]], [['CD3_U', 2, 'out', 2], ['CD3_E', 2, 'in', 2]], [['CD3_U*', 2, 'out', 1], ['CD3_U', 1, 'in', 1]], [['CD3_U*', 2, 'out', 2], ['CD3_U', 1, 'in', 2]]], 1]
# print(s)
# integrateHaarUnitary(s,["AB1_U",[2,2],[2,2],4])
