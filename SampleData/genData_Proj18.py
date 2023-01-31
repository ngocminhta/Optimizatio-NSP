import random as rd

def genData(filename,N,D,a,b):
    valid = [[-1 for i in range(N)] for i in range(D)]
    d = -1
    
    while any(-1 in nested_list for nested_list in valid):
        d += 1
        if d >= D:
            d = 0
        i = 0
        while not ((a <= valid[d].count(1) <= b) and (a <= valid[d].count(2) <= b) and (a <= valid[d].count(3) <=  b) and (a <= valid[d].count(4) <= b)):                
            i = 0    
            while i < N-1:
                if valid[d-1][i] != 4 or d == 0:
                    valid[d][i] = rd.randint(1,4)
                else:
                    valid[d][i] = 0
                if valid[d][i] == 4:
                    valid[d][i+1] = 0
                    i += 1
                i += 1
            valid[d][N-1] = rd.randint(1,4)
    
    res = [[]for i in range(N)]
    for j in range(N):
        for i in range(D):
            if valid[i][j] == 0:
                res[j].append(i+1)
        res[j].append(-1)
        
    with open(filename,'w') as f:
        f.write(str(N) + ' ' + str(D) + ' ' + str(a) + ' ' + str(b) + '\n')
        for nlist in res:
            f.write(' '.join(map(str,nlist)) + '\n')
            
    with open('sol'+filename, 'w') as f2:
        f2.write('The given result is written in the table form with column is day d, the row is Employee n. And the value[d][n] is the shift assigned.\n\n')
        for nlist in valid:
            f2.write(' '.join(map(str,nlist)) + '\n')
        
genData('99.txt',4,2,1,2)