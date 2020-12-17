
# coding: utf-8

# In[5]:


# %load "https://che.byu.edu/imports.py"
import numpy             as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
from scipy.optimize      import fsolve, curve_fit
from scipy.integrate     import odeint, quad
import sqlite3 as sql


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

# In[6]:


UnitPrefix = {'Y':10**24, 'Z':10**21, 'E':10**18, 'P':10**15,                'T':10**12, 'G':10**9, 'M':10**6, 'k':10**3, 'h':100,                'da':10, '':1,'d':.1, 'c':.01, 'm':10**-3, 'μ':10**-6,                 'n':10**-9, 'p':10**-12, 'f':10**-15, 'a':10**-18,                 'z':10**-21, 'y':10**-24}


SI = {'Mass':'k_g', 'time':'s', 'Length':'m', 'Pressure':'Pa', 'Force':'N', 'Energy':'J', 'Power':'W', "Vol":'m^3', 'Temp':'K', 'Mole':'mol'}
SITop = {'k_g':'k_g', 's':'s', 'm':'m', 'Pa':'k_g',      'N':'k_g*m', 'J':'k_g*m^2', 'W':'k_g*m^2', "m^3":'m^3',    'K':'K',    'mol':'mol'}
SIBottom = {'k_g':'', 's':'',  'm':'',  'Pa':'m*s^2', 'N':'s^2',    'J':'s^2',       'W':'s^3',       "m^3":'',     'K':'',     'mol':''}

UnitType = {'g':'Mass', 'lb':'Mass', 'oz':'Mass', 'ton':'Mass', 'amu':'Mass',            's':'time', 'min':'time', 'h':'time', 'd':'time', 'y':'time',            'K':'Temp', 'R':'Temp',            'm':'Length', 'in':'Length', 'mil':'Length','ft':'Length', 'yard':'Length', 'mile':'Length',            'Pa':'Pressure', 'torr':'Pressure', 'mmHg':'Pressure', 'bar':'Pressure', 'atm':'Pressure', 'psi':'Pressure',            'N':'Force', 'lbf':'Force',            'J':'Energy', 'BTU':'Energy', 'calorie':'Energy', 'Calorie':'Energy', 'Wh':'Energy', 'eV':'Energy',            'W':'Power', 'Horsepower':'Power',            'L':'Vol', 'gal':'Vol', 'quart':'Vol', 'cup':'Vol', 'pint':'Vol', 'Tbsp':'Vol', 'tsp':'Vol', 'm^3':'Vol',            'mol':'Mole', 'lbmol':'Mole'}


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

# In[7]:


class UnitException(Exception):
    def __init__(self, operation, unitOne, unitTwo):
        return


# ## Unit Analysis

# In[8]:


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


# ## Unit and Other Variable Definitions

# In[10]:


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


# ## Other Unit Functions

# In[11]:


ρ = 1000 * kg / m**3
U = 15 * m / s
D = 10 * cm
μ = .001 * Pa * s

Re = ρ * U * D / μ


# In[12]:


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


MWElements = {'H':1.008,                                                                              'He':4.0026,              'Li':6.94,   'Be':9.0122, 'B':10.81,   'C':12.011,  'N':14.007,  'O':15.99, 'F':18.998, 'Ne':20.180,              'Na':22.990, 'Mg':24.305, 'Al':26.982, 'Si':28.085, 'P':30.974,  'S':32.06, 'Cl':35.45, 'Ar':39.948,              'K' :39.098}

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


# In[18]:


# ## Thermodynamics

# In[236]:


GasΔHf = {'CH4':-74520, 'C2H6':-83820, 'C3H8':-104680, 'C4H10':-125790, 'C5H12':-146760,
        'C6H14':-166920, 'C7H16':-187780, 'C8H18':-208750, 'C2H4':52510, 'C3H6':19710,
        'C4H8':-540,'C5H10':-21280,'C6H12':-41950,'C7H14':-62760,'C2H4O':-166190,'C2H2':227480,
        'C6H6':82930,'C4H6':109240,'C6H12':-123140,'C2H6O':-235100,'C8H10':29920,'C2H4O':-52630,
        'CH2O':-108570,'CH4O':-200660,'C7H14':-154770,'C8H8':147360,'C7H8':50170,'NH3':-46110,
        'CO2':-393509,'CO':-110525,'HCl':-92307,'HCN':135100,'H2S':-20630,'NO':90250,'NO2':33180,
        'N2O':82050,'N2O4':9160,'SO2':-296830,'SO3':-395720, 'H2O':-241818}

