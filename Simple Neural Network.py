import numpy as np
import copy
import random
import math
import matplotlib.pyplot as plt
from scipy.io import loadmat
from colorama import Fore, Style

def sig(x):
    try:
        y=1/(1+pow(math.e,-x))
    except:
        if x>0:
            y=1
        else:
            y=0
    return y

def dsig_dx(x):
    y=sig(x)*(1-sig(x))
    return y

def r(num):
    array=[]
    for i in range(num):
        array.append(random.uniform(-1,1))
    return array


def plot(nodes):
    n=copy.deepcopy(nodes)
    points=[]
    points2=[]
    for i in range(500):
        for k in range(len(n)):
            if n[k][0]=="I":
                n[k][1]=i/500
            else:
                s=0
                for l in range(len(n[k][2])):
                    s+=n[n[k][2][l]][1]*n[k][3][l]
                n[k][1]=sig(s+n[k][4][0])
            if n[k][0]=="O":
                points.append(n[k][1])
                points2.append((math.sin(i/250*math.pi)+1)/2)
    fig, ax = plt.subplots()
    ax.set_ylabel('output')
    ax.set_xlabel('itteration')
    ax.plot(points,color='red')
    ax.plot(points2,color='blue')
    plt.show()
    
def extract(x,num):
    data=[]
    inputs=[]
    for i in range(28):
        data.append(str(x['dataset'][0][0][0][0][0][0][num][i*28:28*(i+1)]).split(" "))
        
        for j in range(data[i].count('')):
            data[i].remove('')
        if data[i][0]=="[":
            data[i].pop(0)
        else:
            data[i][0]=data[i][0][1:]
        data[i][-1]=data[i][-1][:-1]
        for j in range(len(data[i])):
            data[i][j]=int(data[i][j])
            inputs.append(data[i][j]/255)

    actual=int(x['dataset'][0][0][0][0][0][1][num]) 
    return inputs, actual    
    
numberdata = loadmat('emnist-letters.mat')
    
    


z=784
a=16
b=16
c=26
d=0

nodes=[]
for i in range(z):
    nodes.append(["I",0])
for i in range(a):
    nodes.append(["P",0,[],r(z),r(1),0])
    for j in range(z):
        nodes[-1][2].append(j)
for i in range(b):
    nodes.append(["N",0,[],r(a),r(1),0])
    for j in range(z,z+a):
        nodes[-1][2].append(j)
for i in range(c):
    nodes.append(["O",0,[],r(b),r(1),i])
    for j in range(z+a,z+a+b):
        nodes[-1][2].append(j)
        
for i in range(d):
    nodes.append(["O",0,[],r(c),r(1),i])   
    for j in range(z+a+b,z+a+b+c):
        nodes[-1][2].append(j)


cost=0
costlist=[]
costsums=[]
newnodes=copy.deepcopy(nodes)
rate=1
#used=5
corrects=[]

for i in range(10000000):
    correct=0
    set1=[]
    for p in range(50):
        set1.append(p)
    set2=[]
    for p in range(5):
        set2.append([])
        for j in range(10):
            index=random.randint(0,len(set1)-1)
            set2[p].append(set1[index])
            set1.pop(index)
    for u in range(5):
        for j in range(100):
            if j%10==0:
                nodes=copy.deepcopy(newnodes)
                newnodes=copy.deepcopy(nodes)
            inputs, actual = extract(numberdata,set2[u][j%10])
            actual-=1
            results=[]
            costs=[]
            for k in range(len(nodes)):
                if nodes[k][0]=="I":
                    nodes[k][1]=inputs[k]
                else:
                    s=0
                    for l in range(len(nodes[k][2])):
                        s+=nodes[nodes[k][2][l]][1]*nodes[k][3][l]
                    nodes[k][1]=sig(s+nodes[k][4][0])
                    if nodes[k][0]=="O":
                        results.append(nodes[k][1])
                        if nodes[k][5]==actual:
                            y=1
                        else:
                            y=0
                        cost+=(nodes[k][1]-y)**2
                        costs.append((nodes[k][1]-y)**2)
            for k in range(len(nodes)):
                x=len(nodes)-k-1
                if nodes[x][0]!="I":
                    for l in range(len(nodes[x][2])):
                        dz_dw=nodes[nodes[x][2][l]][1]
                        dal_dz=nodes[x][1]*(1-nodes[x][1])
                        if nodes[x][0]=="O":
                            if nodes[x][5]==actual:
                                y=1
                            else:
                                y=0
                            dc_dal=2*(nodes[x][1]-y)
                        else:
                            dc_dal=nodes[x][5]
                        dc_dw=dz_dw*dal_dz*dc_dal
                        newnodes[x][3][l]-=dc_dw*rate
                        if nodes[x][0]!="P":
                            nodes[nodes[x][2][l]][5]=nodes[x][3][l]*dal_dz*dc_dal
                    dc_db=dal_dz*dc_dal
                    newnodes[x][4][0]-=dc_db*rate
            if (j%100)//10==9:
                if results.index(max(results))==actual:
                    correct+=1
                    print(Fore.GREEN + (" ").join([str(round(max(results),4)),str(results.index(max(results))),str(actual),str(round(sum(costs),4))]) + Style.RESET_ALL)
                else:
                    print(Fore.RED + (" ").join([str(round(max(results),4)),str(results.index(max(results))),str(actual),str(round(sum(costs),4))]) + Style.RESET_ALL)
                if j%100==99:
                    print(i,u,":",cost/10)
                    costlist.append(cost/10)
                    if u==4:
                        costsums.append(sum(costlist[-5:])/len(costlist[-5:]))
                    print() 
                    cost=0
                    
    fig, ax = plt.subplots()
    ax.set_ylabel('cost')
    ax.set_xlabel('itteration')
    ax.plot(costlist[-1000:],color='red')
    plt.show()
    fig, ax = plt.subplots()
    ax.set_ylabel('cost')
    ax.set_xlabel('itteration')
    ax.plot(costsums[-100:],color='blue')
    plt.show()
    corrects.append(correct)
    fig, ax = plt.subplots()
    ax.set_ylabel('correct')
    ax.set_xlabel('itteration')
    ax.plot(corrects[-100:],color='blue')
    plt.show()
    rate=costsums[-1]/10
    print("rate:",rate)
    
    print("correct:",correct)
    print(sum(costlist[-5:])/5,"\n")
    





