import math
import csv
import sys

# Implement your decision tree below
# Used the ID3 algorithm to implement the Decision Tree

# Class used for learning and building the Decision Tree using the given Training Set
class DecisionTree():
    tree = {}

    def learn(self, training_set, attributes, target):
        self.tree = build_tree(training_set, attributes, target)


# Class Node which will be used while classify a test-instance using the tree which was built earlier
class Node():
    value = ""
    children = []

    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = dictionary.keys()


# Majority Function which tells which class has more entries in given data-set
def majorClass(attributes, data, target):

    freq = {}
    index = attributes.index(target)

    for tuples in data:
        if not tuples[index] in freq:
            freq[tuples[index]] = 1 
        else:
            freq[tuples[index]] += 1

    _max = 0
    major = ""

    for key in freq.keys():
        if freq[key]>_max:
            _max = freq[key]
            major = key

    return major


# Calculates the entropy of the data given the target attribute
def entropy(attributes, data, targetAttr):

    freq = {}
    dataEntropy = 0.0

    i = 0
    for entry in attributes:
        if (targetAttr == entry):
            break
        i = i + 1

    i = i - 1

    for entry in data:
        if not entry[i] in freq:
            freq[entry[i]] = 1.0
        else:
            freq[entry[i]]  += 1.0

    for freq in freq.values():
        dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return dataEntropy


# Calculates the information gain (reduction in entropy) in the data when a particular attribute is chosen for splitting the data.
def info_gain(attributes, data, attr, targetAttr):

    freq = {}
    subsetEntropy = 0.0
    i = attributes.index(attr)

    for entry in data:
        if not entry[i] in freq:
            freq[entry[i]] = 1.0
        else:
            freq[entry[i]]  += 1.0

    for val in freq.keys():
        valProb        = freq[val] / sum(freq.values())
        dataSubset     = [entry for entry in data if entry[i] == val]
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)

    return (entropy(attributes, data, targetAttr) - subsetEntropy)


# This function chooses the attribute among the remaining attributes which has the maximum information gain.
def attr_choose(data, attributes, target):

    best = attributes[0]
    maxGain = 0;

    for attr in attributes:
        newGain = info_gain(attributes, data, attr, target) 
        if newGain>maxGain:
            maxGain = newGain
            best = attr

    return best


# This function will get unique values for that particular attribute from the given data
def get_values(data, attributes, attr):

    index = attributes.index(attr)
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])

    return values

# This function will get all the rows of the data where the chosen "best" attribute has a value "val"
def get_data(data, attributes, best, val):

    new_data = [[]]
    index = attributes.index(best)

    for entry in data:
        if (entry[index] == val):
            newEntry = []
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            new_data.append(newEntry)

    new_data.remove([])    
    return new_data


# This function is used to build the decision tree using the given data, attributes and the target attributes. It returns the decision tree in the end.
def build_tree(data, attributes, target):

    data = data[:]
    vals = [record[-1] for record in data]
    default = majorClass(attributes, data, target)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = attr_choose(data, attributes, target)
        tree = {best:{}}
    
        for val in get_values(data, attributes, best):
            new_data = get_data(data, attributes, best, val)
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = build_tree(new_data, newAttr, target)
            tree[best][val] = subtree
    
    return tree

# This function runs the decision tree algorithm. It parses the file for the data-set, and then it runs the 10-fold cross-validation. It also classifies a test-instance and later compute the average accurracy
# Improvements Used: 
# 1. Discrete Splitting for attributes "age" and "fnlwght"
# 2. Random-ness: Random Shuffle of the data before Cross-Validation
def run_decision_tree(train_set):

    data = [tuple(t) for t in train_set] 
    #print(data)
    attributes = ['middle_name','big_first_name','even_last_name','has_vowel','first_last','alphabetic_order','label']
    target = attributes[-1]

    #print("Number of records: %d" % len(data))

    tree = DecisionTree()
    tree.learn( data, attributes, target )

    return tree.tree
    
def accuracy(predicted,actual):
    acc_sum = 0
    for i in range(len(predicted)):
        if predicted[i] == actual[i]:
            acc_sum +=1
           
    return(acc_sum/len(predicted))

def create_dataset(filepath):
    data = []
    with open(filepath,encoding = 'utf8') as file:
        for line in csv.reader(file,delimiter=" "):
            #print(line)
            vowel = ["a","i","e","o","u"]
            #line= line.split()       
            label = line[0]
            #name = ' '.join(line[1:])
            
            #Feature 0: length of full name
            name_length = len(line)-1
            
            # Feature 1 : Second character of first name has vowel 
            try:
                lower_case_First_name = line[1].lower()[1]
                if lower_case_First_name in vowel:
                    has_vowel = 1    
                else:
                    has_vowel = 0
            except IndexError:
                pass

            
 
            # Feature 2: middle name is present or not       
            if name_length>2:
                middle_name = 1
            else:
                middle_name = 0 
            # Feature 3: If first name is bigger than the last name    
            if len(line[1])>len(line[-1]):
                big_first_name = 1
            else:
                big_first_name = 0    
            # Feature 4: If last name is of even lengths          
            if len(line[-1])%2==0:
                even_last_name = 1
            else:
                even_last_name=0  
            # Feature 5: If first and last letters of first name are same  
            f_letter = line[1].lower()[0]
            l_letter = line[1].lower()[-1]
            if f_letter == l_letter:
                first_last = 1
            else:
                first_last = 0  
            # Feature 6: If First  letter or first name comes before first letter of last name
            first_letter_last_word = line[-1].lower()[0] 
            if f_letter < first_letter_last_word:
                alphabetic_order = 1            
            else:
                alphabetic_order = 0   
            line = []                    
            line.append(middle_name)
            line.append(big_first_name)
            line.append(even_last_name)
            line.append(has_vowel)
            line.append(first_last)
            line.append(alphabetic_order)
            line.append(label)
            
            #line = line[3:]
            data.append(line)
    
    return data   

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    #print("fistStr : "+firstStr)
    secondDict = inputTree[firstStr]
    #print("secondDict : " + str(secondDict))
    featIndex = featLabels.index(firstStr)
    #print("featIndex : " + str(featIndex))
    key = testVec[featIndex]
    #print("key : " + str(key))
    valueOfFeat = secondDict[key]
    #print("valueOfFeat : " + str(valueOfFeat))
    if isinstance(valueOfFeat, dict):
        #print("is instance: "+str(valueOfFeat))
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        #print("is Not instance: " + valueOfFeat)
        classLabel = valueOfFeat
    return classLabel 

train = sys.argv[1] 
test =  sys.argv[2] 
  
def main():
    train_set = create_dataset(train)
    test_set = create_dataset(test)
    tree = run_decision_tree(train_set)
    output = []
    for dat in test_set:
        output.append(classify(tree, ['middle_name','big_first_name','even_last_name','has_vowel','first_last','alphabetic_order'], dat[:6]))
    print("Obtained Error:"+str((1- accuracy(output,[dat[6] for dat in test_set]))*100)+"%")        

if __name__ == "__main__":
    main()
    

    
    
    
