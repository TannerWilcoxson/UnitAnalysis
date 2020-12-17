import numpy             as np
import matplotlib.pyplot as plt
from scipy.optimize      import fsolve, curve_fit
from scipy.integrate     import odeint, quad

# # ChE Essentials 
# ## Ideas to Implement
# #Common ChE Values
# #Finish The Periodic Table

# # Units
# ## Ideas to Implement
# #AutoConvert Unitless to Scalar
# #Clean Complex Unit __init__ / ConvertTo (double returns)
# #Clean add/sub/mul/div
# #ConvertSI()
# #Add Comments
# #AvailableUnits() Prints a list of Currently Supported Units
# ## Unit Converter

UnitPrefix = {'Y':10**24, 'Z':10**21, 'E':10**18, 'P':10**15,                
              'T':10**12, 'G':10**9, 'M':10**6, 'k':10**3, 'h':100,                
              'da':10, '':1,'d':.1, 'c':.01, 'm':10**-3, 'μ':10**-6,                 
              'n':10**-9, 'p':10**-12, 'f':10**-15, 'a':10**-18,                 
              'z':10**-21, 'y':10**-24}

SI = {'Mass':'k_g', 'time':'s', 'Length':'m', 'Pressure':'Pa', 'Force':'N', 'Energy':'J', 'Power':'W', "Vol":'m^3', 'Temp':'K', 'Mole':'mol'}
SITop = {'k_g':'k_g', 's':'s', 'm':'m', 'Pa':'k_g',      'N':'k_g*m', 'J':'k_g*m^2', 'W':'k_g*m^2', "m^3":'m^3',    'K':'K',    'mol':'mol'}
SIBottom = {'k_g':'', 's':'',  'm':'',  'Pa':'m*s^2', 'N':'s^2',    'J':'s^2',       'W':'s^3',       "m^3":'',     'K':'',     'mol':''}

UnitType = {'g':'Mass', 'lb':'Mass', 'oz':'Mass', 'ton':'Mass', 'amu':'Mass',            
            's':'time', 'min':'time', 'h':'time', 'd':'time', 'y':'time',            
            'K':'Temp', 'R':'Temp',            
            'm':'Length', 'in':'Length', 'mil':'Length','ft':'Length', 'yard':'Length', 'mile':'Length',            
            'Pa':'Pressure', 'torr':'Pressure', 'mmHg':'Pressure', 'bar':'Pressure', 'atm':'Pressure', 'psi':'Pressure',            
            'N':'Force', 'lbf':'Force',            
            'J':'Energy', 'BTU':'Energy', 'calorie':'Energy', 'Calorie':'Energy', 'Wh':'Energy', 'eV':'Energy',            
            'W':'Power', 'Horsepower':'Power',            
            'L':'Vol', 'gal':'Vol', 'quart':'Vol', 'cup':'Vol', 'pint':'Vol', 'Tbsp':'Vol', 'tsp':'Vol', 'm^3':'Vol',            
            'mol':'Mole', 'lbmol':'Mole'}


#Divide to Convert to Noted Unit, Multiply to Convert Away From Noted Unit
MassToGrams    = {'g':1, 'lb':453.592**-1, 'oz':453.592**-1*16, 'ton':453.592**-1/2000, 'amu':6.022e+23}
TimeToSec      = {'s':1, 'min':60**-1, 'h':3600**-1, 'd':3600**-1*24**-1, 'y':3600**-1/24/365}
TempToKel      = {'K':1, 'R':1.8}
LengToMeter   = {'m':1, 'in':0.0254**-1, 'mil':0.0254**-1*1000,'ft':0.0254**-1/12, 'yard':0.0254**-1/3/12, 'mile':0.0254**-1/12/5280}
PressureToPa   = {'Pa':1, 'torr':0.00750062, 'mmHg':0.00750062, 'bar':10**-5, 'atm':101325**-1, 'psi':0.000145038}
ForceToNewton  = {'N':1, 'lbf':0.224809}
EnergyToJoule = {'J':1, 'BTU':0.000947817, 'calorie':0.239006, 'Calorie':0.239006/1000, 'Wh':0.000277778, 'eV':1.60218e-19**-1}
PowerToWatt   = {'W':1, 'Horsepower':0.00134102}
VolumeToLitre  = {'L':1, 'gal':0.264172, 'quart':1.05669, 'cup':0.236588, 'pint':0.236588*2, 'Tbsp':67.628, 'tsp':202.884, 'm^3':10**-3}
MoleToMol      = {'mol':1, 'lbmol':453.592**-1}


