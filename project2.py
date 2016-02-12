import sys
    
    

def loadSATProblem(dimacsfile):
    dimacs = open(dimacsfile,"r")
    lines = [lines.strip() for lines in dimacs]
    
    numVars = 0
    numClauses = 0
    clauses = []
    variables = {}  
    for line in lines:
        if not line:
            continue  #skip lines with no content
        elif line[0] == 'c':
            continue #skip lines with comments on them
        elif line[0] == 'p':
            chunks = line.split()
            numVars = int(chunks[2])
            numClauses = int(chunks[3])
        else:
            #turn string into a list of numbers
            numbers = [int(x) for x in line.split() if x != '0']
            #determine the number of the next clause
            clauseNum = len(clauses)
            #start off with empty positive and negative components
            pos = []
            neg = []
            #for each variable in the clause
            for n in numbers:
                #determine whether it belongs in negative or positive component
                if n < 0:
                    neg.append(abs(n))
                else:
                    pos.append(n)
                n = abs(n)
                #create the variable with assignment None if it does not exist yet
                #add the clause number to the list of clauses the variable is in
                if n not in variables:
                    variables[n] = [None, set([clauseNum])]
                else:
                    [assignment, vclauses] = variables[n]
                    
                    vclauses.add(clauseNum)
                
            clauses.append([set(pos+neg), set(), set(), set(pos), set(neg)] )

    dimacs.close()
    return (variables, clauses)

def thereIsNoSolution(filename):
    print("No Solution Found")
    file = open(filename, "w")
    file.write("none")
    file.close()
    exit()

def thereIsASolution(filename, assignments):
    print("Solution Found")
    numbers = []
    for [var, val] in assignments:
        if not val:
            var = var*-1
        numbers.append(var)
    numbers = reversed(sorted(numbers))
    file = open(filename, "w")
    for n in numbers:
        file.write(str(n) + " ");
    file.close()
    exit()
    
    
def performAssignment(newAssign, problemState):
    [variables, clauses, uVars, uClauses, fClauses, assignments, guesses] = problemState
    var = newAssign[0]
    val = newAssign[1]
    uVars.discard(var)
    vData = variables[var]
    vData[0] = val  #record assignment
    cList = vData[1] #list of clauses that the variable occurs within.
    for c in cList:
        cData = clauses[c]
        [ucVars, tVars, fVars,pos, neg] = cData
        if var not in ucVars:
            print(var, c, cData)
            print("variable was not in unassigned set")
            exit(-1)
        ucVars.remove(var)
        if var in pos:
            if val:
                tVars.add(var)
                uClauses.discard(c)
            else:
                fVars.add(var)
        elif var in neg:
            if val:
                fVars.add(var)
            else:
                tVars.add(var)
                uClauses.discard(c)
        else:
            print(var, c, cData)
            print("variable was in unassigned variables but did not occur in clause positively or negatively")
            exit(-1)
        #check if clause was falsified, no unassigned variables, none contribute truth.  
        if len(ucVars) == 0 and len(tVars) == 0:
            fClauses.add(c)
        

def reverseAssignment(oldAssign, problemState):
    [variables, clauses, uVars, uClauses, fClauses, assignments, guesses] = problemState
    var = oldAssign[0]
    val = oldAssign[1]
    uVars.add(var)
    vData = variables[var]
    if vData[0] != val:
        print(oldAssign, var, vData)
        print("Cannot reverse assignment when the variable's recorded value does not match")
        exit(-1)
    vData[0] = None  #erase assignment
    cList = vData[1] #list of clauses that the variable occurs within.
    for c in cList:
        cData = clauses[c]
        [ucVars, tVars, fVars,pos, neg] = cData
        if var in tVars:
            tVars.remove(var)
        elif var in fVars:
            fVars.remove(var)
        else:
            print(var, c, cData)
            print("variable was not in either assigned set")
            exit(-1)
        #mark variable as unassigned in clause
        ucVars.add(var)
        #If clause has no truth supporting variable assignments, mark clause as unsatisfied
        if len(tVars) == 0:
            uClauses.add(c)
        #whether it was falsified or not, it is not falsified now
        fClauses.discard(c)

