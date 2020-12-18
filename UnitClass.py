from .ConversionTools import *
def Unit(Before, After = 'SI', returnUnits = False):    
    preBefore = ''
    preAfter  = ''
    returnUnitsTwo = False
    
    #Process with Before Prefix
    if Before.find('_') != -1:
        preBefore, Before = Before.split('_')
    
    #Define After for SI default
    if After == 'SI':
        After = SI[UnitType[Before]]
        returnUnitsTwo = True
    
    #Process with After Prefix
    if After.find('_') != -1:
        preAfter, After = After.split('_')
    
    #Check Unit Consistency
    if (UnitType[Before] != UnitType[After]):
        return 'Inconsistent Units'
    
    #Returns Numerical Answer Depending on Unit Return Request
    
    #Returns Numerical Answer and Units Parsed Into Base Units
    if (returnUnits and returnUnitsTwo): # or (Before == After):
        numericalAns = ConvertType[UnitType[Before]](Before, After) * UnitPrefix[preBefore] / UnitPrefix[preAfter]
        if preAfter != '':
            preAfter += '_'
        topUnits = SITop[(preAfter + After)]
        bottomUnits = SIBottom[preAfter + After]
        return [numericalAns, topUnits, bottomUnits]
    
    #Returns Numerical Answer and After Units
    elif returnUnits:
        numericalAns = ConvertType[UnitType[Before]](Before, After) * UnitPrefix[preBefore] / UnitPrefix[preAfter]
        return [numericalAns, After]
    
    #Returns Numerical Answer
    else:
        return ConvertType[UnitType[Before]](Before, After) * UnitPrefix[preBefore] / UnitPrefix[preAfter]


# ## Unit Exceptions

class UnitException(Exception):
    def __init__(self, operation, unitOne, unitTwo):
        return


# ## Unit Analysis

