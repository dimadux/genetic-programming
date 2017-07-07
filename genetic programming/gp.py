from random import random,randint,choice
from copy import deepcopy
from math import log
import math

class fwrapper:
    def __init__(self,function,childcount,name):
        self.function=function
        self.childcount=childcount
        self.name=name

class node:
    def __init__(self,fw,children):
        self.function=fw.function
        self.name=fw.name
        self.children=children

    def evaluate(self,inp):
        results=[n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self,indent=0):
        try:
            print((" "*(indent))+str(self.name))
        except:
            print("")
        for c in self.children:
            c.display(indent+1)


class paramnode:
    def __init__(self,idx):
        self.idx=idx

    def evaluate(self,inp):
        return inp[self.idx]
    def display(self,indent=0):
        try:
            print ("%sp%d") % (" "*indent,self.idx)
        except:
            print ("")
class constnode:
    def __init__(self,v):
        self.v=v
    def evaluate(self,inp):
        return self.v
    def display(self,indent=0):
        try:
            print ("%s%d") % (" "*indent,self.v)
        except:
            print ("")

addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')


def addNode(l):
    for i in l:
        if random()<0.5:
            return paramnode(i)
def iffunc(l):
    if l[0]>0: return l[1]
    else: return l[2]

ifw=fwrapper(iffunc,3,'if')
nodew = fwrapper(addNode,1,"node")
def isgreater(l):
    if l[0]>l[1]: return 1
    else: return 0

def sinus(l):
    return math.sin(l[0])

gtw=fwrapper(isgreater,2,'isgreater')
sinw = fwrapper(sinus,1,"sinus")
flist=[addw,mulw,ifw,gtw,subw,sinw]


def makerandomtree(pc,maxdepth=6,fpr=0.5,ppr=0.6):
    if random()<fpr and maxdepth>0:
        f=choice(flist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr)
                           for i in range(f.childcount)]
        return node(f,children)
    elif random()<ppr:
        return paramnode(randint(0,pc-1))
    else:
        return constnode(randint(0,10))

def scorefunction(tree,s):
    dif=0
    for data in s:
        v=tree.evaluate([data[0],data[1]])
        dif+=abs(v-data[2])
    return dif

def mutate(t,pc,probchange=0.1):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if hasattr(t,"children"):
            result.children=[mutate(c,pc,probchange) for c in t.children]
    return result

def crossover(t1,t2,probswap=0.7,top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if hasattr(t1,'children') and hasattr(t2,'children'):
            result.children=[crossover(c,choice(t2.children),probswap,0)
                       for c in t1.children]
    return result


def getrankfunction(dataset):
    def rankfunction(population):
        scores=[(scorefunction(t,dataset),t) for t in population]
        scores.sort()
        return scores
    return rankfunction



def evolve(pc,popsize,rankfunction,maxgen=500,
           mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
  # Returns a random number, tending towards lower numbers. The lower pexp
  # is, more lower numbers you will get
    def selectindex():
        return int(log(random())/log(pexp))

  # Create a random initial population
    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        print (scores[0][0])
        if scores[0][0]==0: break

    # The two best always make it
        newpop=[scores[0][1],scores[1][1]]

    # Build the next generation
        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(mutate(
                      crossover(scores[selectindex()][1],
                                 scores[selectindex()][1],
                                probswap=breedingrate),
                        pc,probchange=mutationrate))
            else:
      # Add a random node to mix things up
                newpop.append(makerandomtree(pc))

        population=newpop
    scores[0][1].display()
    return scores[0][1]