def unitPropegation(problemState):
    [variables, clauses, uVars, uClauses, fClauses, assignments, guesses] = problemState

    performedUP = False

    #collect all clauses with 1 unassigned variables
    for c in range(len(clauses)):
        [ucVars, tVars, fVars,pos, neg] = clauses[c]
        if len(ucVars) == 1 and c in uClauses and c not in fClauses:
            #Add a new assignment to the problem state which satisfied the clause c
            lVars = list(ucVars)
            for var in lVars:
                #will execute only once due to len(ucVars) == 1
                if var in pos:
                    newAssign = [var, True]
                elif var in neg:
                    newAssign = [var, False]
                else:
                    print(var, c, ucVars, tVars, fVars,pos, neg)
                    print("variable was in unassigned variables but did not occur in clause positively or negatively")
                    exit(-1)
                assignments.append(newAssign)
                performAssignment(newAssign, problemState)
                performedUP = True
        else:
            #skip clause and continue to next clause
            continue
    return performedUP        
                    
            

def guessNextAssignment(problemState):
    [variables, clauses, uVars, uClauses, fClauses, assignments, guesses] = problemState
    var = None
    if len(uVars) == 0:
        print("Can't guess next Assignment when there are no unassigned variables")
        exit(-1)
    
    #insert code here about making intelligent guesses for next variable to assign
    #currently returning the naive guess and assignment.  
    for var in uVars:
        break
    return [var, True]

def main(argv):

    dimacsfile = argv[1]
    resultfile = argv[2]
    chatty= False
    veryChatty = False
    if "chatty" in argv:
        chatty = True
    if "verychatty" in argv:
        chatty = True
        veryChatty = True

    if chatty:
        print("Loading File: " + dimacsfile)
    
    (variables, clauses) = loadSATProblem(dimacsfile)
    if chatty:
        print("Done Loading File")
    #Stack of Assignments:
    assignments = []
    #Stack of guesses:
    guesses = []
    #unassigned vars
    uVars = set(variables.keys())
    #unsatisfied clauses
    uClauses = set(range(len(clauses)))
    #falsified clauses (start backtracking)
    fClauses = set()
    #backtrack flag
    backtrack = False

    problemState = [variables, clauses, uVars, uClauses, fClauses, assignments, guesses]

    firstPass = True
    while len(uClauses) > 0 :
        #print(backtrack, uVars, uClauses, fClauses, assignments, guesses)
        #input("press enter to continue")
        if backtrack:
            numAssign = len(assignments)
            numGuess = len(guesses)
            if numAssign == 0:
                thereIsNoSolution(resultfile)  #exits the script if called
            elif numGuess > 0 and guesses[-1] == numAssign -1:
                #need to handle backtracking on a guess,
                #remove the guessed assignment,
                #undo its effects,
                #remove the guess,
                #make the opposite assignment and propegate its effects into clauses.
                #stop backtracking
                lastAssign = assignments.pop()
                guesses.pop()
                reverseAssignment(lastAssign, problemState)
                newAssign = [lastAssign[0], not lastAssign[1]]
                if chatty:
                   print("Reversing Guess: "+str(newAssign))
                assignments.append(newAssign)
                performAssignment(newAssign, problemState)
                backtrack = False
                continue
            else:
                #remove the assignment, undo its effects, and continue backtracking.
                lastAssign = assignments.pop()
                reverseAssignment(lastAssign, problemState)
                continue
        else:
            
            if chatty and firstPass:
                print("Performing Initial Unit Propegation")
                firstPass = False
            if veryChatty:
                print("Performing Unit Propegation")
            while unitPropegation(problemState) and len(fClauses) == 0:
                continue
            if len(fClauses) > 0:
                backtrack = True
                if veryChatty:
                    print("Initiating Backtracking")
                continue
            if len(uClauses) == 0:
                thereIsASolution(argv[2], assignments) #will print and exit script
            newAssign = guessNextAssignment(problemState)
            if chatty:
                print("Guessing: "+str(newAssign))
            guesses.append(len(assignments))
            assignments.append(newAssign)
            performAssignment(newAssign, problemState)
            if len(fClauses) > 0:
                backtrack = True
                if veryChatty:
                    print("Initiating Backtracking")
                continue
            if len(uClauses) == 0:
                thereIsASolution(resultfile, assignments) #will print and exit script


if __name__ == "__main__":
    main(sys.argv)