class ComplexUnits():
    def __init__(self, num, topUnit = '', bottomUnit = '', dontConvert = False):
        if dontConvert:
            self.scalar = num
            self.topUnit = topUnit
            self.bottomUnit = bottomUnit
        
        if(type(topUnit) == list or type(bottomUnit) == list):
            topUnit, bottomUnit = self.combineUnits(topUnit, bottomUnit)
            self.topUnit, self.bottomUnit = self.clearEmpty(topUnit, bottomUnit)
            self.scalar = num
            self.topUnit.sort()
            self.bottomUnit.sort()
            
        else:
            topUnit = list(topUnit.split('*'))    
            bottomUnit = list(bottomUnit.split('*'))
            topUnit, bottomUnit = self.expandPowerInit(topUnit, bottomUnit)
            topUnit, bottomUnit = self.clearEmpty(topUnit, bottomUnit)
            topUnit, bottomUnit, num = self.convertToSI(topUnit, bottomUnit, num)
            topUnit, bottomUnit = self.clearEmpty(topUnit, bottomUnit)
            topUnit, bottomUnit = self.expandPower(topUnit, bottomUnit)
            topUnit, bottomUnit = self.combineUnits(topUnit, bottomUnit)
            self.topUnit, self.bottomUnit = self.clearEmpty(topUnit, bottomUnit)
            self.scalar = num
            self.topUnit.sort()
            self.bottomUnit.sort()
            
            
        return
    
    def newUnit(self, topUnit, bottomUnit, doubleList = False):
        self.topUnit.clear()
        if doubleList:
            for i in topUnit:
                for j in i:
                    self.topUnit.append(j)
        else:
            for i in topUnit:
                self.topUnit.append(i)
        
        self.bottomUnit.clear()
        if doubleList:
            for i in bottomUnit:
                for j in i:
                    self.bottomUnit.append(j)
        else:
            for i in bottomUnit:
                self.bottomUnit.append(i)
    
    def convertToSI(self, topUnit, bottomUnit, num):
        topUnitTemp = list()
        bottomUnitTemp = list()
        
        for i in topUnit:
            if (i == ''):
                continue    
            conversion = Unit(i[0], returnUnits = True)
            num *= conversion[0]**i[1]
            top  = conversion[1].split('*')
            bottom=conversion[2].split('*')
            
            for j in top:
                topUnitTemp.append([j, i[1]])
            for j in bottom:
                bottomUnitTemp.append([j, i[1]])
                
        for i in bottomUnit:
            if i == '':
                continue
                
            conversion = Unit(i[0], returnUnits = True)
            num /= conversion[0]
            
            bottom=conversion[1].split('*')
            top  = conversion[2].split('*')
            
            for j in top:
                topUnitTemp.append([j, i[1]])
            for j in bottom:
                bottomUnitTemp.append([j, i[1]])
            
        return topUnitTemp, bottomUnitTemp, num

    
    def convertTo(self, newUnitTop = '', newUnitBottom = ''):
        topUnit = newUnitTop.split('*')
        bottomUnit = newUnitBottom.split('*')
        
        self.topUnit, self.bottomUnit, toSIRatio= self.convertToSI(self.topUnit, self.bottomUnit, 1)
        self.topUnit, self.bottomUnit = self.clearEmpty(self.topUnit, self.bottomUnit)
        self.topUnit, self.bottomUnit = self.expandPower(self.topUnit, self.bottomUnit)
        
        topUnit, bottomUnit = self.expandPowerInit(topUnit, bottomUnit) 
        topUnit, bottomUnit = self.clearEmpty(topUnit, bottomUnit)
        
        topSI, bottomSI, toNewRatio = self.convertToSI(topUnit, bottomUnit, 1)
        topSI, bottomSI = self.expandPower(topSI, bottomSI)
        topSI, bottomSI = self.combineUnits(topSI, bottomSI)            
        topSI, bottomSI = self.clearEmpty(topSI, bottomSI)
        
        topSI = sorted(topSI, key= lambda unit: unit[0])
        bottomSI = sorted(bottomSI, key= lambda unit: unit[0])
        self.topUnit = sorted(self.topUnit, key= lambda unit: unit[0])
        self.bottomUnit = sorted(self.bottomUnit, key= lambda unit: unit[0])
                
        if topSI != self.topUnit or bottomSI != self.bottomUnit:
            raise UnitException('Conversion', f'{self.topUnit} / {self.bottomUnit}', f'{topSI} / {bottomSI}')
            return
        
        self.scalar = self.scalar * toSIRatio / toNewRatio
        self.topUnit = topUnit
        self.bottomUnit = bottomUnit
        
        return #ComplexUnits(self.scalar * toSIRatio / toNewRatio, topUnit, bottomUnit, True)
        
    def expandPowerInit(self, topUnit, bottomUnit):
        topUnitTemp = list()
        
        for i in topUnit:
            if (i.find('^') == -1):
                topUnitTemp.append(list([i, 1]))
                continue
                
            unit, power = i.split('^')
            power = float(power)
            topUnitTemp.append(list([unit, power]))
        
        bottomUnitTemp = list()
        for i in bottomUnit:
            if (i.find('^') == -1):
                bottomUnitTemp.append(list([i, 1]))
                continue
            
            unit, power = i.split('^')
            power = float(power)
            bottomUnitTemp.append(list([unit, power]))
       
        return topUnitTemp, bottomUnitTemp
    
    def expandPower(self, topUnit, bottomUnit):
        topUnitTemp = list()
        
        for i in topUnit:
            if (i[0].find('^') == -1):
                topUnitTemp.append(list([i[0], i[1]]))
                continue
                
            unit, power = i[0].split('^')
            power = float(power)
            topUnitTemp.append(list([unit, power*i[1]]))
        
        bottomUnitTemp = list()
        for i in bottomUnit:
            if (i[0].find('^') == -1):
                bottomUnitTemp.append(list([i[0], i[1]]))
                continue
                
            unit, power = i[0].split('^')
            power = float(power)
            bottomUnitTemp.append(list([unit, power*i[1]]))
       
        return topUnitTemp, bottomUnitTemp
    
    
    def combineUnits(self, topUnit, bottomUnit):
        itemsRemovedTop = 0
        itemsRemovedBottom = 0
        for i in range(len(topUnit)):
            i -= itemsRemovedTop
            for j in range(len(bottomUnit)):
                j -= itemsRemovedBottom
                if topUnit[i][0] == bottomUnit[j][0]:
                    if topUnit[i][1] > bottomUnit[j][1]:
                        topUnit[i][1] -= bottomUnit[j][1]
                        bottomUnit.remove(bottomUnit[j])
                        itemsRemovedBottom += 1
                        
                    elif topUnit[i][1] < bottomUnit[j][1]:
                        bottomUnit[j][1] -= topUnit[i][1]
                        topUnit.remove(topUnit[i])
                        itemsRemovedTop += 1
                        break
                                      
                    else:
                        bottomUnit.remove(bottomUnit[j])
                        topUnit.remove(topUnit[i])
                        itemsRemovedTop += 1
                        break
                        
        itemsRemoved = 0
        for i in range(len(topUnit)):
            i -= itemsRemoved
            for j in range(len(topUnit)):
                if i == j:
                    continue
                if topUnit[i][0] == topUnit[j][0]:
                    topUnit[i][1] += topUnit[j][1]
                    topUnit.remove(topUnit[j])
                    itemsRemoved += 1
                    break
            
        itemsRemoved = 0
        for i in range(len(bottomUnit)):
            i -= itemsRemoved
            for j in range(len(bottomUnit)):
                if i == j:
                    continue
                if bottomUnit[i][0] == bottomUnit[j][0]:
                    bottomUnit[i][1] += bottomUnit[j][1]
                    bottomUnit.remove(bottomUnit[j])
                    itemsRemoved += 1
                    break
            
        return topUnit, bottomUnit
    
    def clearEmpty(self, topUnit, bottomUnit):
        itemsRemoved = 0;
        for i in range(len(topUnit)):
            if(len(topUnit[i - itemsRemoved][0]) == 0):
                topUnit.remove(topUnit[i-itemsRemoved])
                itemsRemoved +=1
                
        itemsRemoved = 0;
        for i in range(len(bottomUnit)):
            if(len(bottomUnit[i - itemsRemoved][0]) == 0):
                bottomUnit.remove(bottomUnit[i - itemsRemoved])
                itemsRemoved +=1
                
        return topUnit, bottomUnit
    
    def __add__(self, other):
        
        if self.isDimensionless() and type(other) != type(self):
            newTerm = ComplexUnits(self.scalar + other, self.topUnit, self.bottomUnit)
            
        elif not self.isDimensionallyConsistent(other):
            raise UnitException('Addition', f'{self.topUnit} / {self.bottomUnit}', f'{other.topUnit} / {other.bottomUnit}')
        
        elif type(self) == type(other):
            newTerm = ComplexUnits(self.scalar + other.scalar, self.topUnit, self.bottomUnit)
            
        return newTerm
    
    def __sub__(self,other):
        
        if type(other) == type(self):
            negative = ComplexUnits(other.scalar * -1, other.topUnit, other.bottomUnit)
        
        else:
            negative = -1 * other
        
        return self + negative
    
    def __mul__(self,other):
        if type(other) == type(self):
            topUnit = list()
            bottomUnit = list()
            
            for i in range(len(self.topUnit)):
                topUnit.append(list())
                topUnit[i].append(self.topUnit[i][0])
                topUnit[i].append(self.topUnit[i][1])
                
            for i in range(len(self.bottomUnit)):
                bottomUnit.append(list())
                bottomUnit[i].append(self.bottomUnit[i][0])
                bottomUnit[i].append(self.bottomUnit[i][1])
            
            for i in range(len(other.topUnit)):
                j = i + len(self.topUnit)
                topUnit.append(list())
                topUnit[j].append(other.topUnit[i][0])
                topUnit[j].append(other.topUnit[i][1])
                
            for i in range(len(other.bottomUnit)):
                j = i + len(self.bottomUnit)
                bottomUnit.append(list())
                bottomUnit[j].append(other.bottomUnit[i][0])
                bottomUnit[j].append(other.bottomUnit[i][1])
            
            newTerm = ComplexUnits(self.scalar * other.scalar, topUnit, bottomUnit)
            return newTerm
        
        else:
            newTerm = ComplexUnits(self.scalar * other, self.topUnit, self.bottomUnit)
            return newTerm            
    
    def __truediv__(self, other):
        topUnit = other.bottomUnit
        bottomUnit = other.topUnit
        
        recipricol = ComplexUnits(other.scalar**-1,topUnit,bottomUnit)
        
        return self * recipricol
    
    def __rtruediv__(self, other):
        topUnit = self.bottomUnit
        bottomUnit = self.topUnit
        
        recipricol = ComplexUnits(self.scalar**-1, topUnit, bottomUnit)
        return recipricol * other
    
    def __pow__(self, other):
        
        
        if(self.isDimensionless()):
            newTerm = ComplexUnits(self.scalar**other, self.topUnit, self.bottomUnit)
            return newTerm
        
        elif other > 0:
            
            topUnit = list()
            bottomUnit  = list()
            
            for i in range(len(self.topUnit)):
                topUnit.append(list())
                topUnit[i].append(self.topUnit[i][0])
                topUnit[i].append(self.topUnit[i][1])
                topUnit[i][1] *= other
                
            for i in range(len(self.bottomUnit)):
                bottomUnit.append(list())
                bottomUnit[i].append(self.bottomUnit[i][0])
                bottomUnit[i].append(self.bottomUnit[i][1])
                bottomUnit[i][1] *= other

            scalar = self.scalar**other
            return ComplexUnits(scalar, topUnit, bottomUnit)
        
        elif other < 0:
            other *= -1
            newSelf = 1 / self
            return newSelf**other
        
        elif other == 0:
            return self / self
        
        else:
            raise Exception('Fractional Powers Not Yet Supported')
    
    def __str__(self):
        return self.toString()
        
    def toString(self):
        return str(self.scalar) +  str(self.topUnit) + str(self.bottomUnit)
    
    def __printUnits__(self):
        
        stringTop = ''
        for i in self.topUnit:
            stringTop += f"{(str(i[0]) + '^' + str(i[1])) if i[1] != 1 else i[0]} "
        
        stringBottom = ''
        for i in self.bottomUnit:
            stringBottom += f"{(str(i[0]) + '^' + str(i[1])) if i[1] != 1 else i[0]} "
        
        finalString = f"{stringTop}{'/ ' if stringBottom != '' else ''}{stringBottom}"
        finalString = finalString.replace('_','')
        
        return finalString
    
    def prettyPrint(self):
        return f"{self.scalar*1.0:.5} {self.__printUnits__()}"            
    
    def isDimensionallyConsistent(self, other):
        return self.topUnit==other.topUnit and self.bottomUnit==other.bottomUnit
    
    def isDimensionless(self):
        return len(self.topUnit) == 0 and len(self.bottomUnit) == 0


