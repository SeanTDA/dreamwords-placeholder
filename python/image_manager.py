
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
    
  stromboli = stromboli.replace("{","")
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

  stromboli = stromboli.replace("{","")
  return stromboli


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
    
  




def getDirectories():
  preprocessedFolder = input("Preprocessed Folder: ")
  convertedFolder = input("Converted Folder: ")

  currentDir = os.path.dirname(os.getcwd())

  if preprocessedFolder == "":
    preprocessedFolder = "01_preprocessed"
    
  if convertedFolder == "":
    convertedFolder = "02_converted"
    

  preprocessedFolder = currentDir + "/" + preprocessedFolder
  convertedFolder = currentDir + "/" + convertedFolder
  
  print("Set Preprocessed Folder to " + preprocessedFolder)
  print("Set Converted Folder to " + convertedFolder)
  
  return {
    "preprocessedDir": preprocessedFolder,
    "convertedDir": convertedFolder
    }
  


def getDayCount(imageDir):
  dayCount = 0
  for file in os.listdir(imageDir):
    if "metadata" in file:
      dayCount += 1
  return dayCount




def processFiles (preprocessedDir, convertedDir, initialDay, runMode):
  currentDay = initialDay
  for file in os.listdir(preprocessedDir):

    fileName = str(file)

    metadataCode = getMetadataCodeFromDay(currentDay)
    imageCode = getImageCodeFromDay(currentDay)

    metadataFileURL = convertedDir + "/metadata_" + metadataCode + ".json"
    imageFileURL = convertedDir + "/image_" + imageCode + ".png"


    metaStringData = (" ".join(fileName.split("_")[1:]).replace(".png","")).strip().split("X")

    solution = metaStringData[0]

    print("Processing " + solution + "  " + metadataCode)
    
    if len(metaStringData) > 1:
      hiddenWords = metaStringData[1]
    else:
      hiddenWords = ""
    

    # Create Metadata File
    metadata = {"solution": solution, "hiddenWords": hiddenWords}
    with open(metadataFileURL, 'w') as newMetadataFile:
      json.dump(metadata, newMetadataFile)

    if (runMode == 0):
      # Copy Image (with new name)
      shutil.copy(preprocessedDir + "/" + fileName, imageFileURL)
      #shutil.move(preprocessedDir + "/" + fileName, convertedDir + "/" + fileName
    currentDay += 1







directories = getDirectories()


preprocessedDir = directories['preprocessedDir']
convertedDir = directories['convertedDir']

defaultDay = getDayCount(convertedDir)
initialDay = input ("Initial Day? ("+str(defaultDay)+"): ")
if initialDay == "":
  initialDay = defaultDay
initialDay = int(initialDay)

runMode = input("Run Mode (0 = normal, 1 = only meta) ")
if runMode == "":
  runMode = "0"
runMode = int(runMode)

processFiles(preprocessedDir, convertedDir, initialDay, runMode)




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
  

  
  
  