def ConvertMass(Before, After):
    if (UnitType[Before] !='Mass' or UnitType[After] != 'Mass'):
        return 'Inconsistent Units'
    else:
        return MassToGrams[After] / MassToGrams[Before]

def ConvertMole(Before, After):
    if (UnitType[Before] !='Mole' or UnitType[After] != 'Mole'):
        return 'Inconsistent Units'
    else:
        return MoleToMol[After] / MoleToMol[Before]

def ConvertTime(Before, After):
    if (UnitType[Before] !='time' or UnitType[After] != 'time'):
        return 'Inconsistent Units'
    else:
        return TimeToSec[After] / TimeToSec[Before]

def ConvertTemp(Before, After):
    if (UnitType[Before] !='Temp' or UnitType[After] != 'Temp'):
        return 'Inconsistent Units'
    else:
        return TempToKel[After] / TempToKel[Before]

def ConvertLength(Before, After):
    if (UnitType[Before] !='Length' or UnitType[After] !='Length'):
        return 'Inconsistent Units'
    else:
        return LengToMeter[After] / LengToMeter[Before]

def ConvertPressure(Before, After):
    if (UnitType[Before] !='Pressure' or UnitType[After] !='Pressure'):
        return 'Inconsistent Units'
    else:
        return PressureToPa[After] / PressureToPa[Before]

def ConvertForce(Before, After):
    if (UnitType[Before] !='Force' or UnitType[After] !='Force'):
        return 'Inconsistent Units'
    else:
        return ForceToNewton[After] / ForceToNewton[Before]

def ConvertEnergy(Before, After):
    if (UnitType[Before] !='Energy' or UnitType[After] !='Energy'):
        return 'Inconsistent Units'
    else:
        return EnergyToJoule[After] / EnergyToJoule[Before]

def ConvertPower(Before, After):
    if (UnitType[Before] !='Power' or UnitType[After] !='Power'):
        return 'Inconsistent Units'
    else:
        return PowerToWatt[After] / PowerToWatt[Before]

def ConvertVolume(Before, After):
    if (UnitType[Before] !='Vol' or UnitType[After] !='Vol'):
        return 'Inconsistent Units'
    else:
        return VolumeToLitre[After] / VolumeToLitre[Before]

ConvertType = {'Mass':ConvertMass, 'time':ConvertTime, 'Temp':ConvertTemp, 'Length':ConvertLength,               'Pressure':ConvertPressure, 'Force':ConvertForce, 'Energy':ConvertEnergy, 'Power':ConvertPower,               'Vol':ConvertVolume, 'Mole':ConvertMole}

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


# ## Unit Wrapper Class

# In[9]:


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


#Unit and Other Variable Definitions

g = UUU('g')
mg = UUU('m_g')
kg = UUU('k_g')
lb = UUU('lb')
oz = UUU('oz')
ton = UUU('ton')
u = UUU('amu')
s = UUU('s')
min = UUU('min')
h = UUU('h')
d = UUU('d')
y = UUU('y')
K = UUU('K')
R = UUU('R')
m = UUU('m')
mm = UUU('m_m')
cm = UUU('c_m')
km = UUU('k_m')
inch = UUU('in')
mil = UUU('mil')
ft = UUU('ft')
yd = UUU('yard')
mi = UUU('mile')
Pa = UUU('Pa')
kPa = UUU('k_Pa')
MPa = UUU('M_Pa')
GPa = UUU('G_Pa')
torr = UUU('torr')
mmHg = UUU('mmHg')
bar = UUU('bar')
mbar = UUU('m_bar')
atm = UUU('atm')
psi = UUU('psi')
N = UUU('N')
lbf = UUU('lbf')
J = UUU('J')
kJ = UUU('k_J')
J = UUU('J')
BTU = UUU('BTU')
cal = UUU('calorie')
Cal = UUU('Calorie')
Wh = UUU('Wh')
kWh = UUU('k_Wh')
eV = UUU('eV')
W = UUU('W')
kW = UUU('k_W')
MW = UUU('M_W')
hp = UUU('Horsepower')
L = UUU('L')
mL = UUU('m_L')
gal = UUU('gal')
qt = UUU('quart')
c = UUU('cup')
pt = UUU('pint')
Tbsp = UUU('Tbsp')
tsp = UUU('tsp')
mol = UUU('mol') 
lbmol = UUU('lbmol')

