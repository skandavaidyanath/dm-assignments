# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:58:59 2019

@author: Skanda
"""

import csv
import copy
import itertools

def get_unique_items(data):
    """
	 This function reads the database and returns the list of unique items
	 """
    items = {}
    for transaction in data:
        for item in transaction:
            if item in items.keys():
                items[item] = items[item] + 1
            else:
                items[item] = 1
    return items


def c_to_l(data, c, min_support):
    """
	Converts Ci i.e. candidates to Li i.e. prunded candidates with respect to the minimum support
	"""
    l = []
    lsup = []
    for item_set in c:
        support = 0
        for transaction in data:
            if (set(item_set).issubset(set(transaction))):
                support = support + 1
        if support >= min_support:
            l.append(item_set)
            lsup.append(support)
    return l,lsup


def remove_duplicates(lst):
    """
	Utility function that removes the duplicate lists in a nested list of lists
	"""
    unique_set_lst = []
    unique_lst = []
    for row in lst:
        unique_row = set(row)
        if unique_row not in unique_set_lst:
            unique_set_lst.append(unique_row)
    for row in unique_set_lst:
        unique_lst.append(list(row))
    return unique_lst
    

def l_to_c(l, req_common):
    """
	Converts Li i.e. candidates to Ci+1 i.e. prunded candidates of bigger size 
	"""
    copy1 = copy.deepcopy(l)
    copy2 = copy.deepcopy(l)
    c = []
    for item_set1 in copy1:
        for item_set2 in copy2:
            new_item_set = []
            intersection = [value for value in item_set1 if value in item_set2]
            num_common = len(intersection)
            if num_common == req_common:
                new_item_set = item_set1 + item_set2
                c.append(new_item_set)
    return remove_duplicates(c)


def findMaximal(freqSet):
    """
	Finds the maximal item sets given the list of freqeunt item sets 
	"""
    maximal = []
    for item in freqSet:
        notmax = 0
        if isinstance(item, list):
            for sup in freqSet:
                if set(sup).issuperset(set(item)) and len(sup) == len(item) + 1:
                    notmax = 1
            if notmax == 0:
                maximal.append(item)
    return maximal



def findClosed(freqSet, freqSup):
    """
	Finds the list of closed item sets given the list of frequent item sets
	"""
    closed = []
    for item in freqSet:
        notclosed = 0
        if isinstance(item, list):
            for sup in freqSet:
                if set(sup).issuperset(set(item)) and freqSup[freqSet.index(item)] == freqSup[freqSet.index(sup)] and item != sup:
                    notclosed = 1
            if notclosed == 0:
                closed.append(item)
    return closed


def generateAssociationRule(freqSet):
    """
	Generates the associaciation rules given the frequent item sets
	"""
    associationRule = []
    for item in freqSet:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length))
                    temp = []
                    LHS = []
                    for RHS in combinations:
                        LHS = set(item) - set(RHS)
                        temp.append(list(LHS))
                        temp.append(list(RHS))
                        associationRule.append(temp)
                        temp = []
                    length = length - 1
    return associationRule                


def aprioriOutput(rules, dataSet, minimumSupport, minimumConfidence):
    """
	Finds the rules that breach the minimum confidence threshold and gives the output
	"""
    returnAprioriOutput = []
    for rule in rules:
        supportOfX = 0
        supportOfY = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for transaction in dataSet:
            if set(rule[0]).issubset(set(transaction)):
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                supportOfXandY = supportOfXandY + 1
            if set(rule[1]).issubset(set(transaction)):
                supportOfY = supportOfY + 1
        supportOfXinPercentage = (supportOfX * 1.0 / len(dataSet)) * 100
        supportOfXandYinPercentage = (supportOfXandY * 1.0 / len(dataSet)) * 100
        confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100
        if confidence >= minimumConfidence:
            supportOfXAppendString = "Support Of X: " + str(supportOfX)
            supportOfYAppendString = "Support Of Y: " + str(supportOfY)
            confidenceAppendString = "Confidence: " + str(round(confidence, 4)) + "%"
            returnAprioriOutput.append(supportOfXAppendString)
            returnAprioriOutput.append(supportOfYAppendString)
            returnAprioriOutput.append(confidenceAppendString)
            returnAprioriOutput.append(rule)
    return returnAprioriOutput   

    
def main():
    #Reading the database
    data = []
    with open('groceries.csv', 'r') as fp:
        reader = csv.reader(fp)
        for row in reader:
            data.append(row)
    fp.close()
    items = get_unique_items(data)
    temp_c1 = list(items.keys())
    c1 = []
    for string in temp_c1:
        c1.append([string])
    del temp_c1
    #total_number_of_transactions = len(data)  #9835
    total_number_of_items = len(items)  #169
	 #Setting the minimum support and minimum confidence
    min_support = 500
    min_confidence = 20
    l1,l1sup = c_to_l(data, c1, min_support)
    del items
    del c1
    current_l = copy.deepcopy(l1)
    frequent_item_sets = l1
    frequent_item_setssup = l1sup
    #Generating all frequent item sets using the apriori principle
    for i in range(2, total_number_of_items + 1):
        current_c = l_to_c(current_l, i-2)
        current_l, current_lsup = c_to_l(data, current_c, min_support)
        frequent_item_sets.extend(current_l)
        frequent_item_setssup.extend(current_lsup)
        if len(current_l) == 0:
            break
    print(len(frequent_item_sets))
    maximal = []
    #Generating maximal item sets
    maximal = findMaximal(frequent_item_sets)
    closed = []
    #Generating closed item sets
    closed = findClosed(frequent_item_sets, frequent_item_setssup)
    assoc_rules = []
    #Finding association rules
    assoc_rules = generateAssociationRule(frequent_item_sets)
    #Pruning rules based on confidence and giving appropriate output
    AprioriOutput = aprioriOutput(assoc_rules, data, min_support, min_confidence) 
    counter = 1
    if len(AprioriOutput) == 0:
        print("There are no association rules for this support and confidence.")
    else:
        for i in AprioriOutput:
            if counter == 4:
                print(str(i[0]) + "------>" + str(i[1]))
                counter = 0
            else:
                print(i, end='  ')
            counter = counter + 1
    

if __name__ == '__main__':
    main()