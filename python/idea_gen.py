import json
import random
import math


# Google Sheets Wrapper

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
def getGoogleSheetsCreds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
SPREADSHEET_ID = '1-6q1Et3PLvyuxVtvpFECuRBOOALKGb_4-I7hYR_FXEg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
googleSheetsCreds = getGoogleSheetsCreds()
googleSheetsService = build('sheets', 'v4', credentials=googleSheetsCreds)
spreadsheet = googleSheetsService.spreadsheets()


def getGoogleSheetsValues(valueRange):
    global spreadsheet
    result = spreadsheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=valueRange).execute()
    rawValues = result.get('values', [])
    values = []
    for row in rawValues:
        values.append(row[0])
    return values



SHEETRANGE_EASY_OBJ = 'A3:A500'
SHEETRANGE_EASY_DES = 'B3:B500'
SHEETRANGE_HARD_OBJ = 'C3:C500'
SHEETRANGE_HARD_DES = 'D3:D500'

PREPROCESSED_EASY_OBJ = getGoogleSheetsValues(SHEETRANGE_EASY_OBJ)
PREPROCESSED_EASY_DES = getGoogleSheetsValues(SHEETRANGE_EASY_DES)
PREPROCESSED_HARD_OBJ = getGoogleSheetsValues(SHEETRANGE_HARD_OBJ)
PREPROCESSED_HARD_DES = getGoogleSheetsValues(SHEETRANGE_HARD_DES)


# https://docs.google.com/spreadsheets/d/1-6q1Et3PLvyuxVtvpFECuRBOOALKGb_4-I7hYR_FXEg/edit?usp=sharing


def randomiseOrder(myList):
    random.shuffle(myList)

def selectWeightedRandom(data):
    return random.choices(population = data["values"], weights = data["weights"])[0]








def getStructure(structuresData):
    wordCount = selectWeightedRandom(structuresData["LEN"])
    wordCommonalities = selectWeightedRandom(structuresData["COM"][str(wordCount)])
    wordTypes =  selectWeightedRandom(structuresData["TYP"][str(wordCount)])
    wordSizes = selectWeightedRandom(structuresData["SIZ"][str(wordCount)])
    

    randomiseOrder(wordCommonalities)
    randomiseOrder(wordSizes)

    structure = []
    for wordIndex in range(wordCount):        
        structure.append({
            "COM": wordCommonalities[wordIndex],
            "TYP": wordTypes[wordIndex],
            "SIZ": wordSizes[wordIndex]
            })

    return structure
    

def getIsEasySolved(structure):
    isEasySolved = True
    for wordStructure in structure:
        if wordStructure["COM"] == "EASY":
            if wordStructure["SOLVED_WORD"] == '':
                isEasySolved = False
    return isEasySolved



def solveWord(wordbankData, wordStructure, lettersUsed):
    wordCommonality = wordStructure['COM']
    wordType = wordStructure["TYP"]
    wordSize = wordStructure['SIZ']


    
    #wordPool = wordbankData[wordCommonality][wordType] # Local Version

    sheetRange = ""
    wordPool = []
    if wordCommonality == "EASY":
        if wordType == "OBJ":
            wordPool = PREPROCESSED_EASY_OBJ
        elif wordType == "DES":
            wordPool = PREPROCESSED_EASY_DES
    elif wordCommonality == "HARD":
        if wordType == "OBJ":
            wordPool = PREPROCESSED_HARD_OBJ
        elif wordType == "DES":
            wordPool = PREPROCESSED_HARD_DES
    

    # Filter by word length
    wordLengthFilter = (0,0)
    if wordCommonality == "EASY":
        if wordSize == "SHORT":
            wordLengthFilter = (1,4)
        elif wordSize == "LONG":
            wordLengthFilter = (5,99)
    elif wordCommonality == "HARD":
        if wordSize == "SHORT":
            wordLengthFilter = (1,6)
        elif wordSize == "LONG":
            wordLengthFilter = (7,99)
       
    wordPoolFilteredBySize = [x for x in wordPool if len(x) >= wordLengthFilter[0] and len(x) <= wordLengthFilter[1]]

    print("Attempting to find a word with structure : " + str(wordStructure))
    
    # Attempt to find word 50 times before giving up
    for i in range(50):

        #Pick random
        randomWordInPool = random.choice(wordPoolFilteredBySize)

        isWordValid = True

        # Tally number of letters in this random word that have been previously used
        sharedLettersInThisRandomWord = 0
        for letter in randomWordInPool:
            if letter in lettersUsed:
                sharedLettersInThisRandomWord += 1
                
                    
        # Disable 'isWordValid' if there are not enough shared letters
        if wordCommonality == "HARD":
            print("Common Letters in " + randomWordInPool + " = " + str(sharedLettersInThisRandomWord))
            lettersToPassTest = math.floor(float(len(randomWordInPool)) * 0.4)  #0.35 before
            print("To pass test: " + str(lettersToPassTest))
            if sharedLettersInThisRandomWord < lettersToPassTest:
                isWordValid = False

        

        if isWordValid:
            return randomWordInPool
        

    
    #print(wordCommonality + " " + wordType + " " + wordSize + " :  " + str( wordPoolFilteredBySize))
    

    return "[NULL]"




with open("ideas_gen_data.json") as jsonFile:
    allData = json.load(jsonFile)

structuresData = allData["structures"]
wordbankData = allData["wordbank"]





def solveWords():
    structure = getStructure(structuresData)


    # Cycle until all words have been solved
    solvedWordCount = 0
    for wordStructureIndex in range(len(structure)):
        structure[wordStructureIndex]["SOLVED_WORD"] = ""

    lettersUsed = []
    while solvedWordCount < len(structure):

        # 1. Pre-test (each stage): Check if there are 'easy'
        isEasySolved = getIsEasySolved(structure)

        print ("isEasySolved?  " + str(isEasySolved))

        
        for wordStructureIndex in range(len(structure)):

            # 2. Solve Commons First
            if not isEasySolved:
                if structure[wordStructureIndex]["COM"] == "EASY":

                    solvedWord = "[NULL]"
                    while solvedWord == "[NULL]":
                        solvedWord = solveWord(wordbankData, structure[wordStructureIndex], lettersUsed)

                    print("Solved: " + solvedWord)
                    structure[wordStructureIndex]["SOLVED_WORD"] = solvedWord
                    for letter in solvedWord:
                        lettersUsed.append(letter)
                    
                    solvedWordCount += 1

            # Now Solve Harder
            else:
                if structure[wordStructureIndex]["COM"] == "HARD":

                    solvedWord = "[NULL]"
                    while solvedWord == "[NULL]":
                        solvedWord = solveWord(wordbankData, structure[wordStructureIndex], lettersUsed)
                        
                    print("Solved: " + solvedWord)
                    structure[wordStructureIndex]["SOLVED_WORD"] = solvedWord
                    for letter in solvedWord:
                        lettersUsed.append(letter)
                    
                    solvedWordCount += 1
            



    words = []
    for wordStructure in structure:
        words.append(wordStructure["SOLVED_WORD"])
    randomiseOrder(words)
    return {"words":words, "structure": structure}

                

for i in range(50):
    solvedWords = solveWords()
    print("")
    print("")
    print("WORD: " + str(solvedWords["words"]))
    print("STRUCTURE: " + str(solvedWords["structure"]))
    print("")
    print("")


    




# Finally, randomise words
