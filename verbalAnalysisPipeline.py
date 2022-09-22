#verbalAnalysisPipeline reads in the stimLists from a subjects session and checks the words against 
#the subject provided recall list.
#if files are not in the right place you get a "division by zero" error
#bc ┌( ಠ_ಠ)┘
#do the imports
import glob
import sys
from itertools import chain

#initialize all sessions study list
allSessionsStudy = []
practiceStudy    = []

subNum    = input('Type Subject Number to Analyze: ')
runDate   = input('Enter Date Subject Was Run: ')
cobraTag  = 'cobra1_' + subNum + '_'
cobraPTag = 'cobra1_p' + subNum + '_'
#set the path for folder containing the study files
#change name of behavior folder to be analyzed
#main program files
path1 = 'C:\\Users\\Owner\\Desktop\\behave\\' + cobraTag + runDate + '\\stimList_stud*'
#practice files
path2 = 'C:\\Users\\Owner\\Desktop\\behave\\' + cobraPTag + runDate + '\\stimList_stud*'
for filename in glob.glob(path1):
    with open(filename, 'r') as f:
        for line in f:
            allSessionsStudy.append(line)
for filename in glob.glob(path2):
    with open(filename, 'r') as f:
        for line in f:
            allSessionsStudy.append(line)
            practiceStudy.append(line)

#initialize cleaned study list --> change to make sure last letter isn't dropped.
allSessionsStudyClean = []
practiceStudyClean  = []
#clean words and put in list
for word in allSessionsStudy:
    if word == allSessionsStudy[-1]:
        newWord = word[6:-4]
        allSessionsStudyClean.append(newWord)
        allSessionsStudy.pop(-1)
    else:
        newWord = word[6:-5]
        allSessionsStudyClean.append(newWord)
for word in practiceStudy:
    if word == practiceStudy[-1]:
        newWord = word[6:-4]
        practiceStudyClean.append(newWord)
        practiceStudy.pop(-1)
    else: 
        newWord = word[6:-5]
        practiceStudyClean.append(newWord)
        
#initialize all sessions test list
allSessionsTest = []
practiceTest    = []

#set the path for folder containing the test files
#change name of behavior folder to be analyzed
#main program files
path1 = 'C:\\Users\\Owner\\Desktop\\behave\\' + cobraTag + runDate + '\\stimList_test*'
#practice files
path2 = 'C:\\Users\\Owner\\Desktop\\behave\\' + cobraPTag + runDate + '\\stimList_test*'

for filename in glob.glob(path1):
    with open(filename, 'r') as f:
        for line in f:
            allSessionsTest.append(line)
for filename in glob.glob(path2):
    with open(filename, 'r') as f:
        for line in f:
            allSessionsTest.append(line)
            practiceTest.append(line)

#initialize cleaned test list
allSessionsTestClean = []
practiceTestClean    = []
#clean words and put in list
for word in allSessionsTest:
    if word == allSessionsTest[-1]:
        newWord = word[6:-4]
        allSessionsTestClean.append(newWord)
        allSessionsTest.pop(-1)
    else:
        newWord = word[6:-5]
        allSessionsTestClean.append(newWord)
        
for word in practiceTest:
    if word == practiceTest[-1]:
        newWord = word[6:-4]
        practiceTestClean.append(newWord)
        practiceTest.pop(-1)
    else: 
        newWord = word[6:-5]
        practiceTestClean.append(newWord)
    
#list for old words
computerOld = []
#list for new words
computerNew = []

#list for old practice
practiceOld = []
#list for new practice
practiceNew = []

for i in allSessionsStudyClean:
    computerOld.append(i)

for i in allSessionsTestClean:
    if i not in computerOld:
        computerNew.append(i)
        
for i in practiceStudyClean:
    practiceOld.append(i)

for i in practiceTestClean:
    if i not in practiceOld:
        practiceNew.append(i)

#create subject list dictionary
#read subject text file into dictionary
#reading the dictionary, generate lists of subject oldCorrect, subjectNewCorrect
#subjectoldWrong and subjectNewWrong, and other.

