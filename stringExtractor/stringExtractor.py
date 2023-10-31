""" 
The first argument is the source file
The second argument is the minimum string length that will be considered
The third argument is the number of 
"""

import sys
import os

from collections import Counter

from datetime import datetime

print(os.getcwd())


def get_substrings(input_string, min_length=int(sys.argv[2])):
    substrings = [input_string[i:j] for i in range(
        len(input_string)) for j in range(i + min_length, len(input_string) + 1)]
    return substrings


def most_common_substrings(input_string, num_common_substrings):
    substrings = get_substrings(input_string)
    common_substrings = Counter(substrings).most_common(num_common_substrings)
    return common_substrings


sourceFile = open(sys.argv[1], "r")
input_string = sourceFile.read()

while '"\'"' in input_string:
    input_string = input_string.replace('"\'"', '')

# Remove keywords
takeInput = False
keyWordSkip = False
extracted_string = ''
for character in input_string:
    if character == '\\':
        keyWordSkip = True
        continue

    if character == '\'':
        if takeInput == True:
            keyWordSkip = False
            takeInput = False
        else:
            keyWordSkip = False
            takeInput = True
        continue

    if takeInput == True and keyWordSkip == False:
        extracted_string = extracted_string + character

while '\"' in extracted_string:
    extracted_string = extracted_string.replace('\"', '')

# You can change this number to get the desired number of common substrings
num_common = int(sys.argv[3])
common_substrings = most_common_substrings(extracted_string, num_common)

for substring, count in common_substrings:
    print(f"'{substring}': {count} times")

# get the current time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime(
    "%d-%m-%Y %H %M %S")

os.makedirs("Extracted Strings", exist_ok=True)

argFile = sys.argv[1][:-4]

while '\\' in argFile:
    argFile = argFile.replace('\\', '')

while ' ' in argFile:
    argFile = argFile.replace(' ', '')

while '.' in argFile:
    argFile = argFile.replace('.', '')

with open("Extracted Strings\\" + argFile + ".txt", 'a+') as file:
    file.write(str(extracted_string))
