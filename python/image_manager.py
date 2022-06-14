
import os, shutil
import json
import math

def getMetadataCodeFromDay(dayIndex):
  i = dayIndex + 15
  doopsie = chr((i%15)+97)
  lottie = (i*6) % 12
  dollop = chr(((i*2) % 10)+105)
  sam = 500 - (math.floor((i+569.3)*46.85) % 105)
  danthony = math.floor((67.5+i) * 978.54) % 101
  greg = math.floor(7+((i*12.3)%5.5)+12327)%56781
  dro = chr((i%9)+107)+chr((i%12)+108)+chr(103+(i%17))
  pebble = math.floor(i*6.14159) % 9684
  plub = math.floor(i*11.93) % 2680
  stromboli =  str(lottie) + str(greg) + dro + str(pebble) + str(plub) + dollop + str(sam) + str(danthony)
  if len(stromboli) % 2 == 1:
    stromboli = doopsie + stromboli
  return stromboli


def getImageCodeFromDay(dayIndex):
  i = dayIndex + 33
  doopsie = chr((i%26)+97)
  lottie = (i*5) % 16
  dollop = chr(((i*2) % 19)+105)
  sam = 500 - (math.floor((i+19.3)*46.85) % 305)
  danthony = math.floor((67.5+i) * 978.54) % 101
  greg = (7+i+12327)%56781
  dro = chr((i%9)+107)+chr((i%12)+108)+chr(103+(i%17))
  pebble = math.floor(i*3.14159) % 9684
  plub = math.floor(i*18.93) % 1680
  stromboli = str(lottie) + dollop + str(sam) + str(danthony) + str(greg) + dro + str(pebble) + str(plub)
  if len(stromboli) % 2 == 0:
    stromboli = doopsie + stromboli

  stromboli.replace("{","")
  return stromboli





def getDirectories():
  preprocessedFolder = input("Preprocessed Folder: ")
  preprocessedConvertedFolder = input("Preprocessed Converted Folder: ")
  imageFolder = input("Image Folder: ")

  currentDir = os.path.dirname(os.getcwd())

  if preprocessedFolder == "":
    preprocessedFolder = "01_preprocessed"
    
  if preprocessedConvertedFolder == "":
    preprocessedConvertedFolder = "02_preprocessed_converted"
    
  if imageFolder == "":
    imageFolder = "files"

  preprocessedFolder = currentDir + "/" + preprocessedFolder
  preprocessedConvertedFolder = currentDir + "/" + preprocessedConvertedFolder
  imageFolder = currentDir + "/" + imageFolder
  
  print("Set Preprocessed Folder to " + preprocessedFolder)
  print("Set Preprocessed Converted Folder to " + preprocessedConvertedFolder)
  print("Set Image Folder to " + imageFolder)

  return {
    "preprocessedDir": preprocessedFolder,
    "preprocessedConvertedDir": preprocessedConvertedFolder,
    "imageDir": imageFolder
    }
  


def getDayCount(imageDir):
  dayCount = 0
  for file in os.listdir(imageDir):
    if "metadata" in file:
      dayCount += 1
  return dayCount




def processFiles (preprocessedDir, preprocessedConvertedDir, initialDay):
  currentDay = initialDay
  for file in os.listdir(preprocessedDir):

    fileName = str(file)

    metadataCode = getMetadataCodeFromDay(currentDay)
    imageCode = getImageCodeFromDay(currentDay)

    metadataFileURL = imageDir + "/metadata_" + metadataCode + ".json"
    imageFileURL = imageDir + "/image_" + imageCode + ".png"


    solution = (" ".join(fileName.split("_")[1:]).replace(".png","")).strip()
    print(solution)

    # Create Metadata File
    metadata = {"solution": solution}
    with open(metadataFileURL, 'w') as newMetadataFile:
      json.dump(metadata, newMetadataFile)

    
    # Copy Image (with new name)
    shutil.copy(preprocessedDir + "/" + fileName, imageFileURL)
    shutil.move(preprocessedDir + "/" + fileName, preprocessedConvertedDir + "/" + fileName)
    
    currentDay += 1



directories = getDirectories()

imageDir = directories['imageDir']
preprocessedDir = directories['preprocessedDir']
preprocessedConvertedDir = directories['preprocessedConvertedDir']

defaultDay = getDayCount(imageDir)
initialDay = input ("Initial Day? ("+str(defaultDay)+"): ")
if initialDay == "":
  initialDay = defaultDay

processFiles(preprocessedDir, preprocessedConvertedDir, initialDay)

  
#print("metadata_"+getMetadataCodeFromDay(15))
  
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
  

  
  
  
