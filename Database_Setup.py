import sqlite3 as sql
import sys
import os

class myVars():
    '''
    A Class for using persistant variables through the use of an SQLite Database
    Change self.path below to be an absolute path found within your computer.
    
    '''
    def __init__(self):
        path = os.path.realpath(__file__)
        path = path.split('/')
        path[-1] = "units.db"
        self.path = ""
        for i in path:
            self.path += '/'+i

        try:
            file = open(self.path)
            file.close()
        except IOError:
            print("No Database Found. Generating New Database")
            self.__makeNewDatabase__()


    def __makeNewDatabase__(self):
            database = sql.connect(self.path)
            self.cursor = database.cursor()
            self.cursor.execute("create table UnitVariables (UnitName text Primary Key,\
                                                            UnitType text not null,\
                                                            UnitValue real not null);")
            database.commit()
            database.close()
    
    
    def loadUnitVariables(self):
        database = sql.connect(self.path)
        self.cursor = database.cursor()
        self.cursor.execute("SELECT * FROM UnitVariables")
        unitList = self.cursor.fetchall();
        database.close()
        return unitList
    
    
    def add(self, UnitName, UnitType, UnitValue, OverrideExisting = False):
        database = sql.connect(self.path)
        varHolder = "(?,?,?)"
        VarData = (UnitName, UnitType, UnitValue)
    
        try:
            cursor = database.cursor()
            cursor.execute(f"INSERT INTO UnitVariables VALUES {varHolder}", VarData)
            database.commit()
            database.close()
            return
    
        except sql.IntegrityError:
            if OverrideExisting:
                try:
                    self.remove(varName)
                except:
                    database.close()
                    return
                cursor = database.cursor()
                cursor.execute(f"INSERT INTO UnitVariables VALUES {varHolder}", VarData)
                database.commit()
                database.close()
                return
    
            else:
                raise Error("Error: Does Unit type already exist? Try OverrideExisting Flag")
                return
    
    
    def remove(self, varName, database = None):
        opened = False
        if not database:
            opened = True
            database = sql.connect(self.path)
        try:
            cursor = database.cursor()
            cursor.execute(f"DELETE FROM UnitVariables WHERE VarName = ?", (varName,))
            database.commit()
            if opened:
                database.close()
        except:
            if opened:
                database.close()
            print(f"{varName} could not be found")
