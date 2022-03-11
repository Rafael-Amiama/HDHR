import os
import datetime  # Importing the datetime library
import time
from time import sleep 
import telepot   # Importing the telepot library
import glob
import shutil
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
import requests

def handle(msg):
	#now = datetime.datetime.now()
	#localtime = time.asctime( time.localtime(time.time()) )
	cwd = os.getcwd()
	chat_id = msg['chat']['id'] # Receiving the message from telegram
	command = msg['text']   # Getting text from the message
	#command = msg
	print ('Received:')
	print(command)
	print (chat_id)

	RawChan = ['7.1 WHDH','25.1 WFXT','4.1 WBZ-DT','56.1 WLVI','15.1 WBTS-CD','27.1 UniMas','5.1 WCVB','60.1 WNEU-DT','66.1 WUNI-DT','68.1 ION']
	cwd = os.getcwd()
	readDB = open(cwd + "\\" + "LocalDB.txt",'r')
	getDB = readDB.readline()
	ListDB = getDB.split(',')
	print(ListDB)
	LstIndex = 0
	AllTunerStatus = []
	num = 0
	for whichTuner in range(4):
		page = 'http://192.168.1.66/tuners.html'
		Tuner = requests.get(page).text.split("Tuner " + str(num) + " Channel</td><td>")[1].split('</td>')[0]
		AllTunerStatus.append(Tuner)
		num += 1
	print(AllTunerStatus)

	for x in ListDB:
		print('Looking at ' + (ListDB[LstIndex].split(' - ')[0]))
		if int((ListDB[LstIndex].split(' - ')[2])) > 0:
			print((ListDB[LstIndex].split(' - ')[0]) + " says DB is streaming.")
			
				
			if str(RawChan[LstIndex]) in AllTunerStatus:
				#print('Tuner value is ' + Tuner)
				print(RawChan[LstIndex] + ' is playing in a Tuner.')
				print('No need to reset DB.')
				#print("Tuner " + str(num) + " Not in use")
				#AllTunerStatus.append(RawChan[LstIndex])
				
			elif str(RawChan[LstIndex]) not in AllTunerStatus:
				print('elif ' + RawChan[LstIndex]+ ' is NOT playing in any Tuner.')
				print('DataBase User Count for this channel should be reset.')
				#print(ListDB[LstIndex])
				UpdateDB = ListDB[LstIndex][:-1] + '0'
				ListDB[LstIndex] = ListDB[LstIndex][:-1] + '0'
				print(getDB)
				print(str(ListDB).replace("', '",",")[2:-2])
				My_variable = str(ListDB).replace("', '",",")[2:-2]
				write2File = open(cwd + "\\" + "LocalDB.txt","w") # "a" means append to the end of the file. "w" over writes the entire file with new input.
				write2File.write (My_variable), # this comma at the end prevents from creating a new line inside the text file.
				write2File.close()
				
				#print(UpdateDB)
				#AllTunerStatus.append('empty')
				#print('Tuner value is ' + Tuner)
				#print(ListDB[0])
				#print (Tuner)
			#print (Tuner)
				
		else:
			print((ListDB[LstIndex].split(' - ')[0]) + ' DB is at 0\n')

		LstIndex += 1
	




	

	if command in ('WHDH','FOX','CBS','CW','NBC','Unimas','ABC','Telemundo','Univision','ION'):
		print ("Start thread")
		readDB = open(cwd + "\\" + "LocalDB.txt",'r')
		getDB = readDB.readline()
		ListDB = getDB.split(',')
		strmInUse = 0
		for usrCount in ListDB:
			if command in ListDB[strmInUse]:
				ChanUsrCount = ListDB[strmInUse].split(' - ')[2]
				print (ChanUsrCount)
				if int(ChanUsrCount) >= 1:
					print ("Channel is already ON")
					print ("ADD 1 user to stream user count.")
					newCount = int(ChanUsrCount) + 1
					ListDB[strmInUse] = (command + " - " + ListDB[strmInUse].split(' - ')[1] + " - " + str(newCount))
					writeDB = open(cwd + "\\" + "LocalDB.txt",'w')
					writeDB.write(str(ListDB).replace('[','').replace(']','').replace("', '" , ",")[1:-1])
					writeDB.close()
					break
				elif int(ChanUsrCount) == 0:
					print ("Channel Stream is OFF")
					print ("Start channel stream.")
					os.startfile("C:\\Program Files (x86)\\ARM Software\\MacroMaker\\" + command + ".lnk")
					newCount = int(ChanUsrCount) + 1
					ListDB[strmInUse] = (command + " - " + ListDB[strmInUse].split(' - ')[1] + " - " + str(newCount))
					writeDB = open(cwd + "\\" + "LocalDB.txt",'w')
					writeDB.write(str(ListDB).replace('[','').replace(']','').replace("', '" , ",")[1:-1])
					writeDB.close()
					break
			else:
				strmInUse += 1

	elif command in ('stopWHDH','stopFOX','stopCBS','stopCW','stopNBC','stopUnimas','stopABC','stopTelemundo','stopUnivision','stopION'):
		print ("Stop thread")
		readDB = open(cwd + "\\" + "LocalDB.txt",'r')
		getDB = readDB.readline()
		ListDB = getDB.split(',')
		strmInUse = 0
		for usrCount in ListDB:
			print (ListDB[strmInUse])

			if command[4:] in ListDB[strmInUse]:
				ChanUsrCount = ListDB[strmInUse].split(' - ')[2]
				print (ChanUsrCount)
				if int(ChanUsrCount) == 1:
					print ("ONLY 1 User")
					print ("Subtract 1 user to stream user count.")
					print ("Stop channel stream.")
					os.startfile("C:\\Program Files (x86)\\ARM Software\\MacroMaker\\" + command + ".lnk")
					newCount = int(ChanUsrCount) - 1
					ListDB[strmInUse] = (command[4:] + " - " + ListDB[strmInUse].split(' - ')[1] + " - " + str(newCount))
					writeDB = open(cwd + "\\" + "LocalDB.txt",'w')
					writeDB.write(str(ListDB).replace('[','').replace(']','').replace("', '" , ",")[1:-1])
					writeDB.close()
					break
				elif int(ChanUsrCount) > 1:
					print ("Multiple Users")
					print ("Dont Stop channel stream.")
					newCount = int(ChanUsrCount) - 1
					ListDB[strmInUse] = (command[4:] + " - " + ListDB[strmInUse].split(' - ')[1] + " - " + str(newCount))
					writeDB = open(cwd + "\\" + "LocalDB.txt",'w')
					writeDB.write(str(ListDB).replace('[','').replace(']','').replace("', '" , ",")[1:-1])
					writeDB.close()
					break
			else:
				strmInUse += 1

#var = "stopABC"
#handle(var)
 

bot = telepot.Bot("xxxxxxxxxxxxxxxx")
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(5)


