
import json
import random
import pyperclip



infoData = {
"ADJ": "adjective or style",   #  "ADJ": "description",
"OBJ": "thing",
"SET": "setting or place",
"ACT": "action",
}


with open('structures.json', 'r') as f:
    structureData = json.load(f)
with open('wordlist.json', 'r') as f2:
    wordlistData = json.load(f2)


def getRandomStructure(selectedStructures):
    # get weights and list
    structures = []
    structureWeights = []
    for structure in structureData:
        structures.append(structure['data'])
        structureWeights.append(structure['weight'])

    # choose random structure

    foundStructure = False
    randomStructure = ""

    # Gets the previous selected structure
    previousSelectedStructureExists = len(selectedStructures) > 0
    if previousSelectedStructureExists:
        previousSelectedStructure = selectedStructures[len(selectedStructures)-1]
    
    while not foundStructure:
        randomStructure = random.choices(structures, weights=structureWeights, k=1)[0]

        # Ensures the current structure is not the same as the previous day
        if previousSelectedStructureExists:
            if randomStructure != previousSelectedStructure:
                foundStructure = True
        if not previousSelectedStructureExists:
            foundStructure = True
        
    return randomStructure


def getRandomWord(selectedWords, partType):

    # combine all the words in every subcategory of the structure to form a word list
    wordlist = []
    for subcategory in wordlistData[partType]:
        subcategoryName = list(subcategory.keys())[0]
        subcategoryWordlist = subcategory[subcategoryName]
        for word in subcategoryWordlist:
            wordlist.append(word)
        
    # Select word in wordlist
    foundWord = False
    randomWord = ""
    while not foundWord:
        randomWord = random.choice(wordlist)
        if randomWord not in selectedWords: # Ensures word doesnt appear duplicate
            foundWord = True
    return randomWord



selectedStructures = []

for i in range(1):

    selectedStructure = getRandomStructure(selectedStructures)
    selectedStructures.append(selectedStructure)



    selectedWords = []
    for part in selectedStructure:
        selectedWords.append(getRandomWord(selectedWords, part))

    phrase = ' '.join(selectedWords)

    #print(phrase)


    print("Clue: " + infoData[selectedStructure[0]] + " ("+  str(len(selectedWords[0])) +" letters) / "  + infoData[selectedStructure[1]] + " ("+  str(len(selectedWords[1])) +" letters) / "  + infoData[selectedStructure[2]] + " ("+  str(len(selectedWords[2])) +" letters)" )
    #print("")

    
    pyperclip.copy(phrase)
    

#print(structureData)
#print(wordlistData)


'''

    TODO: Add logic to stop repeating words for 50 consecutive days



'''



    
