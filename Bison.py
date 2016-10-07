#!/usr/bin/env python

#Question I will be answering for the Cellular automata project: How long before the grass runs out in the field? When the grass has run out the bison need to be moved to a new field. 

#imported all libraries below, also used the as to label the libary as a shorter name for faster recall
import copy
import random as rnd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np


#List of functions

#function eat (Bison eating grass in the field, they eat 2 unit per loop per bison)

#the bison eat food from every square around them
#if there is no food in the square then it doesn't eat from that square

def eat_conditions(food_square, amount_to_eat):
    """
    Eat 2 from the square, if there's not 2 there, eat it all!!!
    """
    if food_square > amount_to_eat:
        food_square -= amount_to_eat
    else:
        #there's not enough for one meal so I'm going to EAT it ALL!!! 
        food_square = 0
    return food_square

def eat(bison_present, food_available,fieldsize):
    bigger_grid = np.zeros([fieldsize+2, fieldsize+2])
    #put previous array into the middle of larger one
    for i in range(1,fieldsize+1):
        for j in range(1,fieldsize+1):
            bigger_grid[i,j] = food_available[i-1,j-1]
    print(bigger_grid)
    
    #as grid is inside larger one, edge conditions don't matter
    for row in range(1, fieldsize+1):
        for column in range(1, fieldsize+1):      
            if bison_present[row-1][column-1]:
                food_available[row-1][column-1] = eat_conditions(bigger_grid[row][column], 2)
    
    return food_available
                
                
     

#defining fuction for stop_condition, time to move fields
def empty_square(food_available):
    for food_row in food_available:
        for food_quantity in food_row:
            if food_quantity == 0:
                return False 
        return True 
#defining function for grass regrowth in field
def grass_growth(food_available):
    for row in range(0, fieldsize):
        for column in range(0, fieldsize):      
            food_available[row][column]+= 1

#defining fuction for reproduction, 2 bison every 5 loops
def reproduction(bison_present, fieldsize):
    numb_bison=2*(sum(x.count(1) for x in bison_present))
    numb_calves= min(((fieldsize*fieldsize)-(numb_bison/2)), numb_bison)
    if numb_calves >0:
        for calf in range(0, numb_calves):
            add_bison(bison_present, fieldsize)
#define fuction add_bison which adds the new born calves into the bison field. They are placed randomly in the field using the rnd.rand function. The if and elif statments prevent a calf being places where there is already a bison or calf in a square. There is only ever 1 bison or calf per square in the field.
def add_bison(bison_present, fieldsize):
        xbison=rnd.randint(0, fieldsize-1)
        ybison=rnd.randint(0, fieldsize-1)
        if bison_present[xbison][ybison] == 0:
            bison_present[xbison][ybison]=1
        elif bison_present[xbison][ybison]==1:
            add_bison(bison_present, fieldsize)

def random_direction():
    direction=rnd.randint(-1,1)
    return direction

def random_adj_square(bison_present):
    (l,m)=np.shape(bison_present)
    for i in range(l):
        for j in range(m):
            if bison_present[i][j]:
                movement=[i+random_direction(), j +random_direction()]
                if movement[0]>(l-1):
                    movement[0]=movement[0]-l
                if movement[0]<0:
                    movement[0]=movement[0]+l
                if movement[1]>(m-1):
                    movement[1]=movement[1]-m
                if movement[1]<0:
                    movement[1]=movement[1]+m
                if not bison_present[movement[0]][movement[1]]:
                    bison_present[movement[0]][movement[1]]
                    bison_present[movement[0]][movement[1]]=True
                    bison_present[i][j]=False
    return bison_present

    
    


#Defining variables below
food_row = []
food_available = []
bison_row = []
bison_present = []
#add in comments of what each of the below are
x=0 #month counter
y=0 #grass growth counter
k=3 #reproduction counter
l=0 #divider for modulus
m=5 #divider for modulus
n=1 #counter
#user inputs field size which will print a square field e.g. user inputs 5 field will be 5x5 squares big 
print "How big is your field?"
fieldsize = int(raw_input ('<'))

print "fieldsize:", fieldsize

#user inputs how many bison they have in the field to begin with
print "How many bison in a field?"
number_bison = int(raw_input ('<'))

print "Bison number", number_bison

#Main body of code
#making the field full of grass. Grass starts out as 20 units per a square. 

for i in range(0, fieldsize, n):
    food_row.append(20)
for i in food_row:
    food_available.append(copy.copy(food_row))

#print food_square

#making empty space to place bison

for j in range(0, fieldsize, n):
    bison_row.append(0)
for j in range(0, fieldsize, n):
    bison_present.append(copy.copy(bison_row))

#adding in bison from the user input to the bison space which was made above
for numb in range(0, number_bison):
    add_bison(bison_present, fieldsize) 
#print bison_present


# Below sets out the bison eating, grass regrowing and bison reproducing. Each bison will eat in it's own square 2 units in 1 loop and the grass will grow back 1 unit every 3 loops. Each bison will have 2 calves every 5 cycles.


#print "Bison eat food"
while (empty_square(food_available)):
    eat(bison_present,food_available,fieldsize)
    random_adj_square(bison_present)
    x += 1
    y=(y+1)%k
    if y==2:
        grass_growth(food_available)
    l=(l+1)%m
    if l==4:
    
        reproduction(bison_present, fieldsize)
    
#shows end result of the amount of grass in each sqaure of the field and prints it to a file in the project folder
    plt.figure()
    sns.set()
    sns.heatmap(food_available, annot=True, cmap="BuGn")
    plt.title('Field of grass being eaten by the bison')
    figname="Fig_cycle_grass"+ str(x) + ".png"
    sns.plt.savefig(figname)
    if not empty_square(bison_present):
        #shows end result of the ammount of bison in the field and prints it to a file in the project folder
        plt.figure()    
        sns.set()
        sns.heatmap(bison_present, cmap="Greys")
        plt.title("Location of bison in the field")
        figname2="Fig_cycle_bison"+ str(x) + ".png"
        sns.plt.savefig(figname2)
    

#sns.plt.show()
#print x shows how many cycles (months) it has taken for the field to have any square with no grass. This shows the farmer he/she now needs to move the bison to a new field otherwise the bison in that square may die as there is no more food for it to eat.
print "number of months before field needs to be changed:"
print x





#ax = sns.heatmap(bison_square, annot=True, fmt="d") gives you data labels 
#cmap changes the colours of the heatmap


#end result is a field with any sqaure with no food. This then means the bison need to move fields. All field can be full of bison but only move them when food has run out for 1 bison. 

#tomorrow add in eating either side of the square they are in 





