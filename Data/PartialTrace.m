  BeginPackage[ "PartialTrace`"]

  TraceSystem::usage = 
	"MainFunction[ x] computes a simple function."

  Begin[ "Private`"]

SwapParts[expr_, pos1_, pos2_] := 
 ReplacePart[#, #, {pos1, pos2}, {pos2, pos1}] &[expr]
TraceSystem[D_, s_] := (
  
  Qubits = Reverse[Sort[s]];
  TrkM = D;
  
  z = (Dimensions[Qubits][[1]] + 1);
  
  For[q = 1, q < z, q++,
   n = Log[2, (Dimensions[TrkM][[1]])];
   M = TrkM;
   k = Qubits[[q]];
   If[k == n,
    TrkM = {};
    For[p = 1, p < 2^n + 1, p = p + 2,
     TrkM = 
       Append[TrkM, 
        Take[M[[p, All]], {1, 2^n, 2}] + 
         Take[M[[p + 1, All]], {2, 2^n, 2}]];
      ],
    For[j = 0, j < (n - k), j++,
      b = {0};
      For[i = 1, i < 2^n + 1, i++,
       If[(Mod[(IntegerDigits[i - 1, 2, n][[n]] + 
              IntegerDigits[i - 1, 2, n][[n - j - 1]]), 2]) == 1 && 
         Count[b, i]  == 0, 
        Permut = {i, (FromDigits[
             SwapParts[(IntegerDigits[i - 1, 2, n]), {n}, {n - j - 
                1}], 2] + 1)};
        b = 
         Append[b, (FromDigits[
             SwapParts[(IntegerDigits[i - 1, 2, n]), {n}, {n - j - 
                1}], 2] + 1)];
        c = Range[2^n];
        perm = 
         SwapParts[
          c, {i}, {(FromDigits[
              SwapParts[(IntegerDigits[i - 1, 2, n]), {n}, {n - j - 
                 1}], 2] + 1)}];
        
        M = M[[perm, perm]];
        
         ]    
       ]         ;
      TrkM = {};
      For[p = 1, p < 2^n + 1, p = p + 2,
       TrkM = 
         Append[TrkM, 
          Take[M[[p, All]], {1, 2^n, 2}] + 
           Take[M[[p + 1, All]], {2, 2^n, 2}]];
       ]
         ];
    ]
   
   ]
  
  ; Return[TrkM])

  End[]

  EndPackage[]
