from tkinter.tix import Tree
from PIL import ImageChops, Image
import numpy as np
import pytesseract
import keyboard
import requests
import psutil
import uuid
import time
import csv
import sys
import os

pytesseract.pytesseract.tesseract_cmd = './components/Tesseract-OCR/tesseract'

inputDir = "./data/in/"
outDir = "./data/out/"
ssROW = "(Link) Screenshot"

imgOUT = inputDir + str(uuid.uuid4()) + ".png"
P4L = Image.open("./img/P4L.png")

debug = False
debugIMG = False
auto = True


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Check for system arguments
if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-v":
            debug = True
        if arg == "-m":
            auto = False
        if arg == "-h" or arg == "/?":
            
            print(f"{bcolors.BOLD}{bcolors.HEADER}HELP:{bcolors.ENDC}\n")
            print(f"{bcolors.HEADER}Arguments: {bcolors.OKCYAN} (-v = Verbose, -m = Manual verification using 'a' to accept and 'd' to decline, -h or /? = Display help) {bcolors.ENDC}")
            print(f"{bcolors.HEADER}Usage: {bcolors.OKCYAN} Place all images into the 'in' folder or place csv file for auto-download and processing of images. \n        All images will be sorted into 'Accept' or 'Decline' folders located in 'out' depending on premium status. {bcolors.ENDC}")
            exit()







def checkIMG(data):
    im = Image.open(data)

    width, height = im.size
    if width < 1920:
        im = im.resize((1920, 1080), Image.ANTIALIAS)
    width, height = im.size

    def getUser():

        left = width - 270
        top = 20
        right = width
        bottom = 45

        im1 = im.crop((left, top, right, bottom))
        im1 = im1.convert('L')
        # im1.show()

        user = pytesseract.image_to_string(im1).split()[0]
        return user

    def getPrem():
        prem = False

        left = width / 2 - 130
        # top = height / 2 - 430
        top = height / 2 - 300
        # right = width / 2 + 650
        right = width / 2 + 50
        bottom = height / 2 - 150

        im1 = im.crop((left, top, right, bottom))
        im1 = im1.convert('L')
        # im1.show()
        comp = ImageChops.difference(P4L, im1)
        # comp.show()
        # prem = pytesseract.image_to_string(im1).replace("\n", " ").strip()
        if pytesseract.image_to_string(im1).replace("\n", " ").strip() == "THANKS FOR BUYING PREMIUM FOR LIFE!":
            prem = True
        return prem
        
    if auto: data = getUser(), getPrem()
    if not auto:
        im.show()
        while True:
            try:
                if keyboard.is_pressed('a'):
                    data = True
                    for proc in psutil.process_iter():
                        if proc.name() == "display":
                            proc.kill()
                    break
                if keyboard.is_pressed('d'):
                    data = False
                    for proc in psutil.process_iter():
                        if proc.name() == "display":
                            proc.kill()
                    break
            except:
                return
    return data


def operateCSV(data):
    if debug: print(f"{bcolors.HEADER}READING: {bcolors.OKCYAN}{filename} {bcolors.ENDC}\n")
    file = open(data)
    csvreader = csv.DictReader(file)
    for row in csvreader:
        if debug: print(f"{bcolors.HEADER}DOWNLOADING: {bcolors.OKCYAN}{row[ssROW]} {bcolors.ENDC}")
        imgURL = row[ssROW]
        imgOUT = inputDir + str(uuid.uuid4()) + ".png"
        response = requests.get(imgURL)
        fileIMG = open(imgOUT, "wb")
        fileIMG.write(response.content)
        fileIMG.close
    file.close()
    time.sleep(1)
    dest = outDir + "Depleted.csv"
    os.replace(data, dest)
    print("\n")
    time.sleep(1)
    


if not os.path.isdir('./data/in'):
    os.mkdir('./data/in')
if not os.path.isdir('./data/out'):
    os.mkdir('./data/out/')
if not os.path.isdir('./data/out/Accept'):
    os.mkdir('./data/out/Accept')
if not os.path.isdir('./data/out/Decline'):
    os.mkdir('./data/out/Decline')





if not os.listdir(inputDir):
    print(f"{bcolors.FAIL}Warning: No files found.{bcolors.ENDC}")
    
for filename in os.listdir(inputDir):
    if filename.endswith(".csv"):
        data = os.path.join(inputDir, filename)
        operateCSV(data)
    else:
        print(f"{bcolors.OKCYAN}No CSV file found.{bcolors.ENDC}")

    
for filename in os.listdir(inputDir):
    if filename.endswith(".png"):
        if debug: print(f"{bcolors.HEADER}Analysing: {bcolors.OKCYAN}{filename} {bcolors.ENDC}")
        data = os.path.join(inputDir, filename)
        if not auto: 
            prem = checkIMG(data)
            user = filename.removesuffix(".png")
        if auto : user, prem = checkIMG(data)

        if prem:
            dest = outDir + "/accept/" + user + ".png"
            os.replace(data, dest)
            if debug: print(f"{bcolors.HEADER}RC22: {bcolors.OKCYAN}{user} {bcolors.HEADER}PREMIUM: {bcolors.OKGREEN}{prem} {bcolors.ENDC}\n")
            if not debug: print(f"{bcolors.HEADER}RC22: {bcolors.OKCYAN}{user} {bcolors.HEADER}PREMIUM: {bcolors.OKGREEN}{prem} {bcolors.ENDC}")
        else:
            dest = outDir + "/Decline/" + user + ".png"
            os.replace(data, dest)
            if debug: print(f"{bcolors.HEADER}RC22: {bcolors.FAIL}{user} {bcolors.HEADER}PREMIUM: {bcolors.FAIL}{prem} {bcolors.ENDC}\n")
            if not debug: print(f"{bcolors.HEADER}RC22: {bcolors.FAIL}{user} {bcolors.HEADER}PREMIUM: {bcolors.FAIL}{prem} {bcolors.ENDC}")
        

