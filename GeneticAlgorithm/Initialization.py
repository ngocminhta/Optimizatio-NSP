import numpy as np
import pandas as pd

class NurseSchedulingProblem:
    def __init__(self, hardConstraintPenalty, N, D, alpha, beta, dayoff):
        self.hardConstraintPenalty = hardConstraintPenalty
        self.N = N  # number of nurses
        self.D = D  # number of days
        self.alpha = alpha  # min number of nurses in each shift
        self.beta = beta  # max number of nurses in each shift
        self.dayoff = dayoff
        self.nurses = [str(i) for i in range(1, N + 1)]

    def __len__(self):
        return self.N * self.D * 4

    def getCost(self, schedule):
        nurseShiftsDict = self.getNurseShifts(schedule)
        maxShiftDayviolations = self.maxShifts_inAday(nurseShiftsDict)
        nightShiftsviolations = self.nightShifts_condition(nurseShiftsDict)
        numberNursesPerShift = self.countNursesPerShiftViolations(nurseShiftsDict)
        dayoffConditions = self.dayoffCondition(nurseShiftsDict)
        
        fitnesstmp = []
        for n in range(self.N):
            tmp = 0
            for d in range(self.D):
                tmp += schedule[4*self.D*n + 4*d + 3]
            fitnesstmp.append(tmp)
            
        maxNightShift = max(fitnesstmp)
        
        constraintViolations = (
            maxShiftDayviolations
            + nightShiftsviolations
            + numberNursesPerShift
            + 2 * dayoffConditions
            + 5 * maxNightShift
        )
        
        return self.hardConstraintPenalty * constraintViolations

    def dayoffCondition(self, nurseShiftDict):
        violations = 0
        for i_shift, nurseShifts in enumerate(nurseShiftDict.values()):
            for i_nurse_shift in range(len(nurseShifts)):
                if (
                    nurseShifts[i_nurse_shift] == 1
                    and i_nurse_shift // 4 in self.dayoff[i_shift]
                ):
                    violations += 1

        return violations

    def getNurseShifts(self, schedule):
        # return a dictionary with each nurse as a key
        nurseShiftsDict = {}
        shiftIndex = 0
        for nurse in self.nurses:
            nurseShiftsDict[nurse] = schedule[shiftIndex : shiftIndex + 4 * self.D]
            shiftIndex += 4 * self.D
        return nurseShiftsDict

    def maxShifts_inAday(
        self, nurseShiftsDict
    ):  # in a day, a nurse can work at most 1 ca
        violations = 0

        for nurseShifts in nurseShiftsDict.values():
            for i in range(0, self.D * 4, 4):
                dailyShifts = sum(nurseShifts[i : i + 4])
                if dailyShifts > 1:
                    violations += 1
        return violations

    def nightShifts_condition(self, nurseShiftDict):
        violations = 0
        for nurseShifts in nurseShiftDict.values():
            for i in range(0, (self.D - 1) * 4, 4):
                if nurseShifts[i + 3] == 1 and sum(nurseShifts[i + 4 : i + 8]) >= 1:
                    violations += 1
        return violations

    def countNursesPerShiftViolations(self, nurseShiftsDict):
        violations = 0

        for i in zip(*nurseShiftsDict.values()):
            if sum(i) < self.alpha or sum(i) > self.beta:
                violations += 1
        return violations

    def printScheduleInfo(self, schedule):
        # Print the schedule and violations details
        nurseShiftsDict = self.getNurseShifts(schedule)
        """print("Schedule for each nurse:")
        for nurse in nurseShiftsDict:
            print(nurse, ":", nurseShiftsDict[nurse])
        print(
            "max shift in a day violations = ", self.maxShifts_inAday(nurseShiftsDict)
        )
        print()
        print("night shift violations = ", self.nightShifts_condition(nurseShiftsDict))
        print()
        print(
            "number nurse per shift violations = ",
            self.countNursesPerShiftViolations(nurseShiftsDict),
        )"""
        res = [[0 for n in range(self.N)] for d in range(self.D)]
        for n in range(self.N):
            for d in range(self.D):
                for s in range(4):
                    if schedule[4*self.D*n + 4*d + s] == 1:
                        res[d][n] = s
        df = pd.DataFrame(res, index = [d+1 for d in range(self.D)], columns = [n+1 for n in range(self.N)])
        df.index.name = 'Nurse'
        df.columns.name = 'Day'
        display(df)
        #print(df)

def main():
    # create a problem instance:
    nurses = NurseSchedulingProblem(10, 4, 2, 1, 2)
    randomSolution = np.random.randint(2, size=len(nurses))
    print("Random Solution = ")
    print(randomSolution)
    print()
    print(nurses.getCost(randomSolution))
    print()
    print(nurses.printScheduleInfo(randomSolution))


if __name__ == "__main__":
    main()
