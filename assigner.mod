

set P;
set D;

param prefs {P, D};

var decision {P, D} binary;

minimize Cost:
	sum {p in P, d in D}
		decision[p, d] * prefs[p, d];
		
subject to ShiftsPerPerson{p in P}:
	sum {d in D}
		decision[p, d] = 2;
		
subject to PeoplePerShift{d in D}:
	3 <=
	sum {p in P} decision[p, d];