import argparse
parser=argparse.ArgumentParser(description="Convert mathematica CForm expressions into Python methods")
parser.add_argument('inFile',help="Textfile containing mathematica output")
parser.add_argument('outFile', help="File in which to write new python methods")
args=parser.parse_args()


def getSymbols(equation):
    """Return a set of symbols present in the equation"""
    stopchars=['(',')','*','/','+','-',',']
    symbols=set()
    pos=0
    symbol=""
    for i, c in enumerate(equation,1):
        if c in stopchars:
            pos=i
            if(len(symbol)!=0):
                if not all(i.isdigit() for i in symbol):
                    if not '.' in symbol:
                        symbols.add(symbol)
                symbol=""
            
        else:
            symbol+=c
    if(len(symbol)!=0):
                if not all(i.isdigit() for i in symbol):
                    if not '.' in symbol:
                        symbols.add(symbol)
    return symbols


inFileLines=[]
equations=[]

with open(args.inFile) as file:
    inFileLines=file.readlines()

big_mathematica_output = "".join(inFileLines)
big_mathematica_output=big_mathematica_output.replace("\n","").replace(" ","").replace('Power', 'np.power').replace('Sqrt', 'np.sqrt')

if(big_mathematica_output[0:5]=='List('):
    equation_begin_pos=0
    print("List found, splitting")
    big_mathematica_output=big_mathematica_output[5:-1]

bracketlevelcounter=0
for i, c in enumerate(big_mathematica_output):
    if c=='(':
        bracketlevelcounter+=1
    if c==')':
        bracketlevelcounter-=1
    if c==',' and bracketlevelcounter==0:
        equations.append(big_mathematica_output[equation_begin_pos:i])
        equation_begin_pos=i+1
equations.append(big_mathematica_output[equation_begin_pos:])

with open(args.outFile, 'w') as outFile:
    outFile.write("import numpy as np\n")
    for index, eq in enumerate(equations):
        outFile.write("def eqtn"+str(index)+"("+",".join(sorted(getSymbols(eq)))+"):\n")
        outFile.write("\treturn "+eq+"\n")
