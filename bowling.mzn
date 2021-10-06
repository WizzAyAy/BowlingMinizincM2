include "globals.mzn";

int: score;
set of int: throws_set = 1..21;
array[throws_set] of var int: throws;
array[throws_set] of var int: bonus;

var int: nbStrike;
var int: nbSpare;

int: fixedStrikeNumber;
int: fixedSpareNumber;

bool: setStrikeBool;
bool: setSpareBool;

constraint if setStrikeBool == true then nbStrike = fixedStrikeNumber endif;
constraint if setSpareBool == true then nbSpare = fixedSpareNumber endif;

%predicates, throw : first throw of frame
predicate spare(int: throw) = throws[throw] + throws[throw+1] = 10 /\ throws[throw] < 10;
predicate strike(int: throw) = throws[throw] = 10;

constraint score <= 300 /\ score >= 0;

%bonus >= 0
constraint forall(i in throws_set)(
  bonus[i] >= 0
);

%0 to 10 pins per throw
constraint forall(i in throws_set)(
  throws[i] <= 10 /\
  throws[i] >= 0
);

%0 to 10 pins per frame
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 18)(
  throws[i] + throws[i+1] <= 10 /\
  throws[i] + throws[i+1] >= 0
);
/*
%except for the last frame
constraint 
  throws[19] + throws[20] <= 20 /\ 
  throws[19] + throws[20] >= 0;
  */

%if last frame, first throw not spare or strike, second throw -> normal throws
constraint (throws[19] < 10) -> throws[19] + throws[20] <= 10;

%spares
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 19)(
  spare(i) -> bonus[i] = throws[i+2]
);
constraint spare(19) -> bonus[19] = throws[21];

%strikes
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 17)(
  (strike(i) /\ not strike(i+2)) -> bonus[i] = throws[i+2] + throws[i+3] %simple strike
);
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 17)(
  (strike(i) /\ strike(i+2)) -> bonus[i] = throws[i+2] + throws[i+4] %double strike
);
constraint strike(19) -> bonus[19] = throws[20] + throws[21];

%strike means 0 for second 'throw'
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 18)(%18 cause last 3 throws can all be strikes
  (throws[i] = 10) -> throws[i+1] = 0
);

%no bonus points without spare or strike
constraint forall(i in throws_set where i mod 2 = 1 /\ i <= 20)(
  (not strike(i) /\ not spare(i)) -> bonus[i] = 0
);

%no bonus at all on second throws
constraint forall(i in throws_set where i mod 2 = 0)(
  bonus[i] = 0
);
%or last throw
constraint bonus[21] = 0;

%last throw only if spare or strike
constraint (not strike(19) /\ not spare(19)) -> throws[21] = 0;

%if 19 = 0 then 20,21 = 0

constraint throws[19] = 10 -> score = sum(i in 1..19)(throws[i]) + sum(bonus);
constraint throws[19] < 10 -> score = sum(i in 1..20)(throws[i]) + sum(bonus);

constraint nbStrike = sum(i in 1..19 where i mod 2 = 1)(bool2int(strike(i))) 
 + bool2int(strike(20)) + bool2int(strike(21));

constraint nbSpare = sum(i in 1..19 where i mod 2 = 1)(bool2int(spare(i)));

solve :: int_search(throws, first_fail, indomain_max, complete) satisfy;

output
[show(throws[i]) ++ "|" ++ show(throws[i+1])  ++ " + " ++ show(bonus[i]) ++ "\n" | i in 1..19 where i mod 2 = 1]
++
["Bonus finale : " ++ show(throws[21]) ++ "\n"]
++
["Score = " ++ show(score) ++ "\n"]
++
["nbStrike = " ++ show(nbStrike) ++ "\n"]
++
["nbSpare = " ++ show(nbSpare) ++ "\n"];


