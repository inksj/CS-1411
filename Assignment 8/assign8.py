import sys
from math import floor

def loadPGM(filename):
    file = open(filename, "r")
    contents = file.read()
    lines = contents.split("\n")
    L = []
    for line in lines:
        pline = line.strip()
        if len(pline) > 0:
            first = pline[0]
            try:
                int(first)
                L.append(pline)
            except:
                continue
    G = []
    for line in L:
        S = line.split()
        for string in S:
            G.append(int(string))
    
    L = G
    A = G[0]
    B = G[1]
    C = G[2]
    D = []
    for i in range(B):
        D.append(G[3 + i*A: 3+(i+1)*A])
    return(A,B,C,D)
 
   
 
 
def writePGM(fileName, PGM):
    A,B,C,D = PGM
    outputfile=open(fileName,'w')
    outputfile.write("P2\n")
    outputfile.write(str(A)+ ' ' + str(B) + "\n"  )
    outputfile.write(str(C)+"\n")
    for elmts in D:
        for elmt in elmts:
            outputfile.write(str(elmt) + "\n")


def getPixel(P, PGM):
    X=P[0]
    Y=P[1]
    A=PGM[0]
    B=PGM[1]
    C=PGM[2]
    D=PGM[3]
    if (X < A) and (Y < B):
        return D[B-1-Y][X]
    else:
        return int(0)

 
 
def setPixel(P,V,PGM):
    X= P[0]
    Y=P[1]
    A=PGM[0]
    B=PGM[1]
    C=PGM[2]
    D=PGM[3]
    if (X < A) and (Y < B):
        D[B-1-Y][X]= min(max(V,0),C)
    else:
        None
        


    
def drawLine(C1,C2,V,PGM):
    X1=C1[0]
    Y1=C1[1]
    X2=C2[0]
    Y2=C2[1]

    xDiff= X2-X1
    yDiff=Y2-Y1
    between=[]
    if (xDiff==0):
        if yDiff >0:
            between=list(range(Y1+1,Y2))
        else:
            between=list(range(Y2+1,Y1))
        between=[(X1,Y) for Y in between]
    elif(yDiff==0):
        if xDiff>0:
             between=list(range(X1+1,X2))
        else:
            between=list(range(X2+1,X1))
        between=[(X,Y1) for X in between]
    else:
        slope=yDiff/xDiff
        b=Y1-slope*X1
        if abs(xDiff)> abs(yDiff):
            if xDiff>0:
                between=list(range(X1+1,X2))
            else:
                between=list(range(X2+1,X1))

            between=[(X,floor(X*slope + b)) for X in between]
        else:
            if(yDiff>0):
                between=list(range(Y1+1,Y2))
            else:
                between=list(range(Y2+1,Y1))
            between=[(floor((Y-b)/slope),Y) for Y in between]
        setPixel(C1,V,PGM)
        setPixel(C2,V,PGM)
        for C in between:
            setPixel(C,V,PGM)

            
def smooth(W, PGM):
    A,B,C,D = PGM
    A = PGM[0]
    B = PGM[1]
    C=PGM[2]
    D=PGM[3]
   

    copyTuple = (A, B, C, D)
    for row in range(len(copyTuple[3])):
        for col in range(len(copyTuple[3][row])):
            if row == 0 and col ==0:
                P = copyTuple[3][0][0]
                A = 0
                A += getPixel((row,col+1), copyTuple)
                A += getPixel((row+1,col+1), copyTuple)
                A += getPixel((row+1, col), copyTuple)
                A = A//3
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue, (A,B,C,D))
            elif row == 0 and col == A-1:
                P = copyTuple[3][0][A-1]
                A = 0
                A += getPixel((row,col-1), copyTuple)
                A += getPixel((row+1,col-1), copyTuple)
                A += getPixel((row+1,col), copyTuple)
                A = A//3
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif row == B-1 and col ==0:
                P = copyTuple[3][B-1][0]
                A = 0
                A += getPixel((row-1, col), copyTuple)
                A += getPixel((row-1, col+1), copyTuple)
                A += getPixel((row, col+1), copyTuple)
                A = A//3
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif row == B-1 and col == A-1:
                P = copyTuple[3][B-1][A-1]
                A = 0
                A += getPixel((row,col-1),copyTuple)
                A += getPixel((row-1,col-1),copyTuple)
                A += getPixel((row-1,col),copyTuple)
                A = A//3
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif row != 0 and col == 0 and row != B-1:
                P = copyTuple[3][row][0]
                A = 0
                A += getPixel((row-1, col), copyTuple)
                A += getPixel((row-1, col+1), copyTuple)
                A += getPixel((row, col+1), copyTuple)
                A += getPixel((row+1,col+1), copyTuple)
                A += getPixel((row+1,col), copyTuple)
                A = A//5
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif col !=0 and row == 0 and col != A-1:
                P = copyTuple[3][0][col]
                A = 0
                A += getPixel((row, col-1), copyTuple)
                A += getPixel((row+1, col-1), copyTuple)
                A += getPixel((row+1, col), copyTuple)
                A += getPixel((row+1, col+1), copyTuple)
                A += getPixel((row, col+1), copyTuple)
                A = A//5
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif row!=0 and col == A-1 and row != B-1:
                P = copyTuple[3][row][A-1]
                A = 0
                A += getPixel((row-1,col), copyTuple)
                A += getPixel((row-1, col+1), copyTuple)
                A += getPixel((row, col+1), copyTuple)
                A += getPixel((row+1, col+1), copyTuple)
                A += getPixel((row+1, col), copyTuple)
                A = A//5
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            elif col !=0 and row == B-1 and col != A-1:
                P = copyTuple[3][B-1][col]
                A = 0
                A += getPixel((row, col-1), copyTuple)
                A += getPixel((row+1, col-1), copyTuple)
                A += getPixel((row+1, col), copyTuple)
                A += getPixel((row+1, col+1), copyTuple)
                A += getPixel((row, col+1), copyTuple)
                A = A//5
                newValue = floor((P*W+A)/(W+1))
                setPixel((row,col),newValue,(A,B,C,D))
            else:
                P = copyTuple[3][row][col]
                A = 0
                A += getPixel((row, col+1), copyTuple)
                A += getPixel((row, col-1), copyTuple)
                A += getPixel((row+1, col+1), copyTuple)
                A += getPixel((row+1, col-1), copyTuple)
                A += getPixel((row+1, col), copyTuple)
                A += getPixel((row-1, col), copyTuple)
                A += getPixel((row-1, col+1), copyTuple)
                A += getPixel((row-1, col-1), copyTuple)
                A = A//8
                newValue = floor((P*W+A)/(W+1))
                setPixel((row, col),newValue, (A,B,C,D))


 
def main(argv):
    PGM = loadPGM(argv[1])
    drawLine((0,0), (PGM[1]-1, PGM[0]-1), 0, PGM)
    drawLine((0,PGM[0]-1), (PGM[1]-1, 0 ), 0, PGM)
    smooth(3, PGM)
    smooth(3, PGM)
    smooth(3, PGM)
    smooth(3, PGM)
    writePGM(argv[2], PGM)
    

  
    

if __name__ == "__main__":
    main(sys.argv)
