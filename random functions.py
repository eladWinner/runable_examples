# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import math
def Q1(arr , target ):
    n= len(arr)
    mode ="dict"
    lookup=[]
    if (target < n*round(math.log2(n))):
        mode = "arr" # depends on target size and equal it unless: ( target < N ) than O() = N
    if(mode == "arr"):
        lookup = [-1]*(target+1)
    else: #mode == dict
        lookup ={} # O() = N log(n)
    for i in range(n):
        if (arr[i] > target): # none-negative number + val{>target} != target
            continue
        filler = target-arr[i]
        if(mode == "arr"):
            if lookup[filler] !=-1:
                return (i,lookup[filler])
                lookup[arr[i]]=i
        else: #mode == dict
                get = lookup.get(filler)
                if (get != None):
                    return  ( i ,get)
                    lookup[arr[i]]=i
    return -1
def Q2(arr):
    if(len(arr)<1):
        return 0
    lowest =arr[0]
    profit =0
    for i in range(len(arr)):
        lowest=min(lowest,arr[i])
        profit=max(profit,arr[i]-lowest)
    return profit

#Q3
class node:
    def __init__(self,val ,nex=None):
        self.val = val
        self.nex = nex
    def __str__(self):
        return str(self.val)
    def print(self):
        print("printing list")
        print(str(self),end='')
        curr = self.nex
        while curr != None:
            print(","+str(curr),end='')
            curr=curr.nex
        print()
    def __len__(self):
        if self.nex==None:
            return 1
        return 1+len(self.nex)


def read_file(path):
    head =node(0)
    curr = head
    num =0
    with open(path) as f:
        while True:
            c=f.read(1)
            if not c:
                curr.nex= node(num)
                break
            if c !=',':
                if c.isnumeric():
                    num= num*10 +int(c)
            else:# c == ","
                curr.nex= node(num)
                curr=curr.nex
                num=0
    return head.nex
def get_length(nod):
    return len(nod)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	pass
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
