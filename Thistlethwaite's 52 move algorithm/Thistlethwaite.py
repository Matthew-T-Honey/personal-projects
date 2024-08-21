from rubikscube import Cube
from rubiksmath import Point
import copy
import random

#https://www.jaapsch.net/puzzles/thistle.htm

c = Cube("YYYYYYYYYRRRGGGOOOBBBRRRGGGOOOBBBRRRGGGOOOBBBWWWWWWWWW")
moves=["L","Li","L2","R","Ri","R2","F","Fi","F2","B","Bi","B2","U","Ui","U2","D","Di","D2"]
G1moves=["L","Li","L2","R","Ri","R2","F","Fi","F2","B","Bi","B2","U2","D2"]
G2moves=["L","Li","L2","R","Ri","R2","F2","B2","U2","D2"]
G3moves=["L2","R2","F2","B2","U2","D2"]

movemappings1=[["L","Li","L2","R","Ri","R2","F","Fi","F2","B","Bi","B2","U2","D2"],
              ["R","Ri","R2","L","Li","L2","B","Bi","B2","F","Fi","F2","U2","D2"],
              ["R","Ri","R2","L","Li","L2","F","Fi","F2","B","Bi","B2","D2","U2"],
              ["L","Li","L2","R","Ri","R2","B","Bi","B2","F","Fi","F2","D2","U2"],
              ["Li","L","L2","Ri","R","R2","Bi","B","B2","Fi","F","F2","U2","D2"],
              ["Ri","R","R2","Li","L","L2","Fi","F","F2","Bi","B","B2","U2","D2"],
              ["Ri","R","R2","Li","L","L2","Bi","B","B2","Fi","F","F2","D2","U2"],
              ["Li","L","L2","Ri","R","R2","Fi","F","F2","Bi","B","B2","D2","U2"]]

movemappings2=[["L","Li","L2","R","Ri","R2","F2","B2","U2","D2"],
              ["L","Li","L2","R","Ri","R2","U2","D2","B2","F2"],
              ["L","Li","L2","R","Ri","R2","B2","F2","D2","U2"],
              ["L","Li","L2","R","Ri","R2","D2","U2","F2","B2"],
              ["R","Ri","R2","L","Li","L2","B2","F2","U2","D2"],
              ["R","Ri","R2","L","Li","L2","U2","D2","F2","B2"],
              ["R","Ri","R2","L","Li","L2","F2","B2","D2","U2"],
              ["R","Ri","R2","L","Li","L2","D2","U2","B2","F2"],
              ["Li","L","L2","Ri","R","R2","B2","F2","U2","D2"],
              ["Li","L","L2","Ri","R","R2","U2","D2","F2","B2"],
              ["Li","L","L2","Ri","R","R2","F2","B2","D2","U2"],
              ["Li","L","L2","Ri","R","R2","D2","U2","B2","F2"],
              ["Ri","R","R2","Li","L","L2","F2","B2","U2","D2"],
              ["Ri","R","R2","Li","L","L2","U2","D2","B2","F2"],
              ["Ri","R","R2","Li","L","L2","B2","F2","D2","U2"],
              ["Ri","R","R2","Li","L","L2","D2","U2","F2","B2"]]

