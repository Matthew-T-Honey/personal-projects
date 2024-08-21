import tkinter
from functools import partial
import copy
import random

window=tkinter.Tk()
window.title("Chess")
window.geometry("500x500")
window.configure(background="white")

waiting_for_piece=True
letters=["a","b","c","d","e","f","g","h"]
board=[[["♖",1],["♘",1],["♗",1],["♕",1],["♔",1],["♗",1],["♘",1],["♖",1]],[["♙",1],["♙",1],["♙",1],["♙",1],["♙",1],["♙",1],["♙",1],["♙",1]],[[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[]],[["♟",2],["♟",2],["♟",2],["♟",2],["♟",2],["♟",2],["♟",2],["♟",2]],[["♜",2],["♞",2],["♝",2],["♛",2],["♚",2],["♝",2],["♞",2],["♜",2]]]

turn=1
moved=[[0,0,0],[0,0,0]]

def value(v):
    if v!=[]:
        if v[0]=="♙" or v[0]=="♟":
            return 1
        elif v[0]=="♖" or v[0]=="♜" or v=="Rook":
            return 5
        elif v[0]=="♘" or v[0]=="♞" or v=="Knight":
            return 3
        elif v[0]=="♗" or v[0]=="♝" or v=="Bishop":
            return 3
        elif v[0]=="♕" or v[0]=="♛" or v=="Queen":
            return 9
        elif v[0]=="♔" or v[0]=="♚":
            return 100
        else:
            return 0
    else:
        return 0
            
    
def check(bo,tt):
    #if tt=1: check for white check
    for c in range(8):
        for d in range(8):
            if bo[c][d]!=[]:
                if bo[c][d][0]=="♔" and tt==1:
                    king=[c,d]
                elif bo[c][d][0]=="♚" and tt==2:
                    king=[c,d]
    for c in range(8):
        for d in range(8):
            if bo[c][d]!=[]:
                if bo[c][d][1]!=tt:
                    predicting=0
                    if tt==1 and turn==1:
                        predicting=2
                    elif tt==2 and turn==0:
                        predicting=1
                    
                    checkmove=checkmoves(c,d,bo,predicting,1)
                    for e in range(len(checkmove)):
                        
                        if checkmove[e][0]==king[0] and checkmove[e][1]==king[1]:
                            return "Check"
                            

        
    
    

    
def checkmoves(y,x,b,pred,che):
    global turn
    #turn=1: White turn
    #turn=2: Black turn
    #pred=1: Predicting for White
    #pred=2: Predicting for Black
    #p=1: White
    #p=2: Black
    piece=b[y][x]
    moves=[]
    if pred==1:
        p=1
        p2=2
    elif pred==2:
        p=2
        p2=1
    elif turn==1:
        p=1
        p2=2
    else:
        p=2
        p2=1
    if piece!=[]:
        if b[y][x][1]==p:
            if piece[0]=="♙" or piece[0]=="♟":
                if p==1:
                    if b[y+1][x]==[]:
                        if y!=6:
                            moves.append([y+1,x])
                            if y==1:
                                if b[y+2][x]==[]:
                                    moves.append([y+2,x])
                        else:
                            moves.append([y+1,x,"Rook"])
                            moves.append([y+1,x,"Knight"])
                            moves.append([y+1,x,"Bishop"])
                            moves.append([y+1,x,"Queen"])
                            
                    if x!=0:
                        if b[y+1][x-1]!=[]:
                            if b[y+1][x-1][1]==p2:
                                if y==6:
                                    moves.append([y+1,x-1,"Rook"])
                                    moves.append([y+1,x-1,"Knight"])
                                    moves.append([y+1,x-1,"Bishop"])
                                    moves.append([y+1,x-1,"Queen"])
                                else:
                                    moves.append([y+1,x-1])
                    if x!=7:
                        if b[y+1][x+1]!=[]:
                            if b[y+1][x+1][1]==p2:
                                if y==6:
                                    moves.append([y+1,x+1,"Rook"])
                                    moves.append([y+1,x+1,"Knight"])
                                    moves.append([y+1,x+1,"Bishop"])
                                    moves.append([y+1,x+1,"Queen"])
                                else:
                                    moves.append([y+1,x+1])
                elif p==2:
                    if b[y-1][x]==[]:
                        if y!=1:
                            moves.append([y-1,x])
                            if y==1:
                                if b[y-2][x]==[]:
                                    moves.append([y-2,x])
                        else:
                            moves.append([y-1,x,"Rook"])
                            moves.append([y-1,x,"Knight"])
                            moves.append([y-1,x,"Bishop"])
                            moves.append([y-1,x,"Queen"])
                            
                    if x!=0:
                        if b[y-1][x-1]!=[]:
                            if b[y-1][x-1][1]==p2:
                                if y==1:
                                    moves.append([y-1,x-1,"Rook"])
                                    moves.append([y-1,x-1,"Knight"])
                                    moves.append([y-1,x-1,"Bishop"])
                                    moves.append([y-1,x-1,"Queen"])
                                else:
                                    moves.append([y-1,x-1])
                    if x!=7:
                        if b[y-1][x+1]!=[]:
                            if b[y-1][x+1][1]==p2:
                                if y==1:
                                    moves.append([y-1,x+1,"Rook"])
                                    moves.append([y-1,x+1,"Knight"])
                                    moves.append([y-1,x+1,"Bishop"])
                                    moves.append([y-1,x+1,"Queen"])
                                else:
                                    moves.append([y-1,x+1])
            elif piece[0]=="♖" or piece[0]=="♜":
                done=0
                m=1
                while done==0:
                    if y-m==-1:
                        done=1
                    elif b[y-m][x]==[]:
                        moves.append([y-m,x])
                        m+=1
                    elif b[y-m][x][1]==p2:
                        moves.append([y-m,x])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if y+m==8:
                        done=1
                    elif b[y+m][x]==[]:
                        moves.append([y+m,x])
                        m+=1
                    elif b[y+m][x][1]==p2:
                        moves.append([y+m,x])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if x+m==8:
                        done=1
                    elif b[y][x+m]==[]:
                        moves.append([y,x+m])
                        m+=1
                    elif b[y][x+m][1]==p2:
                        moves.append([y,x+m])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if x-m==-1:
                        done=1
                    elif b[y][x-m]==[]:
                        moves.append([y,x-m])
                        m+=1
                    elif b[y][x-m][1]==p2:
                        moves.append([y,x-m])
                        done=1
                    else:
                        done=1   
            elif piece[0]=="♘" or piece[0]=="♞":
                
                if y>=2:
                    if x>=1:
                        if b[y-2][x-1]==[]:
                            moves.append([y-2,x-1])
                        elif b[y-2][x-1][1]==p2:
                            moves.append([y-2,x-1])
                    if x<=6:
                        if b[y-2][x+1]==[]:
                            moves.append([y-2,x+1])
                        elif b[y-2][x+1][1]==p2:
                            moves.append([y-2,x+1])
                if y>=1:
                    if x>=2:
                        if b[y-1][x-2]==[]:
                            moves.append([y-1,x-2])
                        elif b[y-1][x-2][1]==p2:
                            moves.append([y-1,x-2])
                        
                    if x<=5:
                        if b[y-1][x+2]==[]:
                            moves.append([y-1,x+2])
                        elif b[y-1][x+2][1]==p2:
                            moves.append([y-1,x+2])
                            
                if y<=5:
                    if x>=1:
                        if b[y+2][x-1]==[]:
                            moves.append([y+2,x-1])
                        elif b[y+2][x-1][1]==p2:
                            moves.append([y+2,x-1])
                    if x<=6 :   
                        if b[y+2][x+1]==[]:
                            moves.append([y+2,x+1])
                        elif b[y+2][x+1][1]==p2:
                            moves.append([y+2,x+1])
                            
                if y<=6:
                    if x>=2:
                        if b[y+1][x-2]==[]:
                            moves.append([y+1,x-2])
                        elif b[y+1][x-2][1]==p2:
                            moves.append([y+1,x-2])
                    if x<=5:
                        if b[y+1][x+2]==[]:
                            moves.append([y+1,x+2])
                        elif b[y+1][x+2][1]==p2:
                            moves.append([y+1,x+2])
                            
            elif piece[0]=="♗" or piece[0]=="♝":
                done=0
                m=1
                m2=1
                while done==0:
                    if y-m==-1 or x-m2==-1:
                        done=1
                    elif b[y-m][x-m2]==[]:
                        moves.append([y-m,x-m2])
                        m+=1
                        m2+=1
                    elif b[y-m][x-m2][1]==p2:
                        moves.append([y-m,x-m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y-m==-1 or x+m2==8:
                        done=1
                    elif b[y-m][x+m2]==[]:
                        moves.append([y-m,x+m2])
                        m+=1
                        m2+=1
                    elif b[y-m][x+m2][1]==p2:
                        moves.append([y-m,x+m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y+m==8 or x-m2==-1:
                        done=1
                    elif b[y+m][x-m2]==[]:
                        moves.append([y+m,x-m2])
                        m+=1
                        m2+=1
                    elif b[y+m][x-m2][1]==p2:
                        moves.append([y+m,x-m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y+m==8 or x+m2==8:
                        done=1
                    elif b[y+m][x+m2]==[]:
                        moves.append([y+m,x+m2])
                        m+=1
                        m2+=1
                    elif b[y+m][x+m2][1]==p2:
                        moves.append([y+m,x+m2])
                        done=1
                    else:
                        done=1
            elif piece[0]=="♕" or piece[0]=="♛":
                done=0
                m=1
                m2=1
                while done==0:
                    if y-m==-1 or x-m2==-1:
                        done=1
                    elif b[y-m][x-m2]==[]:
                        moves.append([y-m,x-m2])
                        m+=1
                        m2+=1
                    elif b[y-m][x-m2][1]==p2:
                        moves.append([y-m,x-m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y-m==-1 or x+m2==8:
                        done=1
                    elif b[y-m][x+m2]==[]:
                        moves.append([y-m,x+m2])
                        m+=1
                        m2+=1
                    elif b[y-m][x+m2][1]==p2:
                        moves.append([y-m,x+m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y+m==8 or x-m2==-1:
                        done=1
                    elif b[y+m][x-m2]==[]:
                        moves.append([y+m,x-m2])
                        m+=1
                        m2+=1
                    elif b[y+m][x-m2][1]==p2:
                        moves.append([y+m,x-m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                m2=1
                while done==0:
                    if y+m==8 or x+m2==8:
                        done=1
                    elif b[y+m][x+m2]==[]:
                        moves.append([y+m,x+m2])
                        m+=1
                        m2+=1
                    elif b[y+m][x+m2][1]==p2:
                        moves.append([y+m,x+m2])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if y-m==-1:
                        done=1
                    elif b[y-m][x]==[]:
                        moves.append([y-m,x])
                        m+=1
                    elif b[y-m][x][1]==p2:
                        moves.append([y-m,x])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if y+m==8:
                        done=1
                    elif b[y+m][x]==[]:
                        moves.append([y+m,x])
                        m+=1
                    elif b[y+m][x][1]==p2:
                        moves.append([y+m,x])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if x+m==8:
                        done=1
                    elif b[y][x+m]==[]:
                        moves.append([y,x+m])
                        m+=1
                    elif b[y][x+m][1]==p2:
                        moves.append([y,x+m])
                        done=1
                    else:
                        done=1
                done=0
                m=1
                while done==0:
                    if x-m==-1:
                        done=1
                    elif b[y][x-m]==[]:
                        moves.append([y,x-m])
                        m+=1
                    elif b[y][x-m][1]==p2:
                        moves.append([y,x-m])
                        done=1
                    else:
                        done=1 
            elif piece[0]=="♔" or piece[0]=="♚":
                if x>=1:
                    if b[y][x-1]==[]:
                        moves.append([y,x-1])
                    elif b[y][x-1][1]==p2:
                        moves.append([y,x-1])
                    if y>=1:
                        if b[y-1][x-1]==[]:
                            moves.append([y-1,x-1])
                        elif b[y-1][x-1][1]==p2:
                            moves.append([y-1,x-1])
                    if y<=6:
                        if b[y+1][x-1]==[]:
                            moves.append([y+1,x-1])
                        elif b[y+1][x-1][1]==p2:
                            moves.append([y+1,x-1])
                if x<=6:
                    if b[y][x+1]==[]:
                        moves.append([y,x+1])
                    elif b[y][x+1][1]==p2:
                        moves.append([y,x+1])
                    if y>=1:
                        if b[y-1][x+1]==[]:
                            moves.append([y-1,x+1])
                        elif b[y-1][x+1][1]==p2:
                            moves.append([y-1,x+1])
                    if y<=6:
                        if b[y+1][x+1]==[]:
                            moves.append([y+1,x+1])
                        elif b[y+1][x+1][1]==p2:
                            moves.append([y+1,x+1])
                if y>=1:
                    if b[y-1][x]==[]:
                        moves.append([y-1,x])
                    elif b[y-1][x][1]==p2:
                        moves.append([y-1,x])
                if y<=6:
                    if b[y+1][x]==[]:
                        moves.append([y+1,x])
                    elif b[y+1][x][1]==p2:
                        moves.append([y+1,x])
                        
                        
                        
                if piece[0]=="♔":
                    if y==0 and x==4:
                        if moved[0][2]==0:
                            if b[0][0]==["♖",1]:
                                if b[0][1]==[] and b[0][2]==[] and b[0][3]==[]:
                                    if moved[0][0]==0:
                                        moves.append([0,2,"Castle"])
                                
                            if b[0][7]==["♖",1]:
                                if b[0][6]==[] and b[0][5]==[]:
                                    if moved[0][1]==0:
                                        moves.append([0,6,"Castle"])
                if piece[0]=="♚":
                    if y==7 and x==4:
                        if moved[1][2]==0:
                            if b[7][0]==["♜",2]:
                                if b[7][1]==[] and b[7][2]==[] and b[7][3]==[]:
                                    if moved[1][0]==0:
                                        moves.append([7,2,"Castle"])
                                
                            if b[7][7]==["♜",2]:
                                if b[7][6]==[] and b[7][5]==[]:
                                    if moved[1][1]==0:
                                        moves.append([7,6,"Castle"])
                                
    if che==0:
        removemoves=[]
        for m in range(len(moves)):
            b2=copy.deepcopy(b)
            if p==2:
                if len(moves[m])==3:
                    if moves[m][2]=="Castle":
                        if moves[m][1]==6:
                            movepiece=b2[7][7]
                            b2[7][7]=[]
                            b2[7][5]=movepiece
                        elif moves[m][1]==2:
                            movepiece=b2[7][0]
                            b2[7][0]=[]
                            b2[7][1]=movepiece
                    elif moves[m][2]=="Rook":
                        b2[1][x]==["♜",2]
                    elif moves[m][2]=="Knight":
                        b2[1][x]==["♞",2]
                    elif moves[m][2]=="Bishop":
                        b2[1][x]==["♝",2]
                    elif moves[m][2]=="Queen":
                        b2[1][x]==["♛",2]
    
                movepiece=b2[y][x]
                b2[y][x]=[]
                b2[moves[m][0]][moves[m][1]]=movepiece
            elif p==1:
                if len(moves[m])==3:
                    if moves[m][2]=="Castle":
                        if moves[m][1]==6:
                            movepiece=b2[0][7]
                            b2[0][7]=[]
                            b2[0][5]=movepiece
                        elif moves[m][1]==2:
                            movepiece=b2[0][0]
                            b2[0][0]=[]
                            b2[0][3]=movepiece
                    elif moves[m][2]=="Rook":
                        b2[6][x]==["♖",1]
                    elif moves[m][2]=="Knight":
                        b2[6][x]==["♘",1]
                    elif moves[m][2]=="Bishop":
                        b2[6][x]==["♗",1]
                    elif moves[m][2]=="Queen":
                        b2[6][x]==["♕",1]
    
                movepiece=b2[y][x]
                b2[y][x]=[]
                b2[moves[m][0]][moves[m][1]]=movepiece
                
            if check(b2,p)=="Check":
                removemoves.append(moves[m])
        for n in range(len(removemoves)):
            moves.remove(removemoves[n])
            
    return moves


def move(i,j):
    global waiting_for_piece, piece, turn

    if waiting_for_piece==True:
        piece=[i,j]
        waiting_for_piece=False
        buttons[7-i][j].configure(bg="red")
    else:
        waiting_for_piece=True
        if (7-piece[0]+piece[1])%2==1:
            buttons[7-piece[0]][piece[1]].configure(bg="cornsilk", fg="black")
        else:
            buttons[7-piece[0]][piece[1]].configure(bg="black", fg="white")
        #try:
        if [i,j] in checkmoves(piece[0],piece[1],board,0,0) or [i,j,"Castle"] in checkmoves(piece[0],piece[1],board,0,0) or [i,j,"Queen"] in checkmoves(piece[0],piece[1],board,0,0):

                x2=j
                y2=i
                x1=piece[1]
                y1=piece[0]

                if [y2,x2,"Castle"] in checkmoves(y1,x1,board,0,0):
                    if x2==6:
                        movepiece=board[0][7]
                        board[0][7]=[]
                        board[0][5]=movepiece
                    elif x2==2:
                        movepiece=board[0][0]
                        board[0][0]=[]
                        board[0][3]=movepiece
                elif [y2,x2,"Queen"] in checkmoves(y1,x1,board,0,0):
                    done=0
                    while done==0:
                        try:
                            pie=input("What piece would you like to exchange your pawn for:\nR:Rook\nK:Knight\nB:Bishop\nQ:Queen\n")
                            if pie.lower()=="r":
                                board[y1][x1]=["♖",1]
                                done=1
                            elif pie.lower()=="k":
                                board[y1][x1]=["♘",1]
                                done=1
                            elif pie.lower()=="b":
                                board[y1][x1]=["♗",1]
                                done=1
                            elif pie.lower()=="q":
                                board[y1][x1]=["♕",1]
                                done=1
                            else:
                                print("That input is invalid")
                        except:
                            print("That input is invalid")
                                    
                
                movepiece=board[y1][x1]
                board[y1][x1]=[]
                board[y2][x2]=movepiece
                        
                if board[0][0]!=["♖",1]:
                    moved[0][0]=1
                if board[0][7]!=["♖",1]:
                    moved[0][1]=1
                if board[0][4]!=["♔",1]:
                    moved[0][2]=1
                turn=0
        else:
                print("That move is invalid")
                
        #except:
            #print("That move is invalid!")
    for i in range(8):
        for j in range(8):
            if board[7-i][j]==[]:
                buttons[i][j].configure(text="    ")
            else:
                buttons[i][j].configure(text=board[7-i][j][0])
    
    if turn==0:
        if check(board,2)=="Check":
            checkmate=1
            for a in range(8):
                for b in range(8):
                    if board[a][b]!=[]:
                        if board[a][b][1]==2:
                            checkmove=checkmoves(a,b,board,0,0)
                            if checkmove!=[]:
                                checkmate=0    
            if checkmate==1:
                print("Black is in Checkmate!")
                ended=1
            else:
                print("Black is in Check")
                
        piecemoves=[]
        for a in range(8):
            for b in range(8):
                if board[a][b]!=[]:
                    if board[a][b][1]==2:
                        checkmove=checkmoves(a,b,board,0,0)
                        if checkmove!=[]:
                            for c in range(len(checkmove)):
                                if len(checkmove[c])==3:
                                    if checkmove[c][2] != "Castle":
                                        piecemoves.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                else:
                                    piecemoves.append([[a,b],checkmove[c],value(board[checkmove[c][0]][checkmove[c][1]])])
        
        
        for d in range(len(piecemoves)):
            predictedboard1=copy.deepcopy(board)
            
            if len(piecemoves[d][1])==3:
                if piecemoves[d][1][2]=="Castle":
                    if piecemoves[d][1][1]==6:
                        movepiece=predictedboard1[7][7]
                        predictedboard1[7][7]=[]
                        predictedboard1[7][5]=movepiece
                    elif piecemoves[d][1][1]==2:
                        movepiece=predictedboard1[7][0]
                        predictedboard1[7][0]=[]
                        predictedboard1[7][3]=movepiece
                elif piecemoves[d][1][2]=="Rook":
                    predictedboard1[6][piecemoves[d][0][1]]==["♜",2]
                elif piecemoves[d][1][2]=="Knight":
                    predictedboard1[6][piecemoves[d][0][1]]==["♞",2]
                elif piecemoves[d][1][2]=="Bishop":
                    predictedboard1[6][piecemoves[d][0][1]]==["♝",2]
                elif piecemoves[d][1][2]=="Queen":
                    predictedboard1[6][piecemoves[d][0][1]]==["♛",2]

            movepiece=predictedboard1[piecemoves[d][0][0]][piecemoves[d][0][1]]
            predictedboard1[piecemoves[d][0][0]][piecemoves[d][0][1]]=[]
            predictedboard1[piecemoves[d][1][0]][piecemoves[d][1][1]]=movepiece
            
            predictedpiecemoves1=[]
            for a in range(8):
                for b in range(8):
                    if predictedboard1[a][b]!=[]:
                        if predictedboard1[a][b][1]==1:
                            checkmove=checkmoves(a,b,predictedboard1,1,0)
                            if checkmove!=[]:
                                for c in range(len(checkmove)):
                                    if len(checkmove[c])==3:
                                        if checkmove[c][2] != "Castle":
                                            predictedpiecemoves1.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                    else:
                                        predictedpiecemoves1.append([[a,b],checkmove[c],value(predictedboard1[checkmove[c][0]][checkmove[c][1]])])
                
            for e in range(len(predictedpiecemoves1)):
                predictedboard2=copy.deepcopy(predictedboard1)
                
                if len(predictedpiecemoves1[e][1])==3:
                    if predictedpiecemoves1[e][1][2]=="Castle":
                        if predictedpiecemoves1[e][1][1]==6:
                            movepiece=predictedboard2[0][7]
                            predictedboard2[0][7]=[]
                            predictedboard2[0][5]=movepiece
                        elif predictedpiecemoves1[e][1][1]==2:
                            movepiece=predictedboard2[0][0]
                            predictedboard2[0][0]=[]
                            predictedboard2[0][3]=movepiece
                    elif predictedpiecemoves1[e][1][2]=="Rook":
                        predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♜",2]
                    elif predictedpiecemoves1[e][1][2]=="Knight":
                        predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♞",2]
                    elif predictedpiecemoves1[e][1][2]=="Bishop":
                        predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♝",2]
                    elif predictedpiecemoves1[e][1][2]=="Queen":
                        predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♛",2]
    
                movepiece=predictedboard2[predictedpiecemoves1[e][0][0]][predictedpiecemoves1[e][0][1]]
                predictedboard2[predictedpiecemoves1[e][0][0]][predictedpiecemoves1[e][0][1]]=[]
                predictedboard2[predictedpiecemoves1[e][1][0]][predictedpiecemoves1[e][1][1]]=movepiece
                
                predictedpiecemoves2=[]
                for a in range(8):
                    for b in range(8):
                        if predictedboard2[a][b]!=[]:
                            if predictedboard2[a][b][1]==2:
                                checkmove=checkmoves(a,b,predictedboard2,0,0)
                                if checkmove!=[]:
                                    for c in range(len(checkmove)):
                                        if len(checkmove[c])==3:
                                            if checkmove[c][2] != "Castle":
                                                predictedpiecemoves2.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                        else:
                                            predictedpiecemoves2.append([[a,b],checkmove[c],value(predictedboard2[checkmove[c][0]][checkmove[c][1]])])

                highestscore=-2000
                for a in range(len(predictedpiecemoves2)):
                    if predictedpiecemoves2[a][2]>highestscore:
                        highestscore=predictedpiecemoves2[a][2]
                predictedpiecemoves1[e][2]-=highestscore

            highestscore=-3000
            for a in range(len(predictedpiecemoves1)):
                if predictedpiecemoves1[a][2]>highestscore:
                    highestscore=predictedpiecemoves1[a][2]
            piecemoves[d][2]-=highestscore
            
            
        goodmoves=[]
        lowest=-4000
        for a in range(len(piecemoves)):
            if piecemoves[a][2]>lowest:
                goodmoves.append(piecemoves[a])
            if len(goodmoves)>5:
                minimum = [goodmoves[0]]
                for item in goodmoves:
                    if item[2] < minimum[0][2]:
                        minimum = [item]
                    if item[2] == minimum[0][2] and item != minimum[0]:
                        minimum.append(item)
                if len(minimum)!=len(goodmoves):
                    lowest=minimum[0][2]
                    for b in range(len(minimum)):
                        if minimum[b] in goodmoves:
                            goodmoves.remove(minimum[b])
        
        if len(goodmoves)<6 and len(goodmoves)>1:
            print("EXTRA")
            for a in range(len(goodmoves)):
                piecemoves.remove(goodmoves[a])
                goodmoves[a]=[goodmoves[a][0],goodmoves[a][1],0]
                
            for d in range(len(goodmoves)):
                predictedboard1=copy.deepcopy(board)
                
                if len(goodmoves[d][1])==3:
                    if goodmoves[d][1][2]=="Castle":
                        if goodmoves[d][1][1]==6:
                            movepiece=predictedboard1[7][7]
                            predictedboard1[7][7]=[]
                            predictedboard1[7][5]=movepiece
                        elif goodmoves[d][1][1]==2:
                            movepiece=predictedboard1[7][0]
                            predictedboard1[7][0]=[]
                            predictedboard1[7][3]=movepiece
                    elif goodmoves[d][1][2]=="Rook":
                        predictedboard1[6][goodmoves[d][0][1]]==["♜",2]
                    elif goodmoves[d][1][2]=="Knight":
                        predictedboard1[6][goodmoves[d][0][1]]==["♞",2]
                    elif goodmoves[d][1][2]=="Bishop":
                        predictedboard1[6][goodmoves[d][0][1]]==["♝",2]
                    elif goodmoves[d][1][2]=="Queen":
                        predictedboard1[6][goodmoves[d][0][1]]==["♛",2]
    
                movepiece=predictedboard1[goodmoves[d][0][0]][goodmoves[d][0][1]]
                predictedboard1[goodmoves[d][0][0]][goodmoves[d][0][1]]=[]
                predictedboard1[goodmoves[d][1][0]][goodmoves[d][1][1]]=movepiece
                
                predictedpiecemoves1=[]
                for a in range(8):
                    for b in range(8):
                        if predictedboard1[a][b]!=[]:
                            if predictedboard1[a][b][1]==1:
                                checkmove=checkmoves(a,b,predictedboard1,1,0)
                                if checkmove!=[]:
                                    for c in range(len(checkmove)):
                                        if len(checkmove[c])==3:
                                            if checkmove[c][2] != "Castle":
                                                predictedpiecemoves1.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                        else:
                                            predictedpiecemoves1.append([[a,b],checkmove[c],value(predictedboard1[checkmove[c][0]][checkmove[c][1]])])
                    
                for e in range(len(predictedpiecemoves1)):
                    predictedboard2=copy.deepcopy(predictedboard1)
                    
                    if len(predictedpiecemoves1[e][1])==3:
                        if predictedpiecemoves1[e][1][2]=="Castle":
                            if predictedpiecemoves1[e][1][1]==6:
                                movepiece=predictedboard2[0][7]
                                predictedboard2[0][7]=[]
                                predictedboard2[0][5]=movepiece
                            elif predictedpiecemoves1[e][1][1]==2:
                                movepiece=predictedboard2[0][0]
                                predictedboard2[0][0]=[]
                                predictedboard2[0][3]=movepiece
                        elif predictedpiecemoves1[e][1][2]=="Rook":
                            predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♜",2]
                        elif predictedpiecemoves1[e][1][2]=="Knight":
                            predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♞",2]
                        elif predictedpiecemoves1[e][1][2]=="Bishop":
                            predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♝",2]
                        elif predictedpiecemoves1[e][1][2]=="Queen":
                            predictedboard2[6][predictedpiecemoves1[e][0][1]]==["♛",2]
        
                    movepiece=predictedboard2[predictedpiecemoves1[e][0][0]][predictedpiecemoves1[e][0][1]]
                    predictedboard2[predictedpiecemoves1[e][0][0]][predictedpiecemoves1[e][0][1]]=[]
                    predictedboard2[predictedpiecemoves1[e][1][0]][predictedpiecemoves1[e][1][1]]=movepiece
                    
                    predictedpiecemoves2=[]
                    for a in range(8):
                        for b in range(8):
                            if predictedboard2[a][b]!=[]:
                                if predictedboard2[a][b][1]==2:
                                    checkmove=checkmoves(a,b,predictedboard2,0,0)
                                    if checkmove!=[]:
                                        for c in range(len(checkmove)):
                                            if len(checkmove[c])==3:
                                                if checkmove[c][2] != "Castle":
                                                    predictedpiecemoves2.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                            else:
                                                predictedpiecemoves2.append([[a,b],checkmove[c],value(predictedboard2[checkmove[c][0]][checkmove[c][1]])])
                        
                    for f in range(len(predictedpiecemoves2)):
                        predictedboard3=copy.deepcopy(predictedboard2)
                        
                        if len(predictedpiecemoves2[f][1])==3:
                            if predictedpiecemoves2[f][1][2]=="Castle":
                                if predictedpiecemoves2[f][1][1]==6:
                                    movepiece=predictedboard3[7][7]
                                    predictedboard3[7][7]=[]
                                    predictedboard3[7][5]=movepiece
                                elif predictedpiecemoves2[f][1][1]==2:
                                    movepiece=predictedboard3[7][0]
                                    predictedboard3[7][0]=[]
                                    predictedboard3[7][3]=movepiece
                                    
                            elif predictedpiecemoves2[f][1][2]=="Rook":
                                predictedboard3[6][predictedpiecemoves2[f][0][1]]==["♜",2]
                            elif predictedpiecemoves2[f][1][2]=="Knight":
                                predictedboard3[6][predictedpiecemoves2[f][0][1]]==["♞",2]
                            elif predictedpiecemoves2[f][1][2]=="Bishop":
                                predictedboard3[6][predictedpiecemoves2[f][0][1]]==["♝",2]
                            elif predictedpiecemoves2[f][1][2]=="Queen":
                                predictedboard3[6][predictedpiecemoves2[f][0][1]]==["♛",2]
                        
                        movepiece=predictedboard3[predictedpiecemoves2[f][0][0]][predictedpiecemoves2[f][0][1]]
                        predictedboard3[predictedpiecemoves2[f][0][0]][predictedpiecemoves2[f][0][1]]=[]
                        predictedboard3[predictedpiecemoves2[f][1][0]][predictedpiecemoves2[f][1][1]]=movepiece
                        
                        predictedpiecemoves3=[]
                        for a in range(8):
                            for b in range(8):
                                if predictedboard3[a][b]!=[]:
                                    if predictedboard3[a][b][1]==1:
                                        checkmove=checkmoves(a,b,predictedboard3,1,0)
                                        if checkmove!=[]:
                                            for c in range(len(checkmove)):
                                                if len(checkmove[c])==3:
                                                    if checkmove[c][2] != "Castle":
                                                        predictedpiecemoves3.append([[a,b],checkmove[c],int(value(checkmove[c][2]))-1])
                                                else:
                                                    predictedpiecemoves3.append([[a,b],checkmove[c],value(predictedboard3[checkmove[c][0]][checkmove[c][1]])])
                            
                        highestscore=-1000
                        for a in range(len(predictedpiecemoves3)):
                            if predictedpiecemoves3[a][2]>highestscore:
                                highestscore=predictedpiecemoves3[a][2]
                        predictedpiecemoves2[f][2]-=highestscore
                    
                    highestscore=-2000
                    for a in range(len(predictedpiecemoves2)):
                        if predictedpiecemoves2[a][2]>highestscore:
                            highestscore=predictedpiecemoves2[a][2]
                    predictedpiecemoves1[e][2]-=highestscore
    
                highestscore=-3000
                for a in range(len(predictedpiecemoves1)):
                    if predictedpiecemoves1[a][2]>highestscore:
                        highestscore=predictedpiecemoves1[a][2]
                goodmoves[d][2]-=highestscore
                
        
        bestmoves=[]
        highestscore=-4000
        for a in range(len(goodmoves)):
            if goodmoves[a][2]>highestscore:
                highestscore=goodmoves[a][2]
                bestmoves=[goodmoves[a]]
            elif goodmoves[a][2]==highestscore:
                bestmoves.append(goodmoves[a])
                    

        print("Value: "+str(highestscore))
        print("Options: "+str(len(bestmoves)))
        move=bestmoves[random.randint(1,len(bestmoves))-1]
        #print(move)
        x1=move[0][1]
        y1=move[0][0]
        x2=move[1][1]
        y2=move[1][0]
        
        
        if [y2,x2,"Castle"] in checkmoves(y1,x1,board,0,0):
            if x2==6:
                movepiece=board[7][7]
                board[7][7]=[]
                board[7][5]=movepiece
            elif x2==2:
                movepiece=board[7][0]
                board[7][0]=[]
                board[7][3]=movepiece
        elif len(move[1])==3:
            if move[1][2]=="Rook":
                board[y1][x1]=["♜",2]
            elif move[1][2]=="Knight":
                board[y1][x1]=["♞",2]
            elif move[1][2]=="Bishop":
                board[y1][x1]=["♝",2]
            elif move[1][2]=="Queen":
                board[y1][x1]=["♛",2]
                
                
        movepiece=board[y1][x1]
        board[y1][x1]=[]
        board[y2][x2]=movepiece
        
        if board[7][0]!=["♜",2]:
            moved[1][0]=1
        if board[7][7]!=["♜",2]:
            moved[1][1]=1
        if board[7][4]!=["♚",2]:
            moved[1][2]=1
        
        print(str(letters[x1].upper())+str(y1+1)+" To "+str(letters[x2].upper())+str(y2+1))
        turn=1
        for i in range(8):
            for j in range(8):
                if board[7-i][j]==[]:
                    buttons[i][j].configure(text="    ")
                else:
                    buttons[i][j].configure(text=board[7-i][j][0])
    
    
buttons=[]

for i in range(8):
    buttons.append([])
    for j in range(8):
        if board[7-i][j]==[]:
            buttons[i].append(tkinter.Button(window, text="    ", command=partial(move,7-i,j), fg="navy", font=("Helvetica", 16), bg="DodgerBlue2"))
        else:
            buttons[i].append(tkinter.Button(window, text=board[7-i][j][0], command=partial(move,7-i,j), fg="navy", font=("Helvetica", 16), bg="DodgerBlue2"))
        if (i+j)%2==1:
            buttons[i][j].configure(bg="cornsilk", fg="black")
        else:
            buttons[i][j].configure(bg="black", fg="white")
        
        buttons[i][j].grid(row=i,column=j)
        
window.mainloop()





















