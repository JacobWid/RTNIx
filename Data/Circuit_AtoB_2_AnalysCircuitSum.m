BeginPackage["circuitSumAtoB2`"]

CircuitSum2w2d::usage = 
"SumOfCircuit"

Begin[ "Private`"]

Import["/home/jacob/SynologyDrive/Universität/QuantenInfo/Bachelorarbeit/RTNI-master/MATHEMATICA/Data/PartialTrace.m"]
CircuitSum2w2d[ e_, A_] :=
Module[ {sum},
      sum = 0+1/15*(1*1*1*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e])+-1/60*(1*1*1*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e]*Tr[e\[ConjugateTranspose]]*Tr[e])+-1/60*(1*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e])+1/15*(1*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e]);
      Simplify[sum]
]
End[]
EndPackage[]