GasΔGf = {'CH4':-50460,'C2H6':-31855,'C3H8':-24290,'C4H10':-16570,'C5H12':-8650,'C6H14':150,'C7H16':8260,
         'C8H18':16260,'C2H4':68460,'C3H6':62205,'C4H8':70340,'C5H10':78410,'C6H12':86830,
         'C2H4O':-128860,'C2H2':209970,'C6H6':129665,'C4H6':149795,'C6H12':31920,'C2H6O':-168490,'C8H10':130890,
         'C2H4O':-13010,'CH2O':-102530,'CH4O':-161960,'C7H14':27480,'C8H8':213900,'C7H8':122050,'NH3':-16400,
         'CO2':-394359,'CO':-137169,'HCl':-95299,'HCN':124700,'H2S':-33560,'NO':86550,'NO2':51310,'N2O':104200,
         'N2O4':97540,'SO2':-300194,'SO3':-371060, 'H2O':-228572}

LiqΔHf = {'C2H4O2':-484500,'C6H6':49080,'C6H12':-156230,'C2H6O2':-454800,'C2H6O':-277690,'CH4O':-238660,
         'C7H14':-190160,'C7H8':12180,'HNO3':-174100,'SO3':-441040, 'H2SO4':-813989, 'H2O':-285830}

LiqΔGf = {'C2H4O2':-389900,'C6H6':124520,'C6H12':26850,'C2H6O2':-323080,'C2H6O':-174780,
         'CH4O':-166270,'C7H14':20560,'C7H8':113630,'HNO3':-80710, 'H2SO4':-690003, 'H2O':-237129}

SolidΔHf = {'CaC2':-59800,'CaCO3':-1206920,'CaCl2':-795800,'CaCl2·6H2O':-2607900,'Ca(OH)2':-986090,
           'CaO':-635090,'FeO':-272000,'Fe2O3':-824200,'Fe3O4':-1118400,'FeS2':-178200,'LiCl':-408610,
           'LiCl·H2O':-712580,'LiCl·2H2O':-1012650,'LiCl·3H2O':-1311300,'Na2CO3':-1130680,'Na2CO3·10H2O':-4081320,
           'NaCl':-411153, 'NaOH':-425609}

SolidΔGf = {'CaC2':-64900,'CaCO3':-1128790,'CaCl2':-748100,'Ca(OH)2':-898490,'CaO':-604030,'Fe2O3':-742200,
           'Fe3O4':-1015400,'FeS2':-166900,'Na2CO3':-1044440,'NaCl':-384138,'NaOH':-379494}

AqueousΔGf = {'NH3':-26500,'CaCl2':-8101900,'Ca(OH)2':-868070,'HNO3':-111250,'NaCl':-393133,'NaOH':-419150, 'H2SO4':-744530}

HState = {'s':SolidΔHf, 'l':LiqΔHf, 'g':GasΔHf}
GState = {'s':SolidΔGf, 'l':LiqΔGf, 'g':GasΔGf, 'aq':AqueousΔGf}

def ΔHf(species, state):
    try:
        return HState[state][species]
    except:
        return 0

def ΔGf(species, state):
    try:
        return GState[state][species]
    except:
        return 0

def ΔHrxnf(species, state, stoichiometry):
    ΔHrxn = 0
    for i in range(len(species)):
        #print(species[i], ΔHf(species[i],state[i]), state[i], stoichiometry[i])
        ΔHrxn += ΔHf(species[i], state[i]) * stoichiometry[i]
    return ΔHrxn

def ΔHrxn(species, state, stoichiometry):
    ΔHrxn = 0
    for i in range(len(species)):
        #print(species[i], ΔHf(species[i],state[i]), state[i], stoichiometry[i])
        ΔHrxn += ΔHf(species[i], state[i]) * stoichiometry[i]
        ΔHrxn += ΔHmix(298.15, Trxn, species, state, stoichiometry)
    return ΔHrxn

def Qrxn(Tin, Tout, species, state, molsIn, molsOut,):
    Qrxn = 0
    for i in range(len(species)):
        Qrxn += molsOut[i] * (ΔHf(species[i], state[i]) + ΔH(298.15, Tout, species[i], state[i]))
        Qrxn -= molsIn[i] * (ΔHf(species[i], state[i]) + ΔH(298.15, Tin, species[i], state[i]))
    return Qrxn


