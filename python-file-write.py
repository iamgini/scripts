from datetime import datetime
dateTimeObj = datetime.now()
print(dateTimeObj)

daeTimeString = dateTimeObj.strftime("%d-%b-%Y_%H-%M-%S_%f")

f = open("demofile2.txt", "a")
f.write( "\n" + daeTimeString + " Now the file has more content!")
f.close()

#open and read the file after the appending:
f = open("demofile2.txt", "r")
print(f.read())