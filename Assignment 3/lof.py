# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:39:34 2019

@author: Skanda
"""
import pandas as pd
import numpy as np
import pickle
import copy


def build_distance_matrix(data):
    '''
    finds distance if every point to every other point and stores it away in
    a matrix data structure
    '''
    distances = [[0 for j in range(len(data))] for i in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            distances[i][j] = np.linalg.norm(np.array(data[i]) - np.array(data[j]))
        print(i+1)
    with open('distances.pickle', 'wb') as fp:
        pickle.dump(distances, fp)
 


def find_k_distances(distance_matrix, k):
    '''
    finds the k-distance of every point
    '''
    k_distances = []
    for i in range(len(distance_matrix)):
        i_distances = copy.deepcopy(distance_matrix[i])
        del i_distances[i]
        i_distances.sort()
        k_distances.append(i_distances[k-1])
    return k_distances 
        
   
    
def find_reachability(distance_matrix, k_distances):
    '''
    find the reachability distance of every pair of points
    '''
    reachability_distances = [[0 for j in range(len(distance_matrix))] for i in range(len(distance_matrix))]
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix)):
            reachability_distances[i][j] = max(k_distances[j], distance_matrix[i][j])
        print(i+1)
    return reachability_distances 
  

def find_lrd(distance_matrix, k_distances, reachability_distances):
    '''
    finding all guys within the k-distance
    And then use that to find the LRD of every point
    '''
    lrd = [0 for i in range(len(distance_matrix))]
    for i in range(len(distance_matrix)):
        i_distances = distance_matrix[i]
        r_sum = 0
        r_count = 0
        for j in range(len(i_distances)):
            if j==i:
                continue
            if distance_matrix[i][j] <= k_distances[i]:
                r_sum += reachability_distances[i][j]
                r_count += 1
        lrd[i] = r_count/r_sum
    return lrd


def find_lof(distance_matrix, k_distances, reachability_distances, lrd):
    '''
    Finding the LOF of every point
    '''
    lof = [0 for i in range(len(distance_matrix))]
    for i in range(len(distance_matrix)):
        i_distances = distance_matrix[i]
        lrd_sum = 0
        lrd_count = 0
        for j in range(len(i_distances)):
            if j==i:
                continue
            if distance_matrix[i][j] <= k_distances[i]:
                lrd_sum += lrd[j]/lrd[i]
                lrd_count += 1
        lof[i] = lrd_sum/lrd_count
    return lof
        
        

def main():
    df = pd.read_csv('credit.csv')
    df.drop(['Time','Class'], inplace=True, axis=1)
    df = (df - df.mean())/df.std()
    #data = df.T.to_dict('list')
    #build_distance_matrix(data)
    #del data
    k_values = [100]
    distance_matrix = None
    with open('distances.pickle', 'rb') as fp:
        distance_matrix = pickle.load(fp)
    for k in k_values:
        k_distances = find_k_distances(distance_matrix, k)
        reachability_distances = find_reachability(distance_matrix, k_distances)
        lrd = find_lrd(distance_matrix, k_distances, reachability_distances)
        lof = find_lof(distance_matrix, k_distances, reachability_distances, lrd)
        df['Outlier'] = 0
        j = 0
        for i in lof:
            if i > 1.6:
                df.set_value(j, 'Outlier', 1)
            j = j + 1
        df.to_csv(f'lof_output_{k}.csv')
        
    
    
if __name__ == '__main__':    
    main()
    
    




