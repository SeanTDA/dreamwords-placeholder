
import os, shutil
import re
import json
import math
import tkinter as tk
from tkinter import filedialog
import autocorrect



def getMetadataCodeFromDay(dayIndex):
  return "md"+str(dayIndex)


def getImageCodeFromDay(dayIndex):
  return "i"+str(dayIndex)

def getDayFromMetadataCode(metadataCode):
  for i in range(100000):
    if getMetadataCodeFromDay(i) == metadataCode:
      return i
  print("Error ! No day found for " + metadataCode)
  return -1
    
def getDayFromImageCode(imageCode):
  for i in range(100000):
    if getImageCodeFromDay(i) == imageCode:
      return i
  print("Error ! No day found for " + imageCode)
  return -1
    

def get_credit_entry(file_path, number):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data[str(number)]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except KeyError:
        print(f"Key not found: {number}")
        return None
  



def getDayCount(imageDir):
  dayCount = 0
  for file in os.listdir(imageDir):
    if "metadata" in file:
      dayCount += 1
  return dayCount

def spellcheck(text):
  auto = autocorrect.Speller()
  words = text.split()
  for i, word in enumerate(words):
    corrected_word = auto(word)
    if word != corrected_word:
      print(f"!!!!! - Incorrect spelling: {word} (should be {corrected_word})")
      input("Continue? ")
      





def processFiles (preprocessedDir, convertedDir, initialDay, runMode):
  currentDay = initialDay
  for file in os.listdir(preprocessedDir):

    fileName = str(file)

    metadataCode = getMetadataCodeFromDay(currentDay)
    imageCode = getImageCodeFromDay(currentDay)

    metadataFileURL = convertedDir + "/metadata_" + metadataCode + ".json"
    imageFileURL = convertedDir + "/image_" + imageCode + ".png"


    fileNameStripped = fileName.replace(".png","")
    imageCountPart =  " ".join([num for num in fileNameStripped.split("X")[1]]) if ("X" in fileNameStripped) else ""
    solutionPart = " ".join((fileNameStripped.split("X")[0]).split("_")[1:]) if "X" in fileNameStripped else " ".join(fileNameStripped.split("_")[1:])



    hintGoodLetters = ""
    hintBadLetters = ""
    hintHiddenLetters = ""


    if fileNameStripped.count("X") >= 2:
        hintGoodLetters = fileNameStripped.split("X")[2]

    if fileNameStripped.count("X") >= 3:
        hintBadLetters = fileNameStripped.split("X")[3]

    if fileNameStripped.count("X") >= 4:
        hintHiddenLetters = fileNameStripped.split("X")[4]

    creditData = get_credit_entry(preprocessedDir+"/credits.json", currentDay)
    
    #inspired =
    print(creditData)
    inspiredInfo = ""
    creditsInfo = ""
    if creditData is not None:
      inspiredInfo = creditData["inspired"]
      creditsInfo = creditData["credits"]



    metaStringData = {"solution": solutionPart,
                      "imageCount": imageCountPart,
                      "hintGoodLetters": hintGoodLetters,
                      "hintBadLetters": hintBadLetters,
                      "hintHiddenLetters":hintHiddenLetters,
                      "inspired":inspiredInfo,
                      "credits":creditsInfo
                      }



    solution = metaStringData["solution"]
    

    #print("Processing " + solution + " " + imageCode + " " + metadataCode)
    print("Metadata: " +str( metaStringData))

  
    
    for letter in hintBadLetters:
      if letter in solutionPart:
        input("Error! Wrong letter in solution")

              
    spellcheck(solution)

    currentDay += 1

    

    
    # Create Metadata File
    metadata = {"solution": metaStringData["solution"], 
                "hiddenWords": "", 
                "imageCount":  metaStringData["imageCount"], 
                "hintGoodLetters":  metaStringData["hintGoodLetters"], 
                "hintBadLetters":  metaStringData["hintBadLetters"],
                "hintHiddenLetters":metaStringData["hintHiddenLetters"],
                "inspired":metaStringData["inspired"],
                "credits":metaStringData["credits"]}
    
    with open(metadataFileURL, 'w') as newMetadataFile:
      json.dump(metadata, newMetadataFile)

    if (runMode == 0):
      # Copy Image (with new name)
      shutil.copy(preprocessedDir + "/" + fileName, imageFileURL)
    
    





root = tk.Tk()
root.withdraw()




preprocessedDir = filedialog.askdirectory(parent=root, title="Input Folder")
convertedDir = filedialog.askdirectory(parent=root, title="Output Folder")


defaultDay = getDayCount(preprocessedDir)
initialDay = input ("Initial Day? ("+str(defaultDay)+"): ")
if initialDay == "":
  initialDay = defaultDay
initialDay = int(initialDay)


runMode = 0

processFiles(preprocessedDir, convertedDir, initialDay, runMode)

print("- Done -")




#print(getDayFromImageCode("7n3786512441swl336345"))



'''



print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
print("")
for i in range(10000000):
  print("")
  print("Day " + str(i))
  print("Image :")
  print("image_"+getImageCodeFromDay(i))
  print("Metadata :")
  print("metadata_"+getMetadataCodeFromDay(i))
  print("")

'''


  
#shutil.move(preprocessedDir + "/" + fileName, convertedDir + "/" + fileName
  
  