me = 0.000548579909 * u
mp = 1.00727647 * u
mn = 1.008664 * u
h = 6.626 * 10**-34 * J * s
Av = 6.022 * 10**23 / mol


__all__ = [
'g',
'mg',
'kg',
'lb', 
'oz', 
'ton',
'u',
's',
'min',
'h',
'd',
'y',
'K',
'R',
'm',
'mm',
'cm',
'km',
'inch', 
'mil',
'ft', 
'yd', 
'mi', 
'Pa', 
'kPa', 
'MPa',
'GPa',
'torr', 
'mmHg', 
'bar',
'mbar',
'atm',
'psi',
'N',
'lbf',
'J',
'kJ',
'J',
'BTU',
'cal',
'Cal',
'Wh',
'kWh', 
'eV', 
'W',
'kW',
'MW',
'hp',
'L',
'mL',
'gal',
'qt',
'c',
'pt',
'Tbsp',
'tsp',
'mol',
'lbmol',
'me',
'mp',
'mn', 
'h', 
'Av',
'MWU']


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
    


# # Numerical Methods

# In[13]:


a = np.zeros([9,8])       # fill in the finite difference coefficient matrix
a[4:6,0] = np.array([-1,1])
a[3:6,1] = np.array([-0.5,0,0.5])
a[3:7,2] = np.array([-1./3.,-1./2.,1.,-1./6.])
a[2:7,3] = np.array([1./12.,-2./3.,0.,2./3.,-1./12.])
a[2:8,4] = np.array([1./20.,-1./2.,-1./3.,1.,-1./4.,1./30.])
a[1:8,5] = np.array([-1./60.,3./20.,-3./4.,0,3./4.,-3./20.,1./60])
a[0:8,6] = np.array([-1./105,1./10.,-6./10.,-1./4,1,-3./10.,1./15.,-1./140.])
a[:,7]   = np.array([1./280.,-4./105.,1./5.,-4./5.,0.,4./5.,-1./5.,4./105.,-1./280.])

def finiteDifferenceMethod(order, func, x, args = (), Δx = 1e-2):
    order -= 1
    yArray = np.empty(9)
    for i in range(-4,5):
        yArray[i+4] = func(x+i*Δx, *args)
    
    dydx = 0
    for i in range(9):
        dydx += a[i,order] * yArray[i]
    
    dydx /= Δx
    return dydx


# # Molecular Weight

# In[14]:


MWElements = {'H':1.008,                                                                              
              'He':4.0026,              'Li':6.94,   'Be':9.0122, 'B':10.81,   'C':12.011,  'N':14.007,  'O':15.99, 'F':18.998, 'Ne':20.180,              
              'Na':22.990,              'Mg':24.305, 'Al':26.982, 'Si':28.085, 'P':30.974,  'S':32.06, 'Cl':35.45, 'Ar':39.948,              
              'K' :39.098}

def MW(CFormula):
    #if len(CFormula) == 1:
     #   return (MWElements[CFormula])
    
    weight = 0
    for i in range(len(CFormula)):
        if (CFormula[i].isdigit() or CFormula[i].islower()):
            continue
        else:
            if i == len(CFormula)-1 and CFormula[i].isupper():
                weight += MWElements[CFormula[i]]
                continue
            
            if CFormula[i+1].islower():
                k = 1
            else:
                k = 0
            
            j = i + k + 1
            while ((j) < len(CFormula) and CFormula[j].isdigit()):
                j += 1
            
            
            if (i+k+1) == j:
                n = 1
            else:
                n = CFormula[i+k+1:j]
                
            weight += int(n) * MWElements[CFormula[i:i+k+1]]
            
    return weight

def MWU(chemFormula):
        return MW(chemFormula) * UUU('g','mol')

