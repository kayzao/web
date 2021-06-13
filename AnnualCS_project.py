import matplotlib.pyplot as plt
import time
import random
import pprint

source = open("source1_clean.txt", encoding='utf8')
source = source.read()

#Type function to print characters one by one
def type(string, delay):
    for char in string:
        print(char, end="")
        time.sleep(delay)
    print()

#Ask how many words the user wants to type
total = 60
type("How many words would you like to type? (60 words is recommended)", 0.01)
print(end=">>> ")
answer = input()
try:
    total = int(answer)
    if total <= 0:
        type("Your input was not a valid integer; You will type the default of 60 words.", 0.01)
        total = 60
    elif total == 1: type("Your input was a valid integer; You will type a single word. liek y just one.", 0.01)
    else: type("Your input was a valid integer; You will type " + str(total) + " words.", 0.01)
except ValueError:
    type("Your input was not a valid integer; You will type the default of 60 words.", 0.01)

time.sleep(0.3)
#This part of the code takes in a book from Project Gutenberg, and returns random numbers from it, while removing most punctuation and all number-keys-related things, such as 31st
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
words = {}
arr = source.split()
while len(words) < total: #approximate number of words to be printed
    randindex = random.randint(0, len(arr) - 1)
    for num in numbers:
        if not num in arr[randindex]: #if generated word has no number, add to dictionary
            if arr[randindex].lower() in words:
                words[arr[randindex].lower()] += 1
                break
            else:
                words[arr[randindex].lower()] = 1
                break

string = ""
first = True #to tell if the word is first word in string
for word in words:
    if first:
        string += word
        first = False
    else:
        string += " " + word

#to remove punctuation and other similar symbols
x = 0
while x < len(string):
    num = ord(string[x])
    if (num < 97 or num > 122) and num != 45 and num != 32: #if char isn't a-z or '-'
        string = string[:x] + string[x+1:]
        continue #x remains at same value
    x += 1

if total == 1: print("Enter the word that will appear below:")
else: print("Enter the words that will appear below:")
time.sleep(1)

type("="*100, 0.01)
type(string, 0.01) #type series of words
type("="*100, 0.01)

print(end=">>> ")
starttime = time.time()
answer = input()

t = round(time.time() - starttime, 2)
type("Seconds elapsed: " + str(t), 0.01)

#average length of words in enlgish is 4.7 characters, so we can divide # characters by 4.7 to get words per second.
charavg = round(len(answer) / t, 2)
if len(answer) != 0:
    type("You on average typed " + str(charavg) + " characters per second", 0.03)
    type("You typed at about " + str(round(60 * ((len(answer) / 4.7) / t), 2)) + " wpm.", 0.03)

#Code below is for counting mistakes and correct characters, by splitting the answer + string into lists, and comparing charcters of each word in both lists.
mistakes = {}
correct = {}
wrongwords = {}
l_s = string.split()
l_a = answer.split()
totalchar = len(answer)-(len(l_a) - 1) #total num of characters inputed (without spaces)
if len(l_a) == 0: totalchar = 0
correctcount = 0
for x in range(min(len(l_s), len(l_a))):
    s = l_s[x] #the xth word in string
    a = l_a[x] #the xth word in answer
    if s != a:
        if s in wrongwords:
            wrongwords[s] += 1
        else:
            wrongwords[s] = 1
    y = 0
    while y < min(len(s), len(a)): #while y < min length of the 2 words
        #if char != char
        if s[y] != a[y]:
            if s[y] in mistakes:
                mistakes[s[y]] += 1
            else:
                mistakes[s[y]] = 1
        #else if char == char
        elif s[y] == a[y]:
            if s[y] in correct:
                correct[s[y]] += 1
            else:
                correct[s[y]] = 1
            correctcount += 1
        y += 1
    if len(s) < len(a): #If answer word is too long:
        y = len(s)
        while y < len(a):
            if s[-1] in mistakes:
                mistakes[s[-1]] += 1
            else:
                mistakes[s[-1]] = 1
            y += 1
    elif len(s) > len(a): #else if answer word is too short
        y = len(a)
        while y < len(s):
            if s[y] in mistakes:
                mistakes[s[y]] += 1
            else:
                mistakes[s[y]] = 1
            y += 1

#if there are extra words, ignore them
#if there are less answer words than string words:
if len(l_s) > len(l_a):
    for x in range(len(l_s) - len(l_a)):
        if l_s[len(l_a) + x] in wrongwords:
            wrongwords[l_s[len(l_a) + x]]
        else:
            wrongwords[l_s[len(l_a) + x]]

#Code below is to print out the mistakes.
string_errors = ""
if len(answer.split()) == 0:
    type("You didn't type anything.", 0.03)
if answer == string:
    type("You answered correctly.", 0.03)
elif answer != string and len(answer) != 0:
    type("You didn't answer correctly.", 0.03)
    string_errors = "You mistyped "
    x = 0
    for word in wrongwords:
        if len(wrongwords) == 1: #If theres only one mistaken word
            string_errors += "'" + word + "' " + str(wrongwords[word])
            if wrongwords[word] == 1: string_errors += " time."
            else: string_errors += " times."
        elif x + 1 == len(mistakes): #if there are multiple words, and this is last one
            string_errors += "and " + "'" + word + "' " + str(wrongwords[word])
            if wrongwords[word] == 1: string_errors += " time."
            else: string_errors += " times."
        else:
            string_errors += "'" + word + "' " + str(wrongwords[word])
            if wrongwords[word] == 1: string_errors += " time, "
            else: string_errors += " times, "
    type(string_errors, 0.03)
accuracy = round((correctcount / totalchar) * 100, 2)
if not accuracy == 100.00:
    type("You typed with an accuracy of " + str(accuracy) + "%.", 0.03)
#plot character (x-axis), and percentage right (y-axis), which is # right / (# right + # wrong)
chars = []
for x in range(26):
    if chr(x+97) in string: chars.append(chr(x+97)) #if char from a-z is in string, add to chars
percentages = []
for x in chars:
    if x in correct and not x in mistakes: percentages.append(100) #if char was typed correct all the time
    elif x in mistakes and not x in correct: percentages.append(0) #if char was typed wrong all the time
    else:
        percentages.append((correct[x] / (correct[x] + mistakes[x])) * 100)

type("Would you like to see a graph of the percentage each time each character was typed correctly? (Y for yes | N for no)", 0.03)
print(end=">>> ")
answer = ""
valid = False
while(not valid):
    answer = input()
    if answer.lower() == "y" or answer.lower() == "n":
        valid == True
        break
    type("That was not a valid answer. Enter 'Y' for yes or 'N' for no.", 0.03)
    print(end=">>> ")
plt.title("Percentages of Times a Character was Typed Correctly")
plt.xlabel("Characters")
plt.ylabel("Percentage (%)")
plt.ylim([0, 100])
plt.bar(chars, percentages)
if answer.lower() == "y":
    plt.show()
type("(End of this program)", 0.1)
