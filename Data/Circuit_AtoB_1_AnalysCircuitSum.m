BeginPackage["circuitSumAtoB1`"]

CircuitSum2w1d::usage = 
"SumOfCircuit"

Begin[ "Private`"]

Import["/home/jacob/SynologyDrive/Universität/QuantenInfo/Bachelorarbeit/RTNI-master/MATHEMATICA/Data/PartialTrace.m"]
CircuitSum2w1d[ e_, A_] :=
Module[ {sum},
      sum = 0+1*(1*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e]);
      Simplify[sum]
]
End[]
EndPackage[]
