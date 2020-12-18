import numpy             as np
import matplotlib.pyplot as plt

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
SIBottom = {'k_g':'', 's':'',  'm':'',  'Pa':'m*s^2',    'N':'s^2',   'J':'s^2',     'W':'s^3',     "m^3":'',       'K':'',     'mol':''}

UnitType = {'m^3':'Vol'}


#Divide to Convert to Noted Unit, Multiply to Convert Away From Noted Unit
MassToGrams    = {}
TimeToSec      = {}
TempToKel      = {}
LengToMeter   = {}
PressureToPa   = {}
ForceToNewton  = {}
EnergyToJoule = {}
PowerToWatt   = {}
VolumeToLitre  = {'m^3':10**-3}
MoleToMol      = {}


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

