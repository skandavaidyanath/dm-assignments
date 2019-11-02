from apriori import get_unique_items
import csv
import copy


class FPTree(object):
    """
    Implementation of a FPtree data-structure
    """

    def __init__(self, item):
        self.item = item
        self.children = []
        # Is it the last item of the transaction.
        self.transaction_finished = False
        # How many times this item appeared in the addition process
        self.counter = 1
        self.next = None
        self.parent = None

    def add(self, transaction, head_pointers, current_pointers):
        '''
        Adding a transaction in the FPtree structure
        '''
        node = self
        for item in transaction:
            found_in_child = False
            # Search for the item in the children of the present `node`
            for child in node.children:
                if child.item == item:
                        # We found it, increase the counter by 1 to keep track that another
                    # transaction has it as well
                    child.counter += 1
                    # And point the node to the child that contains this item
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new child
            if not found_in_child:
                new_node = FPTree(item)
                node.children.append(new_node)
                new_node.parent = node
                # And then point node to the new child
                node = new_node
                if item not in head_pointers.keys():
                    head_pointers[item] = new_node
                    current_pointers[item] = new_node
                else:
                    current_pointers[item].next = new_node
                    current_pointers[item] = new_node
        # Everything finished. Mark it as the end of a transaction.
        node.transaction_finished = True

 
            
def conditional_fptree(candidate, fptree, head_pointers, min_support, partial, items, initial_counts):
	"""
	Recursive function that generates the frequent_item sets whilst generating conditional 
	FP trees and generating frequent item sets that end with the candidate item in every recursive step
	"""
    modified_counts = dict.fromkeys(initial_counts, 0)
    horizontal_current = head_pointers[candidate]
    while horizontal_current != None:
        vertical_current = horizontal_current.parent
        while vertical_current.parent != None:
            modified_counts[vertical_current] += initial_counts[horizontal_current]
            vertical_current = vertical_current.parent
        horizontal_current = horizontal_current.next
    item_sets = []
    flag = 0
    for item,head in head_pointers.items():
        if item == candidate:
            continue
        support = 0
        current = head
        while current != None:
            support += modified_counts[current]
            current = current.next
        #print('Candidate is ', candidate)
        #print('Item is ', item)
        #print('Support is ', support)
        if support >= min_support:
            flag = 1
            temp_partial = copy.deepcopy(partial)
            temp_partial.append(item)
            item_sets.append(temp_partial)
            item_sets.extend(conditional_fptree(item, fptree, head_pointers, min_support, temp_partial, items, modified_counts))
    if flag == 0:
        #print('Candidate is ', candidate)
        #print('Returning empty')
        return []
    return item_sets
    
    
 
    

def findMaximal(freqSet):
	"""
	Finds the maximal item sets given the list of freqeunt item sets 
	"""
    maximal = []
    for item in freqSet:
        notmax = 0
        if isinstance(item, list):
            for sup in freqSet:
                if set(sup).issuperset(set(item)) and len(sup) == len(item) + 1:          #No immediate superset should be frequent
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
                if set(sup).issuperset(set(item)) and freqSup[freqSet.index(item)] == freqSup[freqSet.index(sup)] and item != sup:    #No superset should have same support
                    notclosed = 1
            if notclosed == 0:
                closed.append(item)
    return closed


def generateAssociationRule(freqSet):
	"""
	Generates the association rules given the frequent item sets
	"""
    associationRule = []
    for item in freqSet:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length))    #Generating association rules based on all possible combinations
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
            if set(rule[0]).issubset(set(transaction)):            #Calculating support of X
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):  #Calculating support of X & Y
                supportOfXandY = supportOfXandY + 1
            if set(rule[1]).issubset(set(transaction)):            #Calculating support of Y
                supportOfY = supportOfY + 1
        supportOfXinPercentage = (supportOfX * 1.0 / len(dataSet)) * 100
        supportOfXandYinPercentage = (supportOfXandY * 1.0 / len(dataSet)) * 100
        confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100      #Calculating confidence
        if confidence >= minimumConfidence:                        #Pruning rules based on confidence
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
	#Getting a list of unique items
    items = get_unique_items(data)
	#Setting the minimum support
    min_support = 100
	#Pruning the items that do not meet minimum support
    pruned = []
    for key,value in items.items():
        if value < min_support:
            pruned.append(key)
    for item in pruned:
        del items[item]
    for transaction in data:
        for item in pruned:
            if item in transaction:
                transaction.remove(item)
	#Building the FP Tree
    head_pointers = {}
    current_pointers = {}
    fptree = FPTree('*')
    for transaction in data:
        sorted_transaction = sorted(transaction, key=items.get)
        fptree.add(sorted_transaction, head_pointers, current_pointers)
    item_list = sorted(items, key=items.get)
    fis = []
    initial_counts = {}
    for item,head in head_pointers.items():
        current = head
        while current != None:
            initial_counts[current] = current.counter
            current = current.next
	#Finding the frequent item sets
    for candidate in item_list:
        fis.append(conditional_fptree(candidate, fptree, head_pointers, min_support, [candidate], items, initial_counts))
    frequent_item_sets = []
    for value in item_list:
        frequent_item_sets.append([value])
    for lst in fis:
        if len(lst) == 0:
            continue
        else:
            for sublst in lst:
                if len(sublst) > 0:
                    frequent_item_sets.append(sublst)
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
                print(str(i[0]) + "------>" + str(i[1]))    #Displaying Apriori output
                counter = 0
            else:
                print(i, end='  ')
            counter = counter + 1
        
    
if __name__ == '__main__':
    main()
