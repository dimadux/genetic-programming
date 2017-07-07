import math
def game(p):
    field = (3,3)
    fieldlist = [0,0,0,0,0,0,0,0,0,0]
    lastturn = [-1,-1]
    playermark = [1,2]
    for turn in range(9):
        for i in range(2):
            move = int(p[i].evaluate(fieldlist)%9)
            if fieldlist[move]!=0: return 1-i
            fieldlist[move]=playermark[i]
            lastturn[i]=move
            if wincondition(fieldlist,playermark)!=False:
                return wincondition(fieldlist,playermark)
    return -1



def wincondition(fieldlist,playermark):
    if fieldlist[1]==playermark and fieldlist[2]==playermark and fieldlist[0]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[3]==playermark and fieldlist[4]==playermark and fieldlist[5]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[6]==playermark and fieldlist[7]==playermark and fieldlist[8]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[0]==playermark and fieldlist[3]==playermark and fieldlist[6]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[1]==playermark and fieldlist[4]==playermark and fieldlist[7]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[2]==playermark and fieldlist[5]==playermark and fieldlist[8]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[0]==playermark and fieldlist[4]==playermark and fieldlist[8]==playermark:
        return math.fabs(1-playermark)
    if fieldlist[2]==playermark and fieldlist[4]==playermark and fieldlist[6]==playermark:
        return math.fabs(1-playermark)
    else:
        return False


def tournament(pl):

    losses=[0 for p in pl]

  # Every player plays every other player
    for i in range(len(pl)):
        for j in range(len(pl)):
            if i==j: continue

      # Who is the winner?
            winner=game([pl[i],pl[j]])

      # Two points for a loss, one point for a tie
            if winner==0:
                losses[j]+=2
            elif winner==1:
                losses[i]+=2
            elif winner==-1:
                losses[i]+=1
                losses[i]+=1
                pass

  # Sort and return the results
    return sorted(zip(losses,pl), key = lambda x: x[0])
