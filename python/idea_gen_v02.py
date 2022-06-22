import json
import random
import math
from colorama import Fore, Back, Style, init
from termcolor import colored
import requests


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


def getWordsFromURL(url):
    return requests.get(url).text.split("\n")

def getOnlineList():
    onlineList = []


    onlineList += getWordsFromURL("https://raw.githubusercontent.com/sroberts/wordlists/master/nouns.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/sroberts/wordlists/master/adjectives.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/hugsy/stuff/main/random-word/english-nouns.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Nouns-Common-Audited-Len-3-6.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Adjectives-Common-Audited-Len-3-6.txt")
    onlineList += getWordsFromURL("https://gist.githubusercontent.com/creikey/42d23d1eec6d764e8a1d9fe7e56915c6/raw/b07de0068850166378bc3b008f9b655ef169d354/top-1000-nouns.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/martinsvoboda/nouns/master/nouns/en_nouns.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/glitchdotcom/friendly-words/master/words/objects.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/glitchdotcom/friendly-words/master/words/collections.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/glitchdotcom/friendly-words/master/words/predicates.txt")
    onlineList += getWordsFromURL("https://raw.githubusercontent.com/glitchdotcom/friendly-words/master/words/teams.txt")
    onlineList += getWordsFromURL("http://www.desiquintans.com/downloads/nounlist/nounlist.txt")
   # onlineList += getWordsFromURL("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
    

    #onlineList += getWordsFromURL("https://gist.githubusercontent.com/Rhomboid/8a61864a5fe1fca3013ba94ed0be9e83/raw/17cc35afc904e36a8141053636a96fdf9729fd0a/nouns.txt")    

    return onlineList

    

def randomiseOrder(myList):
    random.shuffle(myList)

def selectWeightedRandom(data):
    return random.choices(population = data["values"], weights = data["weights"])[0]

SHEETRANGE_EASY_OBJ = 'A3:A5000'
SHEETRANGE_EASY_DES = 'B3:B5000'
SHEETRANGE_HARD_OBJ = 'C3:C5000'
SHEETRANGE_HARD_DES = 'D3:D5000'

PREPROCESSED_EASY_OBJ = getGoogleSheetsValues(SHEETRANGE_EASY_OBJ)
PREPROCESSED_EASY_DES = getGoogleSheetsValues(SHEETRANGE_EASY_DES)
PREPROCESSED_HARD_OBJ = getGoogleSheetsValues(SHEETRANGE_HARD_OBJ)
PREPROCESSED_HARD_DES = getGoogleSheetsValues(SHEETRANGE_HARD_DES)

PREPROCESSED_EASY = PREPROCESSED_EASY_OBJ + PREPROCESSED_EASY_DES
PREPROCESSED_HARD = PREPROCESSED_HARD_OBJ + PREPROCESSED_HARD_DES
PREPROCESSED = PREPROCESSED_EASY + PREPROCESSED_HARD + getOnlineList()
randomiseOrder(PREPROCESSED)











def getWordsWithLettersRemaining(lettersRemaining, wordList, currentPhrase):
    filteredWordList = []
    for word in wordList:
        letterCount = len(word)
        usedLetters = 0
        for letter in word:
            if letter == " ":
                continue
            if letter in currentPhrase:
                usedLetters += 1
        if letterCount - usedLetters == lettersRemaining:
            filteredWordList.append(word)
    return filteredWordList


def getWordsWithLettersRevealed(lettersToReveal, wordList, currentPhrase):
    filteredWordList = []
    for word in wordList:
        letterCount = len(word)
        revealedLetters = 0
        for letter in word:
            if letter == " ":
                continue
            if letter in currentPhrase:
                revealedLetters += 1
        if revealedLetters == lettersToReveal:
            filteredWordList.append(word)
    return filteredWordList


def getWordsCompleted(wordList, currentPhrase):
    filteredWordList = []
    for word in wordList:
        isCompleted = True
        for letter in word:
            if letter == " ":
                continue
            if letter not in currentPhrase:
                isCompleted = False
        if isCompleted:
            filteredWordList.append(word)
    return filteredWordList

def letterToTiny (letter):
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[ord(letter)-97]#"ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"[ord(letter)-97]

def getWordListString(wordList, currentPhrase):
    wordString = ""
    for word in wordList:
        formattedWord = ""
        formattedWord += word
        revealedWord = ""
        for letter in word:
            if letter in currentPhrase or letter == " ":
                revealedWord += letter
            else:
                revealedWord += "_"
        formattedWord += "(" + revealedWord +")"
        wordString += formattedWord + " | "
    return wordString

def getCompletedString(wordList):
    wordString = ""
    for word in wordList:
        wordString += word + " "
    return wordString

       
def getUsedLettersString(currentPhrase):
    usedLetters = ""
    unusedLetters = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for alphabetLetter in alphabet:
        for letter in currentPhrase:
            if letter not in usedLetters:
                usedLetters += letter

    for alphabetLetter in alphabet:
        if alphabetLetter not in usedLetters:
            unusedLetters += alphabetLetter

    
            
            
    wordString = str(usedLetters) + "  ///  " + str(unusedLetters)
    return wordString
 


#MODE = 
MODE = "REVEALED"  # "REMAINING"

DISPLAY_ORDER = "FORWARDS"#"BACKWARDS" # "FORWARDS"

def displayWordlist(wordList, currentPhrase):

    displayOrderData = []
    if DISPLAY_ORDER == "BACKWARDS":
        displayOrderData = [20, -1, -1]
    elif DISPLAY_ORDER == "FORWARDS":
        displayOrderData = [0, 20, 1]
    
    for i in range(displayOrderData[0], displayOrderData[1], displayOrderData[2]):
        if MODE == "REMAINING":
            filteredList = getWordsWithLettersRemaining(i, wordList, currentPhrase)
        if MODE == "REVEALED":
            filteredList = getWordsWithLettersRevealed(i, wordList, currentPhrase)
        if len(filteredList) == 0:
            continue
        wordString = getWordListString(filteredList, currentPhrase)
        if MODE == "REMAINING":
            print(str(i)+"x left: " + wordString)
        if MODE == "REVEALED":
            print(str(i)+"x revealed: " + wordString)
        print("")

    completedList = getWordsCompleted(wordList, currentPhrase)
    print("\nCOMPLETED: " + getCompletedString(completedList))
    print("\nUSED: " + getUsedLettersString(currentPhrase))
    print("")
        

def displayAllWordlists(currentPhrase):
    print("-"*3000)

    randomiseOrder(PREPROCESSED)
    
    displayWordlist(PREPROCESSED[0:800], currentPhrase)



currentPhrase = ""

while True:

    displayAllWordlists(currentPhrase)
    print("Current phrase: " + currentPhrase)
    enteredWord = input("> ")
    if enteredWord == "-":
        currentPhrase = ""
    elif currentPhrase == "":
        currentPhrase = enteredWord
    else:
        currentPhrase += " " + enteredWord



print(PREPROCESSED_EASY)