subjectWords = []
# word list files
#path = "C:\\Users\\Owner\\Desktop\cobra1_11101\subjectList.txt"
path = 'C:\\Users\\Owner\\Desktop\\behave\\' + cobraTag + runDate + '\\' + cobraTag + runDate + '.txt'
for filename in glob.glob(path):
    with open(filename, 'r') as f:
        for line in f:
            subjectWords.append(line)

#split the words at the comma for the subject provided list
splitWords = []
#split the subject words
for word in subjectWords:
    x = word.split(',')
    splitWords.append(x)

#turn the list of lists into a single list
singleList = list(chain(*splitWords))

#take the newline character off the end of the list
noLine = []
for i in singleList:
    x = i.strip()
    noLine.append(x)

#split the noLine list into two parts
#put the elements divided by 2 into first list --> keys
#put the elements not divided by 2 into the second list -- > values
# zip the two lists together as a dictionary that can then be checked against study/test lists
keyList = noLine[::2]
valueList = noLine[1::2]
subjectWords = dict(zip(keyList, valueList))

#regular
subjectOldWrong = []
subjectNewWrong = []
subjectOldCorrect = []
subjectNewCorrect = []
other = []

#practice
subjectOldPWrong = []
subjectNewPWrong = []
subjectOldPCorrect = []
subjectNewPCorrect = []
otherP = []

#iterate through the dictionary checking each value against original study/test lists
for key, value in subjectWords.items():
    if key in computerOld and value == 'old':
        subjectOldCorrect.append(key)
    elif key in computerNew and value == 'old':
        subjectOldWrong.append(key)
    elif key in computerOld and value == 'new':
        subjectNewWrong.append(key)
    elif key in computerNew and value == 'new':
        subjectNewCorrect.append(key)
    else:
        other.append(key)
        
#for practice words 
for key, value in subjectWords.items():
    if key in practiceOld and value == 'old':
        subjectOldPCorrect.append(key)
    elif key in practiceNew and value == 'old':
        subjectOldPWrong.append(key)
    elif key in practiceOld and value == 'new':
        subjectNewPWrong.append(key)
    elif key in practiceNew and value == 'new':
        subjectNewPCorrect.append(key)
    else:
        otherP.append(key)


#get subject accuracy --> TODO put in other stats
#total words
totalWords = ((len(subjectOldWrong) + (len(subjectNewWrong)) + (len(subjectOldCorrect)) + (len(subjectNewCorrect)) + (len(other))))

#percent wrong
percentWrong = (((len(subjectOldWrong) + (len(subjectNewWrong))) + (len(other))) / totalWords * 100)

#percent correct
percentCorrect = (((len(subjectOldCorrect)) + (len(subjectNewCorrect))) / totalWords * 100)

#print the output to a file in the current directory called verbalAnalysis.txt
stdoutOrigin=sys.stdout
sys.stdout = open('C:\\Users\\Owner\\Desktop\\behave\\' + cobraTag + runDate + '\\' + cobraTag + runDate + '_verbalAnalysis.txt', "w")

print("Subject Word Categorization: ")
print("Subject said old but new: ")
print(subjectOldWrong)
print("Subject said new but old: ")
print(subjectNewWrong)
print("Subject correct old recall: ")
print(subjectOldCorrect)
print("Subject correct new recall: ")
print(subjectNewCorrect)
print("Words not included in session list: ")
print(other)

print("Word Stats: ")
print("Total Subject Recalled Words: ")
print(totalWords)
print("Total Percentage of Wrong Words: ")
print(percentWrong)
print("Total Percentage of Correct Words: ")
print(percentCorrect)

#practice stats
totalPracticeWords = ((len(subjectOldPWrong) + (len(subjectNewPWrong)) + (len(subjectOldPCorrect)) + (len(subjectNewPCorrect))))
print("Total Percentage of Practice Words: ")
print((totalPracticeWords/totalWords) * 100)

print("Words from the practice session: ")
print(subjectNewPCorrect + subjectOldPCorrect + subjectNewPWrong + subjectOldPWrong)