def makeNewDatabase(self):
        database = sql.connect(self.path)
        self.cursor = database.cursor()
        self.cursor.execute("create table VariableNames (                                VarName text Primary Key,                                VarTypes text not null);")
        self.cursor.execute("create table StringVariables (                                VarName text Primary Key,                                VarVal text not null);")
        self.cursor.execute("create table FloatVariables (                                   VarName text Primary Key,                                   VarVal real not null);")
        self.cursor.execute("create table IntegerVariables (                                   VarName text Primary Key,                                   VarVal integer not null);")
        self.cursor.execute("create table ArrayVariables (                                    VarName text Primary Key,                                     VarVal blob not null,                                    VarShape blob not null,                                    DType text not null);")
        database.commit()
        database.close()
        
    
    def __loadStrings__(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM StringVariables")
        StringsList = cursor.fetchall();
        
        for i in StringsList:
            setattr(self, i[0], i[1])
            
    def __loadIntegers__(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM IntegerVariables")
        StringsList = cursor.fetchall();
        
        for i in StringsList:
            setattr(self, i[0], i[1])
    
    def __loadFloats__(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM FloatVariables")
        StringsList = cursor.fetchall();
        
        for i in StringsList:
            setattr(self, i[0], i[1])
            
    def __loadArrays__(self):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM ArrayVariables")
        StringsList = cursor.fetchall();
        
        for i in StringsList:
            Var = np.frombuffer(i[1], dtype=np.dtype(i[3])).reshape(*np.frombuffer(i[2], dtype = np.dtype("int32")))
            setattr(self, i[0], Var)
    
    def add(self, varName, Val, OverrideExisting = False):
        database = sql.connect(self.path)
        varHolder = "(?,?)"
        if type(Val) == int:
            varType = "IntegerVariables"
            VarData = (varName, Val)
        elif type(Val) == float:
            varType = "FloatVariables"
            VarData = (varName, Val)
        elif type(Val) == str:
            varType = "StringVariables"
            VarData = (varName, Val)
        elif type(Val) == type(np.array([])):
            varType = "ArrayVariables"
            VarData = (varName, Val.tobytes(), np.array(Val.shape), str(Val.dtype)) #.astype(np.dtype("float64"))
            varHolder = "(?,?,?,?)"
        else:
            print("This Variable Type is Not Currently Supported.                         \nSee Help for a list of currently supported variables")
        try:
            cursor = database.cursor()
            VarNamesData = (varName,varType)
            cursor.execute(f"INSERT INTO VariableNames VALUES(?,?)", VarNamesData)
            database.commit()
            cursor = database.cursor()
            cursor.execute(f"INSERT INTO {varType} VALUES {varHolder}", VarData)
            database.commit()
            setattr(self, varName, Val)
            database.close()
            return
            
        except sql.IntegrityError:
            if OverrideExisting:
                try:
                    self.remove(varName, database)
                except:
                    database.close()
                    return
                cursor = database.cursor()
                data = (varName,varType)
                cursor.execute(f"INSERT INTO VariableNames VALUES(?,?)", VarNamesData)
                database.commit()
                cursor = database.cursor()
                data = (varName, Val)
                cursor.execute(f"INSERT INTO {varType} VALUES {varHolder}", VarData)
                database.commit()
                database.close()
                setattr(self, varName, Val)
                return
            
            else:
                cursor = database.cursor()
                cursor.execute(f"SELECT VarTypes FROM VariableNames WHERE VarName = ?", (varName,))
                varType = cursor.fetchone()[0]
                cursor = database.cursor()
                cursor.execute(f"SELECT VarVal FROM {varType} WHERE VarName = ?", (varName,))
                varVal = cursor.fetchone()[0]
                print(f"{varName} is already a defined {varType[0:-1]} with value {varVal}")
                print("To Override set override flag to true")
                database.close()
                return
                
                
    def remove(self, varName, database = None):
        opened = False
        if not database:
            opened = True
            database = sql.connect(self.path)
        try:
            cursor = database.cursor()
            cursor.execute(f"SELECT VarTypes FROM VariableNames WHERE VarName = ?", (varName,))
            varType = cursor.fetchone()[0]
            cursor = database.cursor()
            cursor.execute(f"DELETE FROM VariableNames WHERE VarName = ?", (varName,))
            database.commit()
            cursor = database.cursor()
            cursor.execute(f"DELETE FROM {varType} WHERE VarName = ?", (varName,))
            database.commit()
            setattr(self, varName, None)
            if opened:
                database.close()
        except:
            if opened:
                database.close()
            print(f"{varName} could not be found")
            
    def printAllVar(self):
        database = sql.connect(self.path)
        cursor = database.cursor()
        cursor.execute(f"Select * FROM VariableNames")
        Vars = cursor.fetchall()
        for i in Vars:
            print(f"({i[0]}, {i[1][0:-1]})")
        database.close()
        return
    
    def printAll(self):
        database = sql.connect(self.path)
        C = database.cursor()
        C.execute("Select * from VariableNames")
        print(C.fetchall())
        C.execute("Select * from StringVariables")
        print(C.fetchall())
        C.execute("Select * from FloatVariables")
        print(C.fetchall())
        C.execute("Select * from IntegerVariables")
        print(C.fetchall())
        C.execute("Select * from ArrayVariables")
        print(C.fetchall())
        database.close()
