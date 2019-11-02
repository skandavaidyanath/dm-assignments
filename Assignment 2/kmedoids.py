# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 21:28:48 2019

@author: Skanda
"""

import pickle
import numpy as np
import random
import copy



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



def read_data():
    id  = 0
    data = {}
    fp = open('data.txt', 'r')
    line = fp.readline()
    sequence = ''
    while line:
        line = line.replace('\n', '')
        if line[0] == '>':
            if id == 0:
                id = id + 1
                line = fp.readline()
                line = line.replace('\n', '')
                continue
            sequence = sequence.replace('*', '')
            data[id] = sequence
            sequence = ''
            id = id + 1
            line = fp.readline()
            line = line.replace('\n', '')
        else:
            sequence+= line
            line = fp.readline()
            line = line.replace('\n', '')
    fp.close()
   # print(data)
    
    with open('data.pickle', 'wb') as fp:
        pickle.dump(data, fp)
    
    
    
def create_distance_matrix(data):
    distances = [[0 for j in range(len(data))] for i in range(len(data))]
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            distances[i][j] = computeDistance(data[i+1], data[j+1])
            distances[j][i] = distances[i][j]
        print(i+1)
    with open('distances.pickle', 'wb') as fp:
        pickle.dump(distances, fp)
        

def main():
    #read_data()
    data = {}
    with open('data.pickle', 'rb') as fp:
        data = pickle.load(fp)
    #create_distance_matrix(data)
    distances = None
    with open('distances.pickle', 'rb') as fp:
        distances = pickle.load(fp)
    k_array = [3,4,5,6,7,8,9,10,11,12]
    best_k_dict = {}
    for k in k_array:
        best_total_sse = 0
        for run in range(3):
            centroids = []
            i = 1
            while i<=k:
                candidate = random.randint(1, len(data))
                if candidate not in centroids:
                    centroids.append(candidate)
                    i = i + 1
            new_centroids = []
            print('K = ', k)
            print('Run = ',run)
            print(centroids)
            print(new_centroids)
            print('************')
            while True:
                total_sse = 0
                clusters = [[centroid] for centroid in centroids]
                for index, string in data.items():
                    if index in centroids:
                        continue
                    dissimilarities = [distances[index-1][centroids[i]-1] for i in range(k)]
                    clusters[dissimilarities.index(min(dissimilarities))].append(index)
                for cluster in clusters:
                    sum_of_squares = {}
                    for point in cluster:
                        value = 0
                        for other_point in cluster:
                            value += (distances[point-1][other_point-1])**2
                        sum_of_squares[point] = value
                    new_centroids.append(min(sum_of_squares, key=sum_of_squares.get))
                    total_sse += sum_of_squares[min(sum_of_squares, key=sum_of_squares.get)]
                print(centroids)
                print(new_centroids)
                print('************')
                if new_centroids == centroids:
                    if run == 0:
                        best_total_sse = total_sse
                        break
                    if total_sse < best_total_sse:
                        best_total_sse = total_sse
                    break
                centroids = copy.deepcopy(new_centroids)
                new_centroids = []
        best_k_dict[k] = best_total_sse
    best_k = min(best_k_dict, key=best_k_dict.get)
    print(best_k)
    with open('kmedoids.txt', 'w+') as fp:
        fp.write('Best K is ' + str(best_k))
        fp.write('\n*********************\n')
        centroids = []
        i = 1
        k = best_k
        while i<=k:
            candidate = random.randint(1, len(data))
            if candidate not in centroids:
                centroids.append(candidate)
                i = i + 1
            new_centroids = []
        while True:
                total_sse = 0
                clusters = [[centroid] for centroid in centroids]
                for index, string in data.items():
                    if index in centroids:
                        continue
                    dissimilarities = [distances[index-1][centroids[i]-1] for i in range(k)]
                    clusters[dissimilarities.index(min(dissimilarities))].append(index)
                for cluster in clusters:
                    sum_of_squares = {}
                    for point in cluster:
                        value = 0
                        for other_point in cluster:
                            value += (distances[point-1][other_point-1])**2
                        sum_of_squares[point] = value
                    new_centroids.append(min(sum_of_squares, key=sum_of_squares.get))
                    total_sse += sum_of_squares[min(sum_of_squares, key=sum_of_squares.get)]
                if new_centroids == centroids:
                    if run == 0:
                        best_total_sse = total_sse
                        break
                    if total_sse < best_total_sse:
                        best_total_sse = total_sse
                    break
                centroids = copy.deepcopy(new_centroids)
                new_centroids = []
        i = 1
        for cluster in clusters:
            fp.write('Cluster '+ str(i) + ' is ')
            fp.write('\n')
            fp.write(str(cluster))
            fp.write('\n')
            fp.write('*******************')
            fp.write('\n')
            i = i + 1
        
        
            
if __name__ == '__main__':
    main()