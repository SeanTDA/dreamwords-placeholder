

def getMetadataURL(i):
  i += 15
  doopsie = chr((i%15)+97)
  lottie = (i*6) % 12
  dollop = chr(((i*2) % 10)+105)
  sam = 500 - (round((i+569.3)*46.85) % 105)
  danthony = round((67.5+i) * 978.54) % 101
  greg = round(7+((i*12.3)%5.5)+12327)%56781
  dro = chr((i%9)+107)+chr((i%12)+108)+chr(103+(i%17))
  pebble = round(i*6.14159) % 9684
  plub = round(i*11.93) % 2680
  stromboli =  str(lottie) + str(greg) + dro + str(pebble) + str(plub) + dollop + str(sam) + str(danthony)
  print(len(stromboli))
  if len(stromboli) % 2 == 1:
    stromboli = doopsie + stromboli
  return stromboli


def getImageURL(i):
  i += 33
  doopsie = chr((i%26)+97)
  lottie = (i*5) % 16
  dollop = chr(((i*2) % 19)+105)
  sam = 500 - (round((i+19.3)*46.85) % 305)
  danthony = round((67.5+i) * 978.54) % 101
  greg = (7+i+12327)%56781
  dro = chr((i%9)+107)+chr((i%12)+108)+chr(103+(i%17))
  pebble = round(i*3.14159) % 9684
  plub = round(i*18.93) % 1680
  stromboli = str(lottie) + dollop + str(sam) + str(danthony) + str(greg) + dro + str(pebble) + str(plub)
  if len(stromboli) % 2 == 0:
    stromboli = doopsie + stromboli
  return stromboli


for i in range(10000000):
  print("")
  print("Day " + str(i))
  print("Image :")
  print("image_"+getImageURL(i))
  print("Metadata :")
  print("metadata_"+getMetadataURL(i))
  print("")

  
  
  