# In[237]:


def ZGas(R = 8.314, P = -1, V = -1, n = -1, T = -1, Z = 1):
    if V == -1 and n == -1:
        return R * T * Z / P 
    elif P == -1:
        return n * R * T * Z / V
    elif V == -1:
        return n * R * T * Z / P
    elif n == -1:
        return P * V / R / T / Z
    elif T == -1:
        return P * V / R / n / Z

def vdWα(Tr = 0, ω = 0):
    return 1

def RKα(Tr, ω = 0):
    return Tr**-.5

def SRKα(Tr, ω):
    return (1 + (0.480 + 1.574 * ω - 0.176 * ω**2) * (1 - Tr**.5))**2

def PRα(Tr, ω):
    return (1 + (0.37464 + 1.54226 * ω - 0.26992 * ω**2) * (1 - Tr**.5))**2
    

vdWTable = {'α':vdWα,  'σ':0,            'ϵ':0,           'Ω':1/8,    'Ψ':27/64,  'Zc':3/8}
RKTable  = {'α':RKα,   'σ':1,            'ϵ':0,           'Ω':.08664, 'Ψ':.42748, 'Zc':1/3}
SRKTable = {'α':SRKα,  'σ':1,            'ϵ':0,           'Ω':.08664, 'Ψ':.42748, 'Zc':1/3}
PRTable  = {'α':PRα,   'σ':(1 + 2**.5),  'ϵ':(1 - 2**.5), 'Ω':0.0778, 'Ψ':.45724, 'Zc':.30740}

EOSTable = {'vdW':vdWTable, 'RK':RKTable, 'SRK':SRKTable, 'PR':PRTable}

def β(EOS, Tr, Pr):
    return EOSTable[EOS]['Ω'] * Pr / Tr

def q(EOS, Tr, ω):
    return EOSTable[EOS]['Ψ'] * EOSTable[EOS]['α'](Tr, ω) / (EOSTable[EOS]['Ω'] * Tr)

def solve_Z(Z, EOS, Tr, Pr, ω):
    β0 = β(EOS, Tr, Pr)
    q0 = q(EOS, Tr, ω)
    return 1 + β0 - q0 * β0 * (Z - β0) / (Z + EOSTable[EOS]['ϵ'] * β0) / (Z + EOSTable[EOS]['σ'] * β0) - Z

def Z(EOS, Tr, Pr, ω, Z = 1):
    "Z(EOS, Tr, Pr, ω, Z = 1):\n    EOS is a string of either 'vdW', 'RK', 'SRK', or 'PR'\n    Tr/Pr are the reduced Temperature/Pressure\n    ω is the acentric factor\n    Z is a guess value(defaults to 1)"
    return fsolve(solve_Z, Z, args = (EOS, Tr, Pr, ω))[0]

def work(Vo, Vf, n, T, R = 8.314, Z = 1):
    def Integrand(V):
        return ZGas(R, V = V, n = n, T = T, Z = Z)
    return -quad(Integrand, Vo, Vf)[0]

def HrSr(T1, Tr, Pr, ω, EOS = 'RK'):
    Zl = Z(EOS, Tr, Pr, 0)
    def lnα(Tr):
        x = np.log(EOSTable[EOS]['α'](np.exp(Tr), ω))
        return x
    I = (0 if(EOSTable[EOS]['σ'] - EOSTable[EOS]['ϵ']) == 0 else (EOSTable[EOS]['σ'] - EOSTable[EOS]['ϵ'])**-1)     * np.log((Zl + EOSTable[EOS]['σ'] * β(EOS, Tr, Pr))/(Zl + EOSTable[EOS]['ϵ'] * β(EOS, Tr, Pr)))
    Hr = (Zl - 1 + (finiteDifferenceMethod(6, lnα, Tr) - 1) * I * q(EOS, Tr, Pr)) * 8.314 * T1
    Sr = (np.log(Zl - β(EOS, Tr, Pr)) + finiteDifferenceMethod(6, lnα, Tr) * I * q(EOS, Tr, Pr)) * 8.314
    return Hr, Sr


# In[238]:


