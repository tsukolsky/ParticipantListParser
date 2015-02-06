specialCharacters = ["Intl State", 0xFF]
STATE_PROVINCE = 'State/Province'
COLUMN_SEPERATOR = ''
FEMALE = 'F'
MALE = 'M'
NEW_PAGE_DELIMITER = '\x0c'

# Field Types in PDF Output
FIRST_NAME = 'FirstName'
LAST_NAME = 'LastName'
GENDER = 'Gender'
AGE = 'Age'
STPR = 'StateProvince\n'
FORMAT = [FIRST_NAME, LAST_NAME, GENDER, AGE, STPR]

class Participant():
    def __init__(self, firstName = ""):
        self.firstName = firstName
        self.lastName = ""
        self.age = -1
        self.gender = 'N'
        self.origin = ''
        
    def setField(self, currentField, value):
        if currentField == FIRST_NAME:
            self.setFirstName(value)
        elif currentField == LAST_NAME:
            self.setLastName(value)
        elif currentField == AGE:
            self.setAge(int(value))
        elif currentField == STPR:
            self.setOrigin(value)
        elif currentField == GENDER:
            self.setGender(value)
        else:
            print "Uknown field to set!"
            
    def getAge(self):
        return self.age
        
    def setAge(self, age):
        self.age = age
    
    def getFirstName(self):
        return self.firstName    
    
    def setFirstName(self, name):
        self.firstName = name
    
    def getLastName(self):
        return self.lastName
    
    def setLastName(self, name):
        self.lastName = name
        
    def getOrigin(self):
        return self.origin
        
    def setOrigin(self, origin):
        self.origin = origin
        
    def getGender(self):
        return self.gender
        
    def setGender(self, gender):
        self.gender = gender
        
    def printParticipant(self):
        print "%s %s, %d, %s, %s"%(self.firstName, self.lastName, self.age, self.gender, self.origin)


F18_24 = "Female 18-24"
F25_29 = "Female 25-29"
F30_34 = "Female 30-34"
F35_39 = "Female 35-39"
F40_44 = "Female 40-44"
F45_49 = "Female 45-49"
F50_54 = "Female 50-54"
F55_59 = "Female 55-59"
F60_64 = "Female 60-64"
F65_69 = "Female 65-69"
F70_74 = "Female 70-74"
F75_79 = "Female 75-79"
F80_   = "Female 80+"

M18_24 = "Male 18-24"
M25_29 = "Male 25-29"
M30_34 = "Male 30-34"
M35_39 = "Male 35-39"
M40_44 = "Male 40-44"
M45_49 = "Male 45-49"
M50_54 = "Male 50-54"
M55_59 = "Male 55-59"
M60_64 = "Male 60-64"
M65_69 = "Male 65-69"
M70_74 = "Male 70-74"
M75_79 = "Male 75-79"
M80_   = "Male 80+"

R18_24 = range(18,25)
R25_29 = range(25,30)
R30_34 = range(30,35)
R35_39 = range(35,40)
R40_44 = range(40,45)
R45_49 = range(45,50)
R50_54 = range(50,55)
R55_59 = range(55,60)
R60_64 = range(60,65)
R65_69 = range(65,70)
R70_74 = range(70,75)
R75_79 = range(75,80)
R80_   = range(80,120)

MaleAgeGroupOrder = [M18_24, M25_29, M30_34, M35_39, M40_44, M45_49, M50_54, M55_59, M60_64, M65_69, M70_74, M75_79, M80_]
FemaleAgeGroupOrder = [F18_24, F25_29, F30_34, F35_39, F40_44, F45_49, F50_54, F55_59, F60_64, F65_69, F70_74, F75_79, F80_]
AgeGroupOrder = MaleAgeGroupOrder + FemaleAgeGroupOrder

FemaleAgeGroups = dict()
MaleAgeGroups = dict()
MasterAgeGroup = dict()
TotalEntrants = 0

def initializeDictionary():
    ## Initialize global age groups
    FemaleAgeGroups[F18_24] = R18_24
    FemaleAgeGroups[F25_29] = R25_29    
    FemaleAgeGroups[F30_34] = R30_34
    FemaleAgeGroups[F35_39] = R35_39
    FemaleAgeGroups[F40_44] = R40_44
    FemaleAgeGroups[F45_49] = R45_49
    FemaleAgeGroups[F50_54] = R50_54
    FemaleAgeGroups[F55_59] = R55_59
    FemaleAgeGroups[F60_64] = R60_64
    FemaleAgeGroups[F65_69] = R65_69
    FemaleAgeGroups[F70_74] = R70_74
    FemaleAgeGroups[F75_79] = R75_79
    FemaleAgeGroups[F80_] = R80_
       
    MaleAgeGroups[M18_24] = R18_24
    MaleAgeGroups[M25_29] = R25_29    
    MaleAgeGroups[M30_34] = R30_34
    MaleAgeGroups[M35_39] = R35_39
    MaleAgeGroups[M40_44] = R40_44
    MaleAgeGroups[M45_49] = R45_49
    MaleAgeGroups[M50_54] = R50_54
    MaleAgeGroups[M55_59] = R55_59
    MaleAgeGroups[M60_64] = R60_64
    MaleAgeGroups[M65_69] = R65_69
    MaleAgeGroups[M70_74] = R70_74
    MaleAgeGroups[M75_79] = R75_79
    MaleAgeGroups[M80_] = R80_
       
    ## Dictionary should be all based on age group
    MasterAgeGroup[F18_24] = list()
    MasterAgeGroup[F25_29] = list()
    MasterAgeGroup[F30_34] = list()
    MasterAgeGroup[F35_39] = list()
    MasterAgeGroup[F40_44] = list()
    MasterAgeGroup[F45_49] = list()
    MasterAgeGroup[F50_54] = list()
    MasterAgeGroup[F55_59] = list()
    MasterAgeGroup[F60_64] = list()
    MasterAgeGroup[F65_69] = list()
    MasterAgeGroup[F70_74] = list()
    MasterAgeGroup[F75_79] = list()
    MasterAgeGroup[F80_] = list()
    
    MasterAgeGroup[M18_24] = list()
    MasterAgeGroup[M25_29] = list()
    MasterAgeGroup[M30_34] = list()
    MasterAgeGroup[M35_39] = list()
    MasterAgeGroup[M40_44] = list()
    MasterAgeGroup[M45_49] = list()
    MasterAgeGroup[M50_54] = list()
    MasterAgeGroup[M55_59] = list()
    MasterAgeGroup[M60_64] = list()
    MasterAgeGroup[M65_69] = list()
    MasterAgeGroup[M70_74] = list()
    MasterAgeGroup[M75_79] = list()
    MasterAgeGroup[M80_] = list()
