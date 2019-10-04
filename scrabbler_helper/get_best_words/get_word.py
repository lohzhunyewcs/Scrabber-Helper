# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 16:34:40 2018

@author: Loh Zhun Yew
@StudentID: 29406641
"""

def suggest_word(string):
    # TODO: Add bonus score 
    return solve_task3(string, 0, 0)

class Node(object):
    def getThings(self):
        """
        placeholder function for debugging purposes
        """
        print('AnagramNode:')
        print("self.item", self.item)
        print("self.childnren", [i.item for i in self.children])    

    def __str__(self):
        """
        change the $ to soemthing else to signify start
        """
        item = self.item if self.item else '$'
        return "Parent: " + str(item) + "\nChildren: " + str(self.children)

    def __repr__(self):
        item = self.item if self.item else '$'
        return "Parent: " + str(self.item) + "\nChildren: " + str(self.children)[1:-1]

    def isChild(self, character):
        """
        returns a tuple (boolean, position)
        """
        for child in range(len(self.children)):
            if self.children[child].item == character:
                return (True, child)
        return (False, -1)

class AnagramNode(Node):
    """
    Parent Node should be None similar to TrieNode
    Nodes used to form a trie
    if the word is abc, bac, a trie "a" -> "b" -> "c" -> "$"
    is formed
    at the end of "$", a TrieNode/Tries is made to put the strings
    
    Properties:
        - At Node "$", a  counter is given to count the number of anagrams
        - At Node "$", a list of length N(length of anagram) is made where
          the indexes contain the string of every word
              - e.g: abc, bac, list = ["ab", "ba", "cc"]
        
    """
    def __init__(self, item, end = True):
        self.children = []
        if item is None:
            self.item = None
        elif item == '$':
            self.item = '$'
            self.counter = 0
            self.max = []
            self.length = 0
        elif len(item) == 1:
            self.item = item
            if end:
                self.children.append(AnagramNode('$'))
        elif len(item) > 1:
            self.item = item[0]
            self.addAnagram(item[1:])
                        
    def getThings(self):
        """
        placeholder function for debugging purposes
        """
        print('AnagramNode:')
        print("self.item", self.item)
        print("self.childnren", [i.item for i in self.children])
        
    def addAnagram(self, string):
        child, index = self.isChild(string[0])
        if child:
            if len(string) == 1:
                self.children[index].append(AnagramNode('$'))
            else:
                self.children[index].addAnagram(string[1:])
        elif len(string) == 1:
            self.addCharacter(string)
        else:
            newChild = AnagramNode(string[0], end = False)
            newChild.addAnagram(string[1:])
            self.children.append(newChild)

    def addCharacter(self, character):
        """
        assumes character is a string of length 1
        """
        if not self.isChild(character)[0]:
            newChild = AnagramNode(character)
            self.children.append(newChild)
    
    def addString(self, string, original = None, start = True):
        """
        Looks if the anagram is in the tree
        if it is:
        Creates a TrieNode if there is none and add string to it
        otherwise:
            creates new anagram nodes and everything then
            create the trie
            
        TODO: optimize inTrie to return a list of all the child indexes if true, -1 otherwise
                can reduce complexity here
        """
        if start:
            original = string
            string = countingSort(string)
            if string[-1] != '$':
                string += '$'
            if self.inTrie(string):
                _, index = self.isChild(string[0])
                return self.children[index].addString(string[1:], original, start = False)
            else:
                self.addAnagram(string)
                return self.addString(original)
        else:
            _, index = self.isChild(string[0])
            if string != '$':#Keep tranversing until it hits the end '$'
                return self.children[index].addString(string[1:], original, start = False)
            else: # if the item is '$'
                self.children[index].children.append(TrieNode(original))#self.children[index] is the '$' Node
                self.children[index].counter += 1
                if self.children[index].length == 0:
                    length = len(original)
                    self.children[index].length = length
                    self.children[index].max = [original]*length
                else:
                    for i in range(len(original)):
                        if get_letter_score(original[i]) == get_letter_score(self.children[index].max[i][i]):
                            self.children[index].max[i] = min(original, self.children[index].max[i])
                        elif get_letter_score(original[i]) > get_letter_score(self.children[index].max[i][i]):
                            self.children[index].max[i] = original
                """
                if ==:
                    compare strings
                if getScore[newString[i]] > getScore[currentMax[i]]:
                    replace self.currentmax[i] = newString
                """
                return self.children[index].counter
    
    def inTrie(self, string, start = True):
        """
        Used only to check anagramList
        """
        if start and string[-1] != '$':
            string += '$'
        child, index = self.isChild(string[0])
        if child:
            if len(string) == 1:
                return True
            else:
                return self.children[index].inTrie(string[1:], start = False)
        else:
            return False

class TrieNode(Node):
    """
    Parent/Root Node should be None
    A Node that branches out to other nodes to form strings
    """
    def __init__(self, item, end = True):
        self.children = []
        if item is None:
            self.item = None
        elif item == '$':
            self.item = '$'
        elif len(item) == 1:
            self.item = item
            if end:
                self.children.append(TrieNode('$'))
        elif len(item) > 1:
            self.item = item[0]
            self.addString(item[1:])
    
    def getThings(self):
        """
        placeholder function for debugging purposes
        """
        print('TrieNode:')
        print("self.item", self.item)
        print("self.childnren", [i.item for i in self.children])
    
    def addString(self, string):
        child, index = self.isChild(string[0])
        if child:
            if len(string) == 1:
                self.children[index].append(TrieNode('$'))
            else:
                self.children[index].addString(string[1:])
        elif len(string) == 1:
            self.addCharacter(string)
        else:
            newChild = TrieNode(string[0], end = False)
            newChild.addString(string[1:])
            self.children.append(newChild)
                
    def addCharacter(self, character):
        """
        assumes character is a string of length 1
        """
        if not self.isChild(character)[0]:
            newChild = TrieNode(character)
            self.children.append(newChild)

def radixSort(toSort):
    if type(toSort) == list:
        return radixSortStringsList(toSort)
    elif type(toSort) == str:
        return countingSort(toSort)

def countingSort(string):
    """
    """
    maxValue = ord(max(string)) - 97
    resultList = []
    for i in range(maxValue + 1):
        resultList.append([])
    for j in string:
        resultList[ord(j) - 97].append(j)
    finalString = [] 
    for k in resultList:
        finalString += k
    return ''.join(finalString)

def radixSortStringsList(lst, key = 0):
    """
    Guideline:
    ogList = [cb,ab,ba,bb, ca, aa]
    first loop = [[ab, aa], [ba, bb] , [cb, ca]]
    second loop = [[[aa], [ab]], [[ba], [bb]], [[ca], [cb]]]
    TODO: make it work for strings
    """
    if len(lst) == 0 or len(lst) == 1 or sameWords(lst):
        return lst
    maxValue = 27#ord(max(lst)[key]) - 97, <-- can change to another better function for space complexity
    resultList = []
    for i in range(maxValue + 1):
        resultList.append([])
    for j in lst:
        if len(j) > key:
            resultList[ord(j[key]) - 96].append(j)
        else:
            resultList[0].append(j)
    recursiveList = []
    for alphabets in resultList:
        if len(alphabets) != 0:
            result = radixSortStringsList(alphabets, key +  1)
            recursiveList += result#(radixSortStringsList(alphabets, key +  1))
    final = []
    for k in recursiveList:
        final += [k]
    return final

def sameWords(lst):
    firstWord = lst[0]
    for i in lst:
        if i != firstWord:
            return False
    return True

def loadWords(fileName):
    """
    Complexity: 
        Worse Case O(T) where T is the total number of characters
    This only occurs when there are no common prefixes 
    """
    if '.txt' not in fileName:
        fileName += '.txt'
    file = open(fileName, 'r')
    wordList = AnagramNode(None)
    mostAnagram = None
    mostCounter = 0
    i = 0
    for word in file:
        word = word.strip().lower()
        counter = wordList.addString(word)
        if counter >= mostCounter:
            mostCounter = counter
            mostAnagram = word
    return wordList, mostAnagram

def getAnagramNode(wordList, string, start = True):
    """
    Assumes wordList is a AnagramNode and string is in wordList
    intended to be a helper function only
    Complexity: 
        Worse Case:O(k) where k is the number of characters in a string
    """
    if start:
        string = countingSort(string)
        if len(string) == 0 or not wordList.inTrie(string):
            return None
        elif string[-1] != '$':
            string += "$"
    _, index = wordList.isChild(string[0])
    if string != '$':
        return getAnagramNode(wordList.children[index], string[1:], start = False)
    else:
        return wordList.children[index]
    
def getAnagrams(wordList, string):
    """
    Assumes wordList is a Trie and string is in wordList
    
    Uses getAnagramNode to get the node
    Travesees the TrieNode to get all the nodes
    Complexity:
        Worse Case: O(k + W) where k is the number of characters of the anagram  
    """
    node = getAnagramNode(wordList, string)
    if node is None:
        return []
    else:
        return radixSort(getAnagramsAux(node))
    
    
def getAnagramsAux(node, parentString = ""):
    """
    Extended function used to recursively get all the strings
    Complexity:
        Worse Case: O(k) where k is the total number of characters in the anagram list
    """
    if len(node.children) == 1 and node.children[0].item == '$':
        return [parentString]
    resultList = []
    for child in node.children:
        newString = parentString + child.item
        resultList += getAnagramsAux(child, newString)
    return resultList

def solve_task1():
    # implement your solution for task 1 inside this function.
    # this function must return a list corresponding to the largest group of anagrams in sorted order
    # feel free to create as many other functions as needed
    """
    Complexity:
        Worse Case: O(T)
    """
    global wordList
    wordList, largestAnagram = loadWords("./get_best_words/dictionary.txt")
    result = getAnagrams(wordList, largestAnagram)
    return result

def solve_task2(query):
    # implement your solution for task 2 inside this function. 
    # this function must return all words that can be made using all letters of the query (in sorted order)
    # feel free to create as many other functions as needed
    """
    Worse Case: O(k + W)
    """
    resultList = getAnagrams(wordList, query)
    return resultList

def stringsCombo(string):
    """
    assumes input string is a string
    returns a list of possible strings formed by the input
    complexity: 2^n where n is length of string
    """
    n = len(string)
    resultList = [] 
    for i in range(2**n - 1, 0, -1):
        binaryFormat = bin(i)
        newStr = ""
        j = -1
        while binaryFormat[j] != 'b':
            if binaryFormat[j] == '1':
                newStr = string[int(j)] + newStr
            j -= 1
        resultList.append(newStr)
    return resultList

def getScore(combo, comboScore, x, y):
    return comboScore + get_letter_score(combo[x]) * (y - 1)

def getSmallestAnagram(node, parentString = ""):
    if len(node.children) == 1 and node.children[0].item == '$':
        return parentString
    result = ""
    smallestChild = None
    for child in node.children:
        if smallestChild is None or smallestChild.item > child.item:
            smallestChild = child
    result += getSmallestAnagram(smallestChild, parentString + smallestChild.item)
    return result

def solve_task3(query, letter_num, boost_amount):
    # implement your solution for task 3 inside this function. 
    # this function must return a list containing two values [bestWord, score] where bestWord is the best possible world and score is its score
    # feel free to create as many other functions as needed
    """
    Asusmes wordList is a trie
    query is string to be queried
    x: position of string that will have a bonus multiplier(y) must - 1 when using for index
    y: bonus multiplier
    returns [string, score]    
    
    Complexity:
        Worse Case: O(2^k*k)
        2^k to generate (2^k - 1) combinations and needed to get k nodes
    """
    query = countingSort(query)
    combos = stringsCombo(query)
    currentMax = [0, "n/a"]
    #when adding bonuses later, just score multiply by( y - 1)
    for combo in combos:
        node = getAnagramNode(wordList, combo)
        if node is not None:
            comboScore = sum([get_letter_score(i) for i in combo])
            if len(combo) >= letter_num:
                maxString = node.max[letter_num - 1]
                current = [getScore(maxString, comboScore, letter_num - 1, boost_amount), maxString]
            else:
                maxString = getSmallestAnagram(node)
                current = [comboScore, maxString]                
            if current > currentMax:
                currentMax = current            
    currentMax.reverse()
    return currentMax




#############################################################################
# WARNING: DO NOT MODIFY ANYTHING BELOW THIS.
# PENALTIES APPLY IF YOU CHANGE ANYTHING AND TESTER FAILS TO MATCH THE OUTPUT
#############################################################################

# this function returns the score of a given letter
def get_letter_score(char):
    return score_list[ord(char)-96]

               
def print_task1(aList):
    string = ", ".join(aList)
    print("\nThe largest group of anagrams:",string)

def print_task2(query,aList):
    string = ", ".join(aList)

    print("\nWords using all letters in the query ("+query+"):",string)

def print_task3(query,score_boost,aList):
    if len(aList) == 0:
        print("\nThe best word for query ("+query+","+score_boost+"):", "List is empty, task not attempted yet?")
    else:
        print("\nThe best word for query ("+query+","+score_boost+"):",str(aList[0])+", "+str(aList[1]))
        
def print_query(query,score_boost):
    unique_letters = ''.join(set(query))
    unique_letters = sorted(unique_letters)
    scores = []
    for letter in unique_letters:
        scores.append(letter+":"+str(get_letter_score(letter)))
    print("Scores of letters in query: ", ", ".join(scores))
    
        
# score_list is an array where the score of a is at index 1, b at index 2 and so on
score_file = open("./get_best_words/Scores.txt")
score_list = [0 for x in range(27)]
for line in score_file:
    line = line.strip()
    line = line.split(":")
    score_list[ord(line[0])-96] = int(line[1])
anagrams_list = solve_task1()    
print_task1(anagrams_list)

# query = input("\nEnter the query string: ")


# while query != "***":
#     score_boost = input("\nEnter the score boost: ")
#     print_query(query,score_boost)
    
#     score_boost_list = score_boost.split(":")
#     letter_num =  int(score_boost_list[0])
#     boost_amount = int(score_boost_list[1])
    
#     results = solve_task2(query)
#     print_task2(query,results)

#     answer = solve_task3(query, letter_num, boost_amount)
#     print_task3(query,score_boost,answer)
    
#     query = input("\nEnter the query string: ")

# print("See ya!")
