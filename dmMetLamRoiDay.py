from PyCBLS.VarIntLS import VarIntLS
from PyCBLS.LocalSearchManager import LocalSearchManager
from PyCBLS.NotEqual import NotEqual
from PyCBLS.MustEqual import MustEqual
from PyCBLS.ConstraintSystem import ConstraintSystem
from PyCBLS.HillClimbingSearch import HillClimbingSearch
from PyCBLS.ConditionalSumWithBound2 import ConditionalSumWithBound
import random as rd
import pandas as pd

# print solution
def printSolution():
    for d in range(D):
        for n in range(N):
            print(assign[d][n].getValue(), end = ' ')
        print('')

#--------start code
mgr = LocalSearchManager()

# read data from file
with open('/Users/ngocminhta/Optimization-NSP/SampleData/testCase1/0.txt') as file:
  N, D, a, b = [int(q) for q in file.readline().split()]
  dayoff = [[0 for d in range(D)] for n in range(N)]
  for n in range(N):
    for d in [int(h) for h in file.readline().split()]:
      if d != -1:
            dayoff[n][d-1] = 1

# define decision variable
assign = [[VarIntLS(mgr,0,3,rd.randint(1, 4),f'assign_{n}_{d}') for n in range(N)] for d in range(D)]

mor = VarIntLS(mgr,1,1,1,'mor')
aft = VarIntLS(mgr,2,2,2,'aft')
eve = VarIntLS(mgr,3,3,3,'eve')
nig = VarIntLS(mgr,4,4,4,'nig')
shifts = [mor, aft, eve, nig]

zero = VarIntLS(mgr,0,0,0,'zero')
#a = VarIntLS(mgr,a,a,a,'a')
#b = VarIntLS(mgr,b,b,b,'b')

constraints = []

# set the given dayoff
for n in range(N):
    for d in range(D):
        if dayoff[n][d] == 1:
            c = NotEqual(assign[d][n],mor,'NotEqual')
            constraints.append(c)
            c = NotEqual(assign[d][n],aft,'NotEqual')
            constraints.append(c)
            c = NotEqual(assign[d][n],eve,'NotEqual')
            constraints.append(c)
            c = NotEqual(assign[d][n],nig,'NotEqual')
            constraints.append(c)
        else:
            c = NotEqual(assign[d][n],zero,'NotEqual')
            constraints.append(c)

# dayoff after a night shift
for n in range(N):
    for d in range(D-1):
        c = MustEqual(assign[d-1][n], nig, assign[d][n], zero, 'MustEqual')
        # if assign[d-1][n] == nig:
        #     c = NotEqual(assign[d][n],mor,'NotEqual')
        #     constraints.append(c)
        #     c = NotEqual(assign[d][n],aft,'NotEqual')
        #     constraints.append(c)
        #     c = NotEqual(assign[d][n],eve,'NotEqual')
        #     constraints.append(c)
        #     c = NotEqual(assign[d][n],nig,'NotEqual')
        #     constraints.append(c)
        # else:
        #     c = NotEqual(assign[d][n],zero,'NotEqual')
        #     constraints.append(c)

# A nurse assigned to only one shift - actually implemented

count = [1 for i in range(N)]
# Assign a shift has min a and max b nurse.
for d in range(D):
    #c = LessOrEqual(ConditionalSum(assign[d],count,0,'CountMor'), VarIntLS(mgr,b,b,b,'b'), 'LessOrEqual')
    c = ConditionalSumWithBound(assign[d],count,1,a,b,'CountMor')
    constraints.append(c)
    c = ConditionalSumWithBound(assign[d],count,2,a,b,'CountAft')
    constraints.append(c)
    c = ConditionalSumWithBound(assign[d],count,3,a,b,'CountEve')
    constraints.append(c)
    c = ConditionalSumWithBound(assign[d],count,4,a,b,'CountNig')
    constraints.append(c)

C = ConstraintSystem(constraints)

# close the model, init data structures representing relation between components of the model
mgr.close()

print('Init, C = ',C.violations())
answer = HillClimbingSearch(C)
answer.search(1000)

res = [[0 for n in range(N)] for d in range(D)]
for d in range(D):
    for n in range(N):
        res[d][n] = assign[d][n].getValue()
df = pd.DataFrame(res, index = [d+1 for d in range(D)], columns = [n+1 for n in range(N)])
df.index.name = 'Day'
df.columns.name = 'Nurse'
print(df)

maxNightShift = -1
for n in range(N):
    tmp = 0
    for d in range(D):
        if res[d][n] == 4:
            tmp += 1

    if tmp > maxNightShift:
        maxNightShift = tmp

print('Optimal solution - Max night shift assigned to a nurse:', maxNightShift)