gasAntoine = {'CH4':(1.702, 0.009081, -2.164e-06, 0),'C2H6':(1.131, 0.019225, -5.561e-06, 0),            'C3H8':(1.213, 0.028785, -8.824e-06, 0),'n-C4H10':(1.935, 0.036915, -1.1402e-05, 0),            'i-C4H10':(1.677, 0.037853, -1.1945e-05, 0),'C5H12':(2.464, 0.045351, -1.4111e-05, 0),            'C6H14':(3.025, 0.053722, -1.6791e-05, 0),'C7H16':(3.570, 0.062127, -1.9486e-05, 0),            'C8H18':(4.108, 0.070567, -2.2208e-05, 0),'C2H4':(1.424, 0.014394, -4.392e-06, 0),            'C3H6':(1.637, 0.022706, -6.915e-06, 0),'C4H8':(1.967, 0.03163, -9.873e-06, 0),            'C5H10':(2.691, 0.039753, -1.2447e-05, 0),'C6H12':(3.220, 0.048189, -1.5157e-05, 0),            'C7H14':(3.768, 0.056588, -1.7847e-05, 0),'C8H16':(4.324, 0.06496, -2.0521e-05, 0),            'C2H4O':(1.693, 0.017978,  -6.158e-06, 0),'C6H6':(-0.206, 0.039064, -1.3301e-05, 0),            'C4H6':(2.734, 0.026786, -8.882e-06, 0),'C6H12':(-3.876, 0.063249, -2.0928e-05, 0),            'C2H6O':(3.518, 0.020001,  -6.002e-06, 0),'C8H10':(1.124, 0.05538, -1.8476e-05, 0),            'C2H4O':(-0.385, 0.023463, -9.296e-06, 0),'CH2O':(2.264, 0.007022, -1.877e-06, 0),            'CH4O':(2.211, 0.012216, -3.45e-06, 0),'C8H8':(2.050, 0.050192, -1.6662e-05, 0),            'NH3':(3.578, 0.00302, 0, -18600.0),'Br2':(4.493, 5.6e-05, 0, -15400.0),            'CO':(3.376, 0.000557, 0, -3100.0),'CO2':(5.457, 0.001045, 0, -115700.0),            'CS2':(6.311, 0.000805, 0, -90600.0),'Cl2':(4.442, 8.9e-05, 0, -34400.0),            'H2':(3.249, 0.000422, 0, 8300.0),'H2S':(3.931, 0.00149, 0, -23200.0),            'HCl':(3.156, 0.000623, 0, 15100.0),'HCN':(4.736, 0.001359, 0, -72500.0),            'N2':(3.280, 0.000593, 0, 4000.0),'N2O':(5.328, 0.001214, 0, -92800.0),            'NO':(3.387, 0.000629, 0, 1400.0),'NO2':(4.982, 0.001195, 0, -79200.0),            'N2O4':(11.660, 0.002257, 0, -278700.0),'O2':(3.639, 0.000506, 0,  -22700.0),            'SO2':(5.699, 0.000801, 0,  -101499.99999999999),'SO3':(8.060, 0.001056, 0,  -202800.0),            'H2O':(3.470, 0.00145, 0, 12100.0),'air':(3.355, 0.575, 0, -.016)}

liqAntoine =   {'Ammonia':(22.626,-0.10075, 0.00019271, 0),'Aniline':(15.819,0.02903, -1.58e-05, 0),                'Benzene':(-0.747,0.06796, -3.778e-05, 0),'1,3-Butadiene':(22.711,-0.08796, 0.00020579, 0),                'Carbontetrachloride':(21.155,-0.04828, 0.00010114, 0),'Chlorobenzene':(11.278,0.03286, -3.19e-05, 0),                'Chloroform':(19.215,-0.04289, 8.301e-05, 0),'Cyclohexane':(-9.048,0.14138, -0.00016162, 0),                'Ethanol':(33.866,-0.1726, 0.00034917, 0),'Ethyleneoxide':(21.039,-0.08641, 0.00017228, 0),                'Methanol':(13.431,-0.05128, 0.00013113, 0),'n-Propanol':(41.653,-0.21032, 0.0004272, 0),                'Sulfurtrioxide':(-2.930,0.13708, -8.473e-05, 0),'Toluene':(15.133,0.00679, 1.635e-05, 0),                'Water':(8.712, 1.25*10**-3, -0.18*10**-6, 0)}

