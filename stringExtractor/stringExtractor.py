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

# Get the substrings in a string


def get_substrings(input_string, min_length=int(sys.argv[2])):
    substrings = [input_string[i:j] for i in range(
        len(input_string)) for j in range(i + min_length, len(input_string) + 1)]
    return substrings

# Get the most common substrings


def most_common_substrings(input_string, num_common_substrings):
    substrings = get_substrings(input_string)
    common_substrings = Counter(substrings).most_common(num_common_substrings)
    return common_substrings


# Open source file and store as a string
sourceFile = open(sys.argv[1], "r")
input_string = sourceFile.read()

# Remove keywords
while '"\'"' in input_string:
    input_string = input_string.replace('"\'"', '')

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

# 3rd argument is the number of common substring results to display
num_common = int(sys.argv[3])
common_substrings = most_common_substrings(extracted_string, num_common)

# Display the common substrings from most common to least common
for substring, count in common_substrings:
    print(f"'{substring}': {count} times")

# get the current time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime(
    "%d-%m-%Y %H %M %S")

# Prepare the sourceFile name as a directory for saving the extracted keylog file
os.makedirs("Extracted Strings", exist_ok=True)

argFile = sys.argv[1][:-4]

while '\\' in argFile:
    argFile = argFile.replace('\\', '')

while ' ' in argFile:
    argFile = argFile.replace(' ', '')

while '.' in argFile:
    argFile = argFile.replace('.', '')

# Save the extracted keylogs (without keywords or keycharacters) in a file
with open("Extracted Strings\\" + argFile + ".txt", 'a+') as file:
    file.write(str(extracted_string))
