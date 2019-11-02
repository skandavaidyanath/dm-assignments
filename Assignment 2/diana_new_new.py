import pickle
import numpy as np
import sys
# sys.setrecursionlimit(5000)
import random
import copy
import numpy as np
from collections import defaultdict
import math
from matplotlib import pyplot as plt
from pathlib import Path
import pickle
import weakref
from scipy.cluster.hierarchy import dendrogram

distances = None
with open('distances.pickle', 'rb') as fp:
    distances = pickle.load(fp) #310*310 matrix
    #just refer wrt to numbers 0 to 309




'''
Algo:
for each cluster till it has only one element:
    first have the whole cluster
    find the most disimilar elements and seperate them
    with remaining elements find which is it closer to then put it there
repeat for all leaves



'''
def computeDistance(str1, str2, scoring_fn=None):

	if not scoring_fn:

		MATCH_SCORE=0

		MISMATCH_PENALTY=1

		GAP_PENALTY=2

	score_mat=np.zeros([len(str1)+1, len(str2)+1])

	for i in range(len(str1)+1):

		for j in range(len(str2)+1):

			if(i==0 or j==0):

				entry=i*GAP_PENALTY + j*GAP_PENALTY

			else:

				entry=min((score_mat[i, j-1]+GAP_PENALTY), (score_mat[i-1, j]+GAP_PENALTY),

					score_mat[i-1, j-1]+(MATCH_SCORE*int(str1[i-1]==str2[j-1])+MISMATCH_PENALTY*(str1[i-1]!=str2[j-1])))

			score_mat[i, j]=entry

	score=score_mat[len(str1), len(str2)]

	return score



class Node(object):
    def __init__(self,value):
        self.list = value; #this will be the list of points in the cluster
        self.left = None
        self.right = None

    def get_value(self):
        return self.list

def most_dissimilar(cluster,distances):
    '''
    this finds the two points that have the max distance
    :param cluster: the cluster you want to split
    :return: the two points that are most dissimilar
    '''

    max_dist = 0
    point1 = None
    point2 = None

    n = len(cluster)
    for i in range(0,n):
        for j in range(i+1,n):
            if distances[cluster[i]][cluster[j]] == 0 and len(cluster) == 2:
                return cluster[i], cluster[j], 0
            if distances[cluster[i]][cluster[j]]>max_dist:
                max_dist=distances[cluster[i]][cluster[j]];
                point1 = cluster[i];
                point2 = cluster[j];

    return point1,point2,max_dist

# i is the iteration number

# random is to id the cluster
i=0
random = 0


#update the matrix when you split
def split(cluster,distances,mat):
    global random,i
    '''

    :param cluster: a list of nodes
    :return:the two cluster from this cluster
    '''
    if len(cluster) == 2:
        #when only two are there use the key of dict as Id for the cluster
        mat[i][0] = random
        random = random +1
        mat[i][1] = random
        random = random + 1
        mat[i][2] = distances[cluster[0]][cluster[1]]
        mat[i][3] = 2 # length of the merged cluster is 2 so pts is 2
        i+=1
        return [cluster[0]], [cluster[1]],distances[cluster[0]][cluster[1]]
    #if the cluster is more than 2 then
    point1,point2,dist = most_dissimilar(cluster,distances)
    #now you have the most dissimilar points now split the cluster based on these two distances
    # print(point1)
    # print(point2)
    left = []
    right = []
    for point in cluster:
        if distances[point1][point]>distances[point2][point]: # if point is closer to point 1
            right.append(point)
        else:
            left.append(point)

    #update the matrix here with IDs for the cluster
    # cluster(first param is the parent) left and right are the children

    mat[i][0] = random # assign unique id for both cluster
    random+=1
    mat[i][1] = random
    random+=1
    mat[i][2] = dist#the distance found by the most_dissimilar function
    mat[i][3] = len(cluster)#length of cluster before splitting
    i+=1
    return left,right,dist

# pass the matrix when splitting
def solve(root,distances,mat):
   
    if len(root.get_value())<=1:# when you reach cluster with 1 element then return
        return

    left,right,dist = split(root.get_value(),distances,mat)# function that splits the root

    root.left = Node(left)# create two child nodes and split them
    root.right = Node(right)

    solve(root.left,distances,mat)
    solve(root.right,distances,mat)

#normal DFS for verification
def traverse(root):
    #prints all the leaves rooted at root
    if root==None:
        return
    if root.right == None and root.left == None:
        print(root.get_value())

        return
    traverse(root.left)

    traverse(root.right)

def displayDendogram(mergemat, markers):    #to display the dendogram with the help of the merge matrix
    dendrogram(mergemat, labels = markers)
    fig1 = plt.gcf()
    fig1.set_size_inches(18.5, 10.5)
    plt.show()
    fig1.savefig("Complete.png", dpi =100)

def main():
    #get the data in dict


    # data = {}
    # with open('data.pickle', 'rb') as fp:
    #     data = pickle.load(fp)

    init = list(range(0,310))
    merge_matrix = np.zeros((310, 4)) #init the linkage matrix

    root = Node(init)# define a root node
    #recursive function to split left and right till only one element is there in the cluster
    solve(root,distances,merge_matrix)#to limit the depth of recursion tree will go since two sequnces are the same

    #verification part
    traverse(root)

    displayDendogram(merge_matrix, init)





if __name__ == '__main__':
    main()