solidAntoine = {'CaO':(6.104,0.000443, 0, -1.047e-06),'CaCO3':(12.572,0.002637, 0, -3.12e-06),              'Ca(OH)2':(9.597,0.005435, 0, 0.0),'CaC2':(8.254,0.001429, 0, -1.042e-06),              'CaCl2':(8.646,0.00153, 0, -3.02e-07),'C':(1.771,0.000771, 0, -8.67e-07),              'Cu':(2.677,0.000815, 0, 3.5e-08),'CuO':(5.780,0.000973, 0, -8.74e-07),              'Fe(α)':(-0.111,0.006111, 0, 1.15e-06),'Fe2O3':(11.812,0.009697, 0, -1.976e-06),              'Fe3O4':(9.594,0.027112, 0, 4.09e-07),'FeS':(2.612,0.013286, 0, 0.0),              'I2':(6.481,0.001502, 0, 0.0),'LiCl':(5.257,0.002476, 0, -1.93e-07),              'NH4Cl':(5.939,0.016105, 0, 0.0),'Na':(1.988,0.004688, 0, 0.0),              'NaCl':(5.526,0.001963, 0, 0.0),'NaOH':(0.121,0.016316, 0, 1.948e-06),              'NaHCO3':(5.128,0.018148, 0, 0.0),'S':(4.114,-0.001728, 0, -7.83e-07)}

TSolidMax = {'CaO':2000, 'CaCO3':1200, 'Ca(OH)2':700,             'CaC2':720, 'CaCl2':1055, 'C':2000, 'Cu':1357,             'CuO':1400, 'Fe(α)':1043, 'Fe2O3':960, 'Fe3O4':850,             'FeS':411, 'I2':386.8, 'LiCl':800, 'NH4Cl':458, 'Na':371,             'NaCl':1073, 'NaOH':566, 'NaHCO3':400, 'S':368.3}

AntoineTuple = {'s':solidAntoine, 'l':liqAntoine, 'g':gasAntoine}

def AntoineCp(T, A, B, C, D):
    return (A + B * T + C * T**2 + D * T**-2) * 8.314

def ΔH(T1, T2, species = '', state = 'g'):
    "H(T1, T2, species =, param =)"
    return quad(AntoineCp, T1, T2, args = AntoineTuple[state][species])[0]

def ΔS(T1, T2, P1, P2, species = '', state = 'g'):
    def solve(T, A, B, C, D):
        return AntoineCp(T, A, B, C, D) / T
    
    return quad(solve, T1, T2, args = AntoineTuple[state][species])[0] - 8.314 * np.log(P2/P1)

def ΔU(T1, T2, species = '', param = ()):
    if species != '':
        def Integrand(T):
            return AntoineCP(*AntoineTuple[phase][species]) - 8.314 
    else:
        def Integrand(T):
            return Cp[phase](*param) - 8.314
    return quad(Integrand, T1, T2)[0]


def CpMix(T, species = (), state = (), mols = ()):
    if len(species) != len(mols):
        raise Exception('species and mols length mismatch')
    A = 0
    B = 0
    C = 0
    D = 0
    for i in range(len(species)):
        A += AntoineTuple[state[i]][species[i]][0] * mols[i]
        B += AntoineTuple[state[i]][species[i]][1] * mols[i]
        C += AntoineTuple[state[i]][species[i]][2] * mols[i]
        D += AntoineTuple[state[i]][species[i]][3] * mols[i]
    tupleMix = (A,B,C,D)
    return AntoineCp(T, *tupleMix)

def ΔHmix(T1, T2, species, state, mols):
    X = (species, state, mols)
    return quad(CpMix, T1, T2,X)[0]


# ## Persistant Variables

# In[ ]:


class myVars():
    '''
    A Class for using persistant variables through the use of an SQLite Database
    Change self.path below to be an absolute path found within your computer.
    
    Currently supported variable are:
    Integers
    Floats
    Strings
    Numpy Arrays (Doesn't work if Array.dtype returns "O")
    '''
    def __init__(self):
        #--------------------
        # Set Your Path Here
        #--------------------
        self.path = "C:\\Users\\tanne\Homework\PersistantVariables.db"
        try:
            file = open(self.path)
            file.close()
        except IOError:
            print("No Database Found. Generating New Database")
            self.makeNewDatabase()
        
        self.database = sql.connect(self.path)
        self.__loadStrings__()
        self.__loadIntegers__()
        self.__loadFloats__()
        self.__loadArrays__()
        self.database.close()
        
        
        
            
    
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
        

