def nurse_scheduling(n, d, a, b, f):
    work = [ [1,2,3,4] for i in range(n) ]
    for i in range(n):
        available_days = [x for x in range(1, d + 1) if x not in f[i]]
        for j in range(len(available_days)):
            day = available_days[j]
            if len(work[i]) < b:
                break
            if 4 not in work[i][:b]:
                work[i] = work[i][b:]
            else:
                night_shifts = work[i][:b].count(4)
                work[i] = [0] * (night_shifts) + work[i][night_shifts + b - a:]
            if day > 1 and work[i][0] > 0:
                work[i][0] -= 1
    max_night_shifts = max([x.count(4) for x in work])
    return max_night_shifts


n = 9
d = 5
a = 1
b = 3
f = [[], [4], [], [], [], [], [], [5], []]
work = [1,2,3,4]

print(nurse_scheduling(n, d, a, b, f))
