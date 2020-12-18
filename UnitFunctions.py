# Wrapped Functions for Unit Integration
def log10(value, unitOveride = False):
    "Takes a unitless value and returns the log10 in scalar form"
    if (not value.innerGunk.isDimensionless()) or unitOveride:
        raise UnitException('Log', value.printUnits(), unitOveride)

    newVal = np.log10(value.innerGunk.scalar)
    return newVal



def log(value, unitOveride = False):
    "Takes a unitless value and returns the natural log in scalar form"
    if (not value.innerGunk.isDimensionless()) or unitOveride:
        raise UnitException('Natural Log', value.printUnits(), unitOveride)

    newVal = np.log(value.innerGunk.scalar)
    return newVal



def exp(value, unitOveride = False):
    "Takes a unitless value and returns the e^value in scalar form"
    if (not value.innerGunk.isDimensionless()) or unitOveride:
        raise UnitException('exp', value.printUnits(), unitOveride)

    return np.exp(value.innerGunk.scalar)



def fsolveU(func, guess, arguments = ()):
    "Standard fsolve that can handle functions that take/return units. Multi-dimension supported"
    try:
        func(guess, *arguments)
    except:
        raise Exception('Couldn\'t compute function')

    guessUnit = 1

    if type(guess) == type(UUU('')):
        guessUnit = UUU(guess.innerGunk.topUnit, guess.innerGunk.bottomUnit)
        guess = guess.getNum()

    elif type(guess) == type(list()):
        guessUnit = []
        temp = []

        for i in range(len(guess)):
            if type(guess[i]) == type(UUU('')):
                guessUnit.append(UUU(guess[i].innerGunk.topUnit, guess[i].innerGunk.bottomUnit))
                guess[i] = guess[i].getNum()

            else:
                guessUnit.append(1)

    def newFunc(guess):
        guess = guess * guessUnit
        funcReturn = func(guess, *arguments)
        ans = []
        for i in range(len(guess)):
            if type(funcReturn[i]) == type(UUU('')):
                ans.append(funcReturn[i].getNum())
            else:
                ans.append(funcReturn)

        return ans

    num = fsolve(newFunc, guess)
    ans = num * guessUnit
    return ans




def quadU(func, lowerBound, upperBound, arguments = ()):
    "Standard quad that can handle functions that take/return units"
    try:
        func(lowerBound, *arguments)
    except:
        raise Exception('Couldn\'t compute function')

    returnUnit = func(lowerBound, *arguments) * lowerBound
    returnUnit = UUU(returnUnit.innerGunk.topUnit, returnUnit.innerGunk.bottomUnit)

    boundUnit = 1

    if type(lowerBound) == type(UUU('')):
        lowerBound = lowerBound.getNum()
        upperBound = upperBound.getNum()
        boundUnit = UUU(lowerBound.innerGunk.topUnit, lowerBound.innerGunk.bottomUnit)

    def newFunc(x):
        x = x * boundUnit
        funcReturn = func(x, *arguments)
        return funcReturn.getNum()

    num = quad(newFunc, lowerBound, upperBound)[0]
    return num * returnUnit




def plot(X, Y, option = None, label = ''):
    "Standard plt.plot that can handle functions that take/return units."
    Xscalar = np.zeros(len(X))
    xSample = X[0]

    for i in range(len(X)):
        Xscalar[i] = X[i].getNum()

    Yscalar = np.zeros(len(Y))
    for i in range(len(Y)):
        Yscalar[i] = Y[i].getNum()

    ySample = Y[0]
    Y = Yscalar
    X = Xscalar
    if option != None:
        plt.plot(X, Y, option, label = label)
    else:
        plt.plot(X,Y, label = label)
    plt.xlabel(f"({xSample.printUnits()})")
    plt.ylabel(f"({ySample.printUnits()})")
    plt.legend()
    return

