import random
import networkx as nx
import networkx.algorithms.community as nxcom
 

kMax = 3
community1 = []
community2 = []
community3 = []
communityArray = [[],[],[]]
requiredModularity = 0.5
tabuArray = []

G = nx.read_edgelist('karate_edge_list.txt')
numberOfNodes = nx.number_of_nodes(G)

def generateInitialSolution(communityArr):
    for n in G:
        community1.append(n)
    
    for a in range(int(numberOfNodes/3)):
        community2.append(community1[a])
        community1.remove(community1[a])

    for a in range(int(numberOfNodes/3)):
        community3.append(community1[a])
        community1.remove(community1[a])

    communityArr[0] = community1
    communityArr[1] = community2  
    communityArr[2] = community3  
    print("Initial Solution: "+str(communityArr))
    return communityArr

def calculateModularity(communities):
    modularity = nxcom.modularity(G, communities)
    return modularity

def changeCommunity(currentSolutionArr, oldCommunityIndex, oldNodeIndex):
    print("CHANGECOMMUNITY")
    newCommunityIndex = random.randint(0,2) #community seçilir
    while(newCommunityIndex == oldCommunityIndex):
        newCommunityIndex = random.randint(0, 2)

    newNodeIndex = random.randint(0, (len(currentSolutionArr[newCommunityIndex])-1))
    print("Selected node: "+str(currentSolutionArr[newCommunityIndex][newNodeIndex]))
    
    node1= currentSolutionArr[oldCommunityIndex][oldNodeIndex]
    node2 = currentSolutionArr[newCommunityIndex][newNodeIndex]
    currentSolutionArr[oldCommunityIndex].remove(node1) 
    currentSolutionArr[newCommunityIndex].remove(node2) 
    currentSolutionArr[newCommunityIndex].append(node1) 
    currentSolutionArr[oldCommunityIndex].append(node2)      
    
    print(currentSolutionArr)
    return currentSolutionArr    

def shake(currentSolutionArr, k):
    print("SHAKE")
    
    for x in range(k):
        print("Shake iteration: " +str(x+1))
        communityIndex = random.randint(0,2) #community seçilir
        arraySize = len(currentSolutionArr[communityIndex])
        nodeIndex = random.randint(0,arraySize-1) #community içinden bir node seçilir
        while(currentSolutionArr[communityIndex][nodeIndex] in tabuArray):
            nodeIndex = random.randint(0,arraySize-1)
        print("Selected node: "+str(currentSolutionArr[communityIndex][nodeIndex]))   
        currentSolutionArr = changeCommunity(currentSolutionArr, communityIndex, nodeIndex)
        tabuArray.append(currentSolutionArr[communityIndex][nodeIndex])
    return currentSolutionArr        
            

def localSearch(shakeSolutionArr):
    pass


def vns():
    
    print(nx.nodes(G))
    currentSolution = generateInitialSolution(communityArray)
    modularity = calculateModularity(currentSolution)
    for x in range(3):
    #while(modularity <= requiredModularity): #Stop condition
        k = 1
        while(k <= kMax):
            print("Main iteration: "+str(k))
            shakeSolution = shake(currentSolution, k)
            #newSolution = localSearch(shakeSolution)
            newSolution = shakeSolution
            if(calculateModularity(newSolution) > calculateModularity(currentSolution)):
                currentSolution = newSolution
                k = 1
            else:
                k = k+1

            modularity = calculateModularity(currentSolution) 
            print("Current solution: "+ str(currentSolution))
            print("Modularity: "+str(modularity))   

           
    

if __name__== "__main__":
  vns()
