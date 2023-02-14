def nurse_scheduling_backtracking(n, d, a, b, f):
    work = [ [1,2,3,4] for i in range(n) ]
    shifts = [0] * n
    def backtrack(day):
        if day == d + 1:
            return True
        available_nurses = [i for i in range(n) if day not in f[i]]
        for i in range(len(available_nurses)):
            nurse = available_nurses[i]
            if shifts[nurse] >= b:
                continue
            for j in range(len(work[nurse])):
                shift = work[nurse][j]
                if shift == 4 and shifts[nurse] >= a:
                    continue
                shifts[nurse] += 1
                work[nurse].pop(j)
                if day > 1 and shift == 4:
                    work[nurse].insert(0, 0)
                if backtrack(day + 1):
                    return True
                work[nurse].insert(j, shift)
                shifts[nurse] -= 1
        return False
    backtrack(1)
    max_night_shifts = max(shifts)
    return max_night_shifts

n = 9
d = 5
a = 1
b = 3
f = [[], [4], [], [], [], [], [], [5], []]
work = [1,2,3,4]

print(nurse_scheduling_backtracking(n, d, a, b, f))
