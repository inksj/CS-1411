def printLine(n):
    s=""
    for i in range(n):
        s+="*"
    print(s)

def printTop(n):
    if n==1:
        printLine(1)
    else:
        printLine(n)
        printTop(n-1)

def printBottom(n):
    if n==1:
        printLine(1)
    else:
        printLine(n)
        printBottom(n-1)

def printImage(n):
    printTop(n-1)
    printLine(n)
    printBottom(n-1)
    
def main():
    n=4
    printImage(n)

if __name__== "__main__":
    main()
