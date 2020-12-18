MWElements = {'H':1.008,                                                                              
              'He':4.0026,              'Li':6.94,   'Be':9.0122, 'B':10.81,   'C':12.011,  'N':14.007,  'O':15.99, 'F':18.998, 'Ne':20.180,              
              'Na':22.990,              'Mg':24.305, 'Al':26.982, 'Si':28.085, 'P':30.974,  'S':32.06, 'Cl':35.45, 'Ar':39.948,              
             'K' :39.098}

def MW(CFormula):
    
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
