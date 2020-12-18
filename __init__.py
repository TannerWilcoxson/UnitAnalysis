#Unit and Other Variable Definitions

from . import Database_Setup as _Database_Setup
from . import ConversionTools as _ConversionTools
from . import UnitClass as _UnitClass
import os as _os
import sys as _sys

path = _os.path.realpath(__file__)
path = path.split('/')
path[-1] = "units.db"
_data_path = ""
for _i in path:
    _data_path += '/'+ _i

_needs_init = False
if not _os.path.isfile(_data_path):
    _needs_init = True
    
_db = _Database_Setup.myVars()

if _needs_init:
    _db.add("g", "Mass", 1)
    _db.add("mg", "Mass", 1000)
    _db.add("kg", "Mass", 1000**-1)
    _db.add("lb", "Mass", 453.592**-1)
    _db.add("oz", "Mass", 453.592**-1*16)
    _db.add("ton", "Mass", 453.592**-1/2000)
    _db.add("amu", "Mass", 6.022e23)

    _db.add("s", "time", 1)
    _db.add("min", "time", 60**-1)
    _db.add("h", "time", 3600**-1)
    _db.add("d", "time", 3600**-1/24)
    _db.add("y", "time", 3600**-1/24/3365)

    _db.add('K', 'Temp', 1)
    _db.add('R', 'Temp', 1.8)

    _db.add('m', 'Length', 1)
    _db.add('mm', 'Length', 1000)
    _db.add('cm', 'Length', 100)
    _db.add('km', 'Length', 1000**-1)
    _db.add('in', 'Length', .0254**-1)
    _db.add('mil', 'Length', 0.0254**-1*1000)
    _db.add('ft', 'Length', 0.0254**-1/12)
    _db.add('yd', 'Length', 0.0254**-1/12/3)
    _db.add('mile', 'Length', 0.0254**-1/12/5280)

    _db.add('Pa', "Pressure", 1)
    _db.add('kPa', "Pressure", 1000**-1)
    _db.add('MPa', "Pressure", 1e-6)
    _db.add('GPa', "Pressure", 1e-9)
    _db.add('torr', "Pressure", 0.00750062)
    _db.add('mmHg', "Pressure", 0.00750062)
    _db.add('bar', "Pressure", 1e-5)
    _db.add('mbar', "Pressure", 1e-2)
    _db.add('atm', "Pressure", 101325**-1)
    _db.add('psi', "Pressure", 0.000145038)

    _db.add('N', "Force", 1)
    _db.add('lbf', "Force", 0.224809)

    _db.add('J', "Energy", 1)
    _db.add('kJ', "Energy", 1e-3)
    _db.add('BTU', "Energy", 0.000947817)
    _db.add('cal', "Energy", 0.239006)
    _db.add('Cal', "Energy", 0.239006/1000)
    _db.add('Wh', "Energy", 0.000277778)
    _db.add('kWh', "Energy", 0.000277778/1000)
    _db.add('eV', "Energy", 1.60218e-19**-1)

    _db.add('W', "Power", 1)
    _db.add('kW', "Power", 1e-3)
    _db.add('MW', "Power", 1e-6)
    _db.add('Horsepower', "Power", 0.00134102)

    _db.add('L', "Vol", 1)
    _db.add('mL', "Vol", 1000)
    _db.add('gal', "Vol", 0.264172)
    _db.add('quart', "Vol", 1.05669)
    _db.add('cup', "Vol", 4.22675)
    _db.add('pint', "Vol", 4.22675/2)
    _db.add('Tbsp', "Vol", 67.628)
    _db.add('tsp', "Vol", 202.884)

    _db.add('mol', "Mole", 1)
    _db.add('lbmol', "Mole", 453.592**-1)

_ScalingByType = {"Mass":_ConversionTools.MassToGrams,
               "time":_ConversionTools.TimeToSec,
               "Temp":_ConversionTools.TempToKel,
               "Length":_ConversionTools.LengToMeter,
               "Pressure":_ConversionTools.PressureToPa,
               "Force":_ConversionTools.ForceToNewton,
               "Energy":_ConversionTools.EnergyToJoule,
               "Power":_ConversionTools.PowerToWatt,
               "Vol":_ConversionTools.VolumeToLitre,
               "Mole":_ConversionTools.MoleToMol}

_AllVars = _db.loadUnitVariables()
_currentmodule  = _sys.modules[__name__]  
_unitNames = []

for _var in _AllVars:
    _ConversionTools.UnitType[_var[0]] = _var[1]
    _ScalingByType[_var[1]][_var[0]] = _var[2]
    _unitNames.append(_var[0])

for _var in _AllVars:
    setattr(_currentmodule, _var[0], _UnitClass.UUU(_var[0]))

def AddNewUnit(unitName, unitType, conversionFactor, replace = False):
    '''
    unitName = name of unit to add to package
    unitType = type of unit (see list of acceptable type below)
    conversionFactor= Conversion Factor to get to the new unit from the
                      specified Unit for a given unitType (seen below)
    replace= Set True to redefine a pre- or previously defined unit

        unitType:SpecifiedUnitType
        'Mass': Grams 
        'time': Seconds
        'Temp': Kelvin
        'Length': Meters
        'Pressure': Pascals
        'Force': Newton
        'Energy': Joule
        'Power': Watt
        'Vol': Liter
        'Mole': Mole

    Example:
        If you wanted to define pounds (assuming it wasn't predefined). Use command-

        addNewUnit('lbs', 'Mass', 1/453.592)
        *It may be helpful to read the third argument as 1 lbs / 453.592 grams
    '''

    _db.add(unitName, unitType, conversionFactor, replace)
    _ConversionTools.UnitType[unitName] = unitType
    _ScalingByType[unitType][unitName] = conversionFactor
    _unitNames.append(unitName)
    setattr(_currentmodule, unitName, _UnitClass.UUU(unitName))

def GetAllUnits():
    return _unitNames

__all__ = _unitNames+['AddNewUnit', 'GetAllUnits']
