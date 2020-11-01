BeginPackage["circuitSumAtoB3`"]

CircuitSum2w3d::usage = 
"SumOfCircuit"

Begin[ "Private`"]

Import["/home/jacob/SynologyDrive/Universität/QuantenInfo/Bachelorarbeit/RTNI-master/MATHEMATICA/Data/PartialTrace.m"]
CircuitSum2w3d[ e_, A_] :=
Module[ {sum},
      sum = 0+7/450*(1*1*1*Tr[ConjugateTranspose[e].e]*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e])+1/3600*(1*1*1*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e]*Tr[e\[ConjugateTranspose]]*Tr[e])+1/3600*(1*1*1*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e]*Tr[e\[ConjugateTranspose]]*Tr[e])+-1/900*(1*1*1*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].e]*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[e\[ConjugateTranspose]]*Tr[e])+1/3600*(1*Tr[ConjugateTranspose[e].e]*Tr[ConjugateTranspose[e].e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e])+-1/900*(1*Tr[ConjugateTranspose[e].e]*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e])+-1/900*(1*Tr[ConjugateTranspose[e].e]*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e])+1/225*(1*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[e\[ConjugateTranspose]]*Tr[e]*Tr[KroneckerProduct[A,A].e\[ConjugateTranspose].KroneckerProduct[A,A].e]);
      Simplify[sum]
]
End[]
EndPackage[]