movemappings3=[["L2","R2","F2","B2","U2","D2"],["L2","R2","U2","D2","B2","F2"],["L2","R2","B2","F2","D2","U2"],["L2","R2","D2","U2","F2","B2"],
               ["B2","F2","L2","R2","U2","D2"],["B2","F2","U2","D2","R2","L2"],["B2","F2","R2","L2","D2","U2"],["B2","F2","D2","U2","L2","R2"],
               ["R2","L2","B2","F2","U2","D2"],["R2","L2","U2","D2","F2","B2"],["R2","L2","F2","B2","D2","U2"],["R2","L2","D2","U2","B2","F2"],
               ["F2","B2","R2","L2","U2","D2"],["F2","B2","U2","D2","L2","R2"],["F2","B2","L2","R2","D2","U2"],["F2","B2","D2","U2","R2","L2"],
               ["D2","U2","F2","B2","L2","R2"],["D2","U2","L2","R2","B2","F2"],["D2","U2","B2","F2","R2","L2"],["D2","U2","R2","L2","F2","B2"],
               ["U2","D2","F2","B2","R2","L2"],["U2","D2","R2","L2","B2","F2"],["U2","D2","B2","F2","L2","R2"],["U2","D2","L2","R2","F2","B2"],
               ["L2","R2","B2","F2","U2","D2"],["L2","R2","U2","D2","F2","B2"],["L2","R2","F2","B2","D2","U2"],["L2","R2","D2","U2","B2","F2"],
               ["F2","B2","L2","R2","U2","D2"],["F2","B2","U2","D2","R2","L2"],["F2","B2","R2","L2","D2","U2"],["F2","B2","D2","U2","L2","R2"],
               ["R2","L2","F2","B2","U2","D2"],["R2","L2","U2","D2","B2","F2"],["R2","L2","B2","F2","D2","U2"],["R2","L2","D2","U2","F2","B2"],
               ["B2","F2","R2","L2","U2","D2"],["B2","F2","U2","D2","L2","R2"],["B2","F2","L2","R2","D2","U2"],["B2","F2","D2","U2","R2","L2"],
               ["D2","U2","B2","F2","L2","R2"],["D2","U2","L2","R2","F2","B2"],["D2","U2","F2","B2","R2","L2"],["D2","U2","R2","L2","B2","F2"],
               ["U2","D2","B2","F2","R2","L2"],["U2","D2","R2","L2","F2","B2"],["U2","D2","F2","B2","L2","R2"],["U2","D2","L2","R2","B2","F2"]]




def bad_edges(c):
    edges=list(c.edges)
    count=0
    
    for edge in edges:
        if edge.colors[0] in ['O','R']:
            pass
        elif edge.colors[2] in ['G','B']:
            pass
        elif edge.colors[1] in ['O','R'] and edge.colors[2] in ['G','B','W','Y']:
            pass
        elif edge.colors[1] in ['G','B'] and edge.colors[0] in ['O','R','W','Y']:
            pass
        else:
            count+=1
            
    return count

def bad_edges_on_ud(c):
    edges=list(c.edges)
    count=0
    
    for edge in edges:
        if edge.colors[1]!=None:
            if edge.colors[0] in ['O','R']:
                pass
            elif edge.colors[2] in ['G','B']:
                pass
            elif edge.colors[1] in ['O','R'] and edge.colors[2] in ['G','B','W','Y']:
                pass
            elif edge.colors[1] in ['G','B'] and edge.colors[0] in ['O','R','W','Y']:
                pass
            else:
                count+=1
            
    return count
    
    
def Stage1(c):
    queue=[[copy.deepcopy(c)]]
    found=False
    print("Calculating Stage 1")
    while True:
        for m in moves:
            if not (len(queue[0])==7 and m[0] not in ['U','D']):
                if len(queue[0])==1:
                    similar=False
                elif queue[0][-1][0]!=m[0]:
                    similar=False
                else:
                    similar=True
                if similar==False:
                    new=copy.deepcopy(queue[0][0])
                    new.sequence(m)
                    
                    b=bad_edges(new)
                    bud=bad_edges_on_ud(new)
                    
                    if b==0:
                        found=m
                        break
                    elif len(queue[0])==6 and (b!=4 or bud!=4):
                        pass
                    elif len(queue[0])==5 and (b not in [4,8] or bud not in [8,4,3]):
                        pass
                    elif len(queue[0])==4 and b not in [2,4,8]:
                        pass
                    else:
                        queue.append([new]+queue[0][1:]+[m])
        if found!=False:
            return queue[0][1:]+[m]
        queue.pop(0)
        

def Stage2(c):
    queue=[[copy.deepcopy(c)]]
    found=False
    print("Calculating Stage 2")
    while True:
        for m in G1moves:
            if len(queue[0])==1:
                similar=False
            elif queue[0][-1][0]!=m[0]:
                similar=False
            else:
                similar=True
            if similar==False:
                new=copy.deepcopy(queue[0][0])
                new.sequence(m)
                
                lredges=[]
                for p in new.pieces:
                    for i in [['Y','B'],['B','W'],['W','G'],['G','Y']]:
                        if i[0] in p.colors and i[1] in p.colors and None in p.colors:
                            lredges.append(p)
                if [p.pos.y for p in lredges]==[0,0,0,0]:
                    found=m
                    break
                else:
                    queue.append([new]+queue[0][1:]+[m])

        if found!=False:
            return queue[0][1:]+[m]
        queue.pop(0)


def Stage3(c):
    
    print("Calculating Stage 3")
    f = open("Stage 2.txt")
    
    lines=f.readlines()
    f.close()
    
    moves=[]
    twists=[]
    
    nums=[11,12,13,21,22,23,31,32,33,41,42,43,51,52]
    translation=["Li","L2","L","Fi","F2","F","Ri","R2","R","Bi","B2","B","U2","D2"]
    
    for l in lines:
        s=list(filter(None,l.split(" ")))[:-1]
        moves.append(s[:9])
        twists.append(s[9:])
        
    
    for m in range(len(moves)):
        for i in range(len(moves[m])):
            moves[m][i]=translation[nums.index(int(moves[m][i]))]
        moves[m].reverse()
        if moves[m][-1]=="Li":
            moves[m].append("Fi")
            
    for t in range(len(twists)):
        for i in range(len(twists[t])):
            twists[t][i]=int(twists[t][i])
            
    
    symetries=[copy.deepcopy(c) for i in range(8)]
    for i in range(4,8):
        symetries[i].reflect(Point(1,1,-1))
    for i in [1,3,5,7]:
        symetries[i].Y()
        symetries[i].Y()
    for i in [2,3,6,7]:
        symetries[i].Z()
        symetries[i].Z()
    
    for s in symetries:
        corners=[[-1,1,-1],[-1,-1,1],[1,-1,-1],[1,1,1],[-1,1,1],[-1,-1,-1],[1,-1,1],[1,1,-1]]
        found=False
        ts=[]
        for cc in corners:
            corner = s.get_piece(cc[0],cc[1],cc[2])
            if corner.colors[0] in ['O','R']:
                t=0
            elif corner.colors[1] in ['O','R'] and cc in [[-1,1,1],[-1,-1,-1],[1,-1,1],[1,1,-1]]:
                t=1
            elif corner.colors[2] in ['O','R'] and cc in [[-1,1,1],[-1,-1,-1],[1,-1,1],[1,1,-1]]:
                t=2
            elif corner.colors[1] in ['O','R'] and cc in [[-1,1,-1],[-1,-1,1],[1,-1,-1],[1,1,1]]:
                t=2
            elif corner.colors[2] in ['O','R'] and cc in [[-1,1,-1],[-1,-1,1],[1,-1,-1],[1,1,1]]:
                t=1
                
            ts.append(t)
        if ts in twists:
            found=[symetries.index(s),ts]
            break
    
    if not found:
        return
    
    sol=moves[twists.index(found[1])]
        
    
    
    for s in range(len(sol)):
        sol[s]=movemappings1[found[0]][G1moves.index(sol[s])]
        
    return sol
        

def ooo(c):
    corners=[[-1,1,-1],[-1,-1,1],[1,-1,-1],[1,1,1],[-1,1,1],[-1,-1,-1],[1,-1,1],[1,1,-1]]
   
    ooo=[]
    for cc in corners:
        corner = c.get_piece(cc[0],cc[1],cc[2])
        middles= [c.get_piece(0,1,0).colors[1],c.get_piece(0,-1,0).colors[1]]
        if corner.colors[1] not in middles:
            ooo.append(corners.index(cc)+1)
    
    return ooo


def Stage4(c):
    
    print("Calculating Stage 4")
    sol=[]
    
    symetries=[copy.deepcopy(c) for i in range(16)]
    for i in range(8,16):
        symetries[i].reflect(Point(1,1,-1))
    for i in [1,5,9,13]:
        symetries[i].X()
    for i in [2,6,10,14]:
        symetries[i].X()
        symetries[i].X()
    for i in [3,7,11,15]:
        symetries[i].Xi()
    for i in [4,5,6,7,12,13,14,15]:
        symetries[i].Y()
        symetries[i].Y()
    
    
    
    ooo_corners=[[1,5],                
                [1,6],                    
                [1,7],                    
                [1,8],                    
                [1,2,5,6],                
                [1,2,5,7],                
                [1,2,5,8],                
                [1,2,7,8],                
                [1,3,6,8],                
                [1,3,5,7],                
                [1,3,5,8],                
                [1,2,3,5,6,7],            
                [1,2,3,5,7,8],            
                [1,2,3,6,7,8],            
                [1,2,3,4,5,6,7,8]]   
    
    moves=[[],[],["F2"],["L2","U2"],["L"],["L","F2"],["Li","U2"],[],["U2"],["R2","F2"],["L","U2"],["L"],["F2","R"],["L","R","U2"],["L","R"]]
    
    
    
    for s in symetries:
        if ooo(s) in ooo_corners:
            for m in moves[ooo_corners.index(ooo(s))]:
                sol+=[movemappings2[symetries.index(s)][G2moves.index(m)]]
            break
    return sol            
                
def in_G3(c):
    correct=True
    for corner in c.corners:
        if corner.pos.x==1:
            if corner.colors[0]!=c.get_piece(1,0,0).colors[0]:
                correct=False
        elif corner.pos.x==-1:
            if corner.colors[0]!=c.get_piece(-1,0,0).colors[0]:
                correct=False
        if corner.pos.y==1:
            if corner.colors[1]!=c.get_piece(0,1,0).colors[1]:
                correct=False
        elif corner.pos.y==-1:
            if corner.colors[1]!=c.get_piece(0,-1,0).colors[1]:
                correct=False
        if corner.pos.z==1:
            if corner.colors[2]!=c.get_piece(0,0,1).colors[2]:
                correct=False
        elif corner.pos.z==-1:
            if corner.colors[2]!=c.get_piece(0,0,-1).colors[2]:
                correct=False
    return correct
            
    

def edges_in_G3(c):
    correct=True
    for edge in c.edges:
        if edge.pos.x in [-1,1]:
            if edge.colors[0] not in [c.get_piece(1,0,0).colors[0],c.get_piece(-1,0,0).colors[0]]:
                correct=False
        if edge.pos.y in [-1,1]:
            if edge.colors[1] not in [c.get_piece(0,1,0).colors[1],c.get_piece(0,-1,0).colors[1]]:
                correct=False
        if edge.pos.z in [-1,1]:
            if edge.colors[2] not in [c.get_piece(0,0,1).colors[2],c.get_piece(0,0,-1).colors[2]]:
                correct=False
    return correct



def Stage5(c):
    print("Calculating Stage 5")
    
    symetries=[copy.deepcopy(c) for i in range(16)]
    for i in range(8,16):
        symetries[i].reflect(Point(1,1,-1))
    for i in [4,5,6,7,12,13,14,15]:
        symetries[i].Y()
        symetries[i].Y()
    for i in [1,5,9,13]:
        symetries[i].Xi()
    for i in [2,6,10,14]:
        symetries[i].X()
        symetries[i].X()
    for i in [3,7,11,15]:
        symetries[i].X()
    
    
    
    o=False
    valid_symetries=[]
    for s in symetries:
        if ooo(s) in [[],[1,5],[1,2,7,8]]:
            valid_symetries.append(s)
            o=ooo(s)
    if o==False:
        print("symetry not found")
        return []
    if o==[]:
        f=open("Stage 3a.txt")
    elif o==[1,2,7,8]:
        f=open("Stage 3b.txt")
    elif o==[1,5]:
        f=open("Stage 3c.txt")
    else:
        return []
    lines=f.readlines()
    f.close()

    edgesolutions=[]
    movesolutions=[]

    for line in lines:
        spl=line[:-1].split(" ")
        moveset=[]
        if spl[0] not in edgesolutions:
            edgesolutions.append(spl[0])
            movesolutions.append([])
            for i in range(1,len(spl)):
                if spl[i]!="":
                    if spl[i-1]=="" and spl[i-2]=="":
                        if moveset!=[]:
                            movesolutions[-1].append(moveset)
                        moveset=[spl[i]]
                    else:
                        moveset.append(spl[i])
            movesolutions[-1].append(moveset)
        else:
            for i in range(1,len(spl)):
                if spl[i]!="":
                    if spl[i-1]=="" and spl[i-2]=="":
                        if moveset!=[]:
                            movesolutions[edgesolutions.index(spl[0])].append(moveset)
                        moveset=[spl[i]]
                    else:
                        moveset.append(spl[i])
            movesolutions[edgesolutions.index(spl[0])].append(moveset)
    
    translation=["Li","L2","L","F2","Ri","R2","R","B2","U2","D2"]
    
    
    found=False
    for v in valid_symetries:
        if found!=False:
            break
        e=[]
        edges=[[-1,1,0],[-1,-1,0],[1,1,0],[1,-1,0],[-1,0,-1],[-1,0,1],[1,0,1],[1,0,-1],[0,1,1],[0,-1,1],[0,-1,-1],[0,1,-1]]
        for edge in edges:
            ee=v.get_piece(edge[0],edge[1],edge[2])
            top=v.get_piece(0,1,0).colors[1]
            bottom=v.get_piece(0,-1,0).colors[1]
            if ('O' in ee.colors or 'R' in ee.colors) and (top in ee.colors or bottom in ee.colors):
                e.append(str(edges.index(edge)+1))
        if ("").join(e) in edgesolutions:
            for m2 in movesolutions[edgesolutions.index(("").join(e))]:
                #print("checking",(" ").join(list(reversed([translation[int(x)-1] for x in m2]))))
                v2=copy.deepcopy(v)
                v2.sequence((" ").join(list(reversed([translation[int(x)-1] for x in m2]))))
                
                if edges_in_G3(v2):
                    found2=False
                    queue=[[copy.deepcopy(v2)]]
                    while True:
                        if len(queue[0])>5:
                            break
                        for m in G3moves:
                            if len(queue[0])==1:
                                similar=False
                            elif queue[0][-1][0]!=m[0]:
                                similar=False
                            else:
                                similar=True
                            if similar==False:
                                new=copy.deepcopy(queue[0][0])
                                new.sequence(m)
                                
                                if in_G3(new):
                                    found2=queue[0][1:]+[m]
                                    break
                                else:
                                    queue.append([new]+queue[0][1:]+[m])
    
                        if found2!=False:
                            break
                        queue.pop(0)
                    if found2!=False:
                        found=[list(reversed([translation[int(x)-1] for x in m2]))+found2,v]
                        break
        if found!=False:
            break
                    
    if found!=False:
        return [movemappings2[symetries.index(found[1])][G2moves.index(f)] for f in found[0]]
    else:
        return []


def Stage6(c):
    print("Calculating Stage 6")
    f=open("Stage 4.txt")

    lines=f.readlines()
    f.close()
    
    solutions=[]
    fbs=[]
    uds=[]
    lrs=[]
    for line in lines:
        
        solutions.append(" ".join(line[1:28].split()))
    
        fbs.append(sorted(list(" ".join(line[30:38].split()).replace("(","").replace(")",""))))
        uds.append(sorted(list(" ".join(line[40:48].split()).replace("(","").replace(")",""))))
        lrs.append(sorted(list(" ".join(line[50:58].split()).replace("(","").replace(")",""))))
    
    
    symetries=[copy.deepcopy(c) for i in range(48)]
    for i in range(24,48):
        symetries[i].reflect(Point(1,1,-1))
    for i in [4,5,6,7,28,29,30,31]:
        symetries[i].Yi()
    for i in [8,9,10,11,32,33,34,35]:
        symetries[i].Y()
        symetries[i].Y()
    for i in [12,13,14,15,36,37,38,39]:
        symetries[i].Y()
    for i in [16,17,18,19,40,41,42,43]:
        symetries[i].Z()
    for i in [20,21,22,23,44,45,46,47]:
        symetries[i].Zi()
    for i in [4*j+1 for j in range(12)]:
        symetries[i].Xi()
    for i in [4*j+2 for j in range(12)]:
        symetries[i].X()
        symetries[i].X()
    for i in [4*j+3 for j in range(12)]:
        symetries[i].X()
    
    translation=["L2","F2","R2","B2","U2","D2"]
        
    
    
    for s in symetries:

        fbedges=[[-1,1,0],[-1,-1,0],[1,-1,0],[1,1,0]]
        udedges=[[-1,0,-1],[-1,0,1],[1,0,1],[1,0,-1]]
        lredges=[[0,1,1],[0,-1,1],[0,-1,-1],[0,1,-1]]
        
        fbwrong=[]
        udwrong=[]
        lrwrong=[]
        
        for coord in fbedges:
            edge=s.get_piece(coord[0],coord[1],coord[2])
            correct=True
            if edge.pos.x==1:
                if edge.colors[0]!=s.get_piece(1,0,0).colors[0]:
                    correct=False
            elif edge.pos.x==-1:
                if edge.colors[0]!=s.get_piece(-1,0,0).colors[0]:
                    correct=False
            if edge.pos.y==1:
                if edge.colors[1]!=s.get_piece(0,1,0).colors[1]:
                    correct=False
            elif edge.pos.y==-1:
                if edge.colors[1]!=s.get_piece(0,-1,0).colors[1]:
                    correct=False
            if edge.pos.z==1:
                if edge.colors[2]!=s.get_piece(0,0,1).colors[2]:
                    correct=False
            elif edge.pos.z==-1:
                if edge.colors[2]!=s.get_piece(0,0,-1).colors[2]:
                    correct=False
            if not correct:
                fbwrong.append(str(fbedges.index(coord)+1))
                
        for coord in udedges:
            edge=s.get_piece(coord[0],coord[1],coord[2])
            correct=True
            if edge.pos.x==1:
                if edge.colors[0]!=s.get_piece(1,0,0).colors[0]:
                    correct=False
            elif edge.pos.x==-1:
                if edge.colors[0]!=s.get_piece(-1,0,0).colors[0]:
                    correct=False
            if edge.pos.y==1:
                if edge.colors[1]!=s.get_piece(0,1,0).colors[1]:
                    correct=False
            elif edge.pos.y==-1:
                if edge.colors[1]!=s.get_piece(0,-1,0).colors[1]:
                    correct=False
            if edge.pos.z==1:
                if edge.colors[2]!=s.get_piece(0,0,1).colors[2]:
                    correct=False
            elif edge.pos.z==-1:
                if edge.colors[2]!=s.get_piece(0,0,-1).colors[2]:
                    correct=False
            if not correct:
                udwrong.append(str(udedges.index(coord)+1))
                
        for coord in lredges:
            edge=s.get_piece(coord[0],coord[1],coord[2])
            correct=True
            if edge.pos.x==1:
                if edge.colors[0]!=s.get_piece(1,0,0).colors[0]:
                    correct=False
            elif edge.pos.x==-1:
                if edge.colors[0]!=s.get_piece(-1,0,0).colors[0]:
                    correct=False
            if edge.pos.y==1:
                if edge.colors[1]!=s.get_piece(0,1,0).colors[1]:
                    correct=False
            elif edge.pos.y==-1:
                if edge.colors[1]!=s.get_piece(0,-1,0).colors[1]:
                    correct=False
            if edge.pos.z==1:
                if edge.colors[2]!=s.get_piece(0,0,1).colors[2]:
                    correct=False
            elif edge.pos.z==-1:
                if edge.colors[2]!=s.get_piece(0,0,-1).colors[2]:
                    correct=False
            if not correct:
                lrwrong.append(str(lredges.index(coord)+1))
        
        #print(fbwrong,udwrong,lrwrong)
        
        for i in range(len(fbs)):
            if fbwrong==fbs[i]:
                if udwrong==uds[i]:
                    if lrwrong==lrs[i]:
                        #print("found:",fbs[i],uds[i],lrs[i])
                        new=copy.deepcopy(s)
                        new.sequence((" ").join(([translation[int(z)-1] for z in solutions[i].split(" ")])))
                        if new.is_solved():
                            #print(symetries.index(s))
                            return [movemappings3[symetries.index(s)][G3moves.index(j)] for j in ([translation[int(z)-1] for z in solutions[i].split(" ")])]
                        
                        new=copy.deepcopy(s)
                        new.sequence((" ").join(reversed([translation[int(z)-1] for z in solutions[i].split(" ")])))
                        if new.is_solved():
                            #print(symetries.index(s))
                            return [movemappings3[symetries.index(s)][G3moves.index(j)] for j in reversed([translation[int(z)-1] for z in solutions[i].split(" ")])]
                        

    return []




def solve_a_cube():
    try:
        sample=[random.choice(moves) for i in range(25)]
        
        print("Cube Shuffle:",(" ").join(sample))
        
        c.sequence((" ").join(sample))
        solution=[]
                 
        s=Stage1(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 1 Solution: ",(" ").join(s))
        
        s=Stage2(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 2 Solution: ",(" ").join(s))
        
        s=Stage3(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 3 Solution: ",(" ").join(s))
        
        s=Stage4(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 4 Solution: ",(" ").join(s))
        
        s=Stage5(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 5 Solution: ",(" ").join(s))
        
        s=Stage6(c)
        c.sequence((" ").join(s))
        solution+=s
        print("Stage 6 Solution: ",(" ").join(s))
        
        
        if c.is_solved():
            print("Correct Solution")
            print("Moves:",len(solution))
        else:
            print("Invalid Solution")
        print("Complete Solution: ",(" ").join(solution))
        
    except:
        print("FOUND AN ERROR")
    



solve_a_cube()
    