class UUU():
    def __init__(self, topUnit = "", bottomUnit = "", existingTerm = "", num = 1):
        if existingTerm != '':
            self.innerGunk = existingTerm
        else:
            self.innerGunk = ComplexUnits(num, topUnit, bottomUnit)
        return
    
    def __add__(self, other):
        if type(self) == type(other):
            calc = self.innerGunk + other.innerGunk
        else:
            calc = self.innerGunk + other
            
        newTerm = UUU(existingTerm = calc)
        return newTerm
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self,other):
        if type(self) == type(other):
            calc = self.innerGunk - other.innerGunk
        else:
            calc = self.innerGunk - other
        newTerm = UUU(existingTerm = calc)
        return newTerm
    
    def __rsub__(self, other):
        return self * -1 + other
    
    def __mul__(self,other):
        if type(other) == type(self):
            calc = self.innerGunk * other.innerGunk
            newTerm = UUU(existingTerm = calc)
            return newTerm
        
        else:
            calc = self.innerGunk * other
            newTerm = UUU(existingTerm = calc)
            return newTerm
        
    def __rmul__(self,other):
        if type(other) == type(self):
            calc = self.innerGunk * other.innerGunk
            newTerm = UUU(existingTerm = calc)
            return newTerm
        else:
            calc = self.innerGunk * other
            newTerm = UUU(existingTerm = calc)
        return newTerm    

    
    def __truediv__(self, other):
        if type(other) == type(self):
            calc = self.innerGunk / other.innerGunk
            newTerm = UUU(existingTerm = calc)
            return newTerm
        
        else:
            calc = self.innerGunk * other**-1
            newTerm = UUU(existingTerm = calc)
            return newTerm
        
    def __rtruediv__(self, other):
        calc = other / self.innerGunk
        newTerm = UUU(existingTerm = calc)
        return newTerm
    
    def __pow__(self, other):
        calc = self.innerGunk**other
        newTerm = UUU(existingTerm = calc)
        return newTerm
    
    def __neg__(self):
        calc = self.innerGunk * -1
        return UUU(existingTerm = calc)
    
    def __str__(self):
        return self.prettyPrint()
    
    def __float__(self):
        if self.innerGunk.isDimensionless():
            return self.innerGunk.scalar
        
        else:
            raise Exception('Cannot convert Unit Class to a Float')

    
    def __int__(self):
        if self.innerGunk.isDimensionless and (self.innerGunk.scalar % 1 == 0):
            return int(self.innerGunk.scalar)
        
        else:
            raise Exception('Cannot convert Unit Class to an Integer')
     
    def toString(self):
        return self.innerGunk.toString()
    
    def getNum(self):
        return self.innerGunk.scalar
    
    def prettyPrint(self):
        return self.innerGunk.prettyPrint()
    
    def printUnits(self):
        return self.innerGunk.__printUnits__()
    
    def convertTo(self, newUnitTop = '', newUnitBottom = ''):
        return UUU(existingTerm = self.innerGunk.convertTo(newUnitTop, newUnitBottom))


