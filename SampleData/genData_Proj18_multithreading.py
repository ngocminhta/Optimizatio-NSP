import random as rd
import threading
import time

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
 
t = time.time()               
t0 = threading.Thread(target=genData('0.txt',10,6,1,4))
t1 = threading.Thread(target=genData('1.txt',15,15,1,7))
t2 = threading.Thread(target=genData('2.txt',20,15,3,8))
t3 = threading.Thread(target=genData('3.txt',25,20,3,10))
t4 = threading.Thread(target=genData('4.txt',25,25,3,12))
t5 = threading.Thread(target=genData('5.txt',30,35,5,20))
t6 = threading.Thread(target=genData('6.txt',35,50,5,20))
t7 = threading.Thread(target=genData('7.txt',50,45,5,25))
t8 = threading.Thread(target=genData('8.txt',50,55,8,25))
t9 = threading.Thread(target=genData('9.txt',60,60,10,30))

t0.start()
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()

# t0.join()
# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()
# t7.join()
# t8.join()
# t9.join()

print ("GenData has completed in ", time.time()- t)


