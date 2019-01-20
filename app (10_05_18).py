import sys
import os
import platform
import sys
import subprocess
import threading
from PyQt4.QtGui import QWidget, QPushButton, QLineEdit, QMessageBox, QApplication
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import*
from PyQt4.QtGui import*
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from openpyxl import Workbook
import main
import user
import previous
import New
import intermediate
import intermediate_settings
import continous
import continous_settings
import variable
import variable_settings
#import settings
import serial
import design6
import time


datapath = "/home/pi/Design6/"
#ser = serial.Serial()
#port = "/dev/ttyUSB0"
#ser.port = "/dev/ttyUSB0"
#baudrate = 115200

wb = Workbook()
ws1 = wb.active

#global malegender
malegender = False
femalegender= False
othergender= False
Gender = ""

Inter_Pressure = 0
Inter_Pump_on = 0
Inter_Pump_off = 0
Inter_cycle = 0

cont_pressuretext = 0 
cont_pumpon_inc = 0

temp_inter_cycle = 0

reading = ""
year = 0
month = 0
date = 0

hour = 0
minute = 0
sec = 0

gender_tuple = ('Male','Female','Others')
#global Target_Pressure
ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=1)
'''
try:
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    #exit()
'''
def read_from_port(ser):
	      global GlobalSerIn
              global year ,month ,date
              global hour ,minute ,sec 
	      global reading 
              global dateTimeEdit
              while True:
		        #ser.flushInput()
                        #ser.flushOutput()
			data = ""
			datedata = ""
			timedata = ""
			
                        reading = ser.readline()
		        data = reading
		    #time.sleep(3),
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime(year,month,date,hour,minute,sec)
                                                
			print "Data Recieved"
                        print(data)
                        if data[:5] == 'Date+':
	                   datedata = data
			   #print(map(int, datedata.split(".")))
			   print(datedata.split("+"))
			   #date = int(datedata[6:8])
	       		   #month = int(datedata[9:10])
	                   #year = int(datedata[11:15])
		           date = int(datedata.split("+")[1])
			   month = int(datedata.split("+")[2])
			   year = int(datedata.split("+")[3])
		           #print year

	                if data[:5] == 'Time+':
	                   timedata = data
                           print("TIME")
			   print(timedata.split("+"))
                           #print data[6:8]
	                   hour = int(timedata.split("+")[1])
	                   minute = int(timedata.split("+")[2])
	                   sec = int(timedata.split("+")[3])


			if data[:6] == 'Pi:OFF':
			   print("OFF")
                           #os.system("vcgencmd display_power 0")
 
                        if data[:5] == 'Pi:ON':
			   print("ON")
                           #os.system("vcgencmd display_power 1")

                        
#thread = threading.Thread(target=read_from_port, args=(ser,))
#thread.start() 



class KeyboardLineEdit(QLineEdit):
    def __init__(self,parent=None):
        super(KeyboardLineEdit,self).__init__(parent)

    def focusInEvent(self, event):
        try:
            print("Run Florence")
            #subprocess.Popen(["matchbox-keyboard ","extended"])
	    subprocess.Popen(["florence"])
            
        except (OSError, IOError) as e:
            pass

    def focusOutEvent(self,e):
        subprocess.Popen(["killall","florence"])
        print("Kill Florence")


class mainApp(QtGui.QMainWindow, main.Ui_MainWindow):
    		def __init__(self):
		#def __init__(self, parent=None):	        		
			super(self.__class__, self).__init__()
        		#super(userApp, self).__init__(parent)
			self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
		        self.timer_main = QtCore.QTimer()
        		self.timer_main.timeout.connect(self.user_app)
			self.userapp = userApp()
        		self.timer_main.start(2000)


		def user_app(self):
			self.close()                     
    			self.userapp.show()
			self.timer_main.stop()
			
class userApp(QtGui.QMainWindow, user.Ui_MainWindow):
    		def __init__(self):
		#def __init__(self, parent=None):	        		
			super(self.__class__, self).__init__()
        		#super(userApp, self).__init__(parent)
			self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
			#global userapp

    		        #self.userapp.show()  
			self.previousButton.clicked.connect(self.previous_user)
			#self.previousapp = previousApp()
			

			self.newButton.clicked.connect(self.new_user)
			self.newapp = newApp()
			

		def previous_user(self):
		        print('previous')
			#self.close()
			#self.previousapp.show()

		def new_user(self):
		        print('new')
			
                        #self.setOpacity(0.5)			
			self.close()
        		#QTimer.singleShot(1000, self.fade)
			self.newapp.show()
	
class previousApp(QtGui.QMainWindow, previous.Ui_MainWindow):
		global year ,month ,date
                global hour ,minute ,sec   		
		
		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self)  # 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
                        self.dateTimeEdit.setDateTime(QtCore.QDateTime(year,month,date,hour,minute,sec))
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime(2011,4,22,16,33,15))
			self.intermediateButton.clicked.connect(self.intermediate_profile)
			self.intermediateapp = intermediateApp()

			self.continousButton.clicked.connect(self.continous_profile)
			self.continousapp = continousApp() 

			self.variableButton.clicked.connect(self.variable_profile)
			self.variableapp = variableApp()
			
			self.previous_back.clicked.connect(self.previousAppbackbutton)

		def intermediate_profile(self):
			global Inter_Pressure
		        print('intermediate profile')
			self.close()
			  #self.intermediate.name_textdisplay.setText('NameTest')
			self.intermediateapp.show()	
			
			self.intermediateapp.nametext.setText(str(Name))
			self.intermediateapp.gendertext.setText(str(Gender))
			self.intermediateapp.agetext.setText(str(Age))
			self.intermediateapp.sitetext.setText(str(Site))
			self.intermediateapp.sizetext.setText(str(Size))
			self.intermediateapp.doctortext.setText(str(Doctor))
                        #self.intermediateapp.pressuretext.setText(str(Inter_Pressure))		   

		def continous_profile(self):
			
		        print('continous profile')
			self.close()
			self.continousapp.show()

			self.continousapp.nametext.setText(str(Name))
			self.continousapp.gendertext.setText(str(Gender))
			self.continousapp.agetext.setText(str(Age))
			self.continousapp.sitetext.setText(str(Site))
			self.continousapp.sizetext.setText(str(Size))
			self.continousapp.doctortext.setText(str(Doctor))

		def variable_profile(self):
			
		        print('variable profile')
			self.close()
			self.variableapp.show()

			self.variableapp.nametext.setText(str(Name))
			self.variableapp.gendertext.setText(str(Gender))
			self.variableapp.agetext.setText(str(Age))
			self.variableapp.sitetext.setText(str(Site))
			self.variableapp.sizetext.setText(str(Size))
			self.variableapp.doctortext.setText(str(Doctor))

		def previousAppbackbutton(self):
		        print ('previous_back')
			self.close()
			self.userapp = userApp()		        
			self.userapp.show()


class newApp(QtGui.QMainWindow, New.Ui_MainWindow):
               
    		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self)  #    
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			#self.back.clicked.connect(main_user)
			#self.userapp = userApp()
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
                        self.dateTimeEdit.setDateTime(QtCore.QDateTime(year,month,date,hour,minute,sec))
#                        self.setting.clicked.connect(app_setting)
#			self.settingsapp = settingsApp()
			self.nametext = KeyboardLineEdit(self)
			self.nametext.setGeometry(QtCore.QRect(107, 81, 283, 32))
			
			self.malebutton.setCheckable(True)
			self.malebutton.pressed.connect(self.male_check)

			self.femalebutton.setCheckable(True)
			self.femalebutton.pressed.connect(self.female_check)

			self.othersbutton.setCheckable(True)
			self.othersbutton.pressed.connect(self.others_check)
  		       
			self.agetext = KeyboardLineEdit(self)
			self.agetext.setGeometry(QtCore.QRect(107, 179, 283, 32))

			self.sitetext = KeyboardLineEdit(self)
			self.sitetext.setGeometry(QtCore.QRect(500, 80, 283, 32))


			self.sizetext = KeyboardLineEdit(self)
			self.sizetext.setGeometry(QtCore.QRect(500, 130, 283, 32))
        		
			self.doctortext = KeyboardLineEdit(self)
			self.doctortext.setGeometry(QtCore.QRect(500, 180, 283, 32))

			self.next.clicked.connect(self.next_details)
			#print ('name:' + self.nametext.text())
			self.previousapp = previousApp()

			#self.back.clicked.connect(self.newappbackbutton)
			#self.userapp = userApp()
			
		def male_check(self):
		        #print ('malenotselected')
			global Gender
			if self.malebutton.isChecked():
			    self.malebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -78.png'))
        		    print "male unselected"
			    #Gender = "Male"
			    #print Gender
     		        else:
                            print "male selected"
			    femalegender = False
			    print (femalegender)
			    othergender = False
			    print (othergender)
			    malegender = True
                            print (malegender)
			    self.femalebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -79.png'))

			    self.othersbutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -80.png'))
			    
			    self.malebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -81.png'))

			    if malegender  == True:   
				Gender = 'Male'
				print 'male assigned'				
	                        print (Gender)

		def female_check(self):
		        global Gender
			if self.femalebutton.isChecked():
			    self.femalebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -79.png'))
        		    print "female unselected"
			    #Gender = "Male"
			    #print Gender
     		        else:
                            print "female selected"
			    othergender = False
			    #print 'othergender:' + othergender
			    malegender = False
			    femalegender = True
			    self.malebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -78.png'))

			    self.othersbutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -80.png'))

			    self.femalebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -82.png'))

			    if femalegender == True:   
				Gender = 'Female'
				print 'Female assigned'				
	                        print (Gender)


		def others_check(self):
		        global Gender
			if self.othersbutton.isChecked():
			    self.othersbutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -80.png'))
        		    print "others unselected"
			    #Gender = "Male"
			    #print Gender
     		        else:
                            print "others selected"
			    malegender = False
			    femalegender = False
			    othergender = True
			    self.femalebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -78.png'))

			    self.malebutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -79.png'))

			    self.othersbutton.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Form Screen/Buttons/vac_screens (FORM) 800px X 480px (5.2.18) -83.png'))

			    if othergender == True:   
				Gender = 'Others'
				print 'others assigned'				
	                        print (Gender)

		def next_details(self):
			#temp_name = self.nametext.text()
			global Gender, malegender,femalegender,othergender,Name, Age, Site, Size, Doctor
			Name = self.nametext.text()
 
			

			#if self.maleradioButton.isChecked():
			#Gender = "Male"	
			#if self.femaleradioButton.isChecked():
			 #   Gender = "Female"
			#if self.otherradioButton.isChecked():
			 #   Gender = "Others"

			if malegender  == True:
      			   #Gender = "gender_tuple[0]"
                           self.intermediateapp.gendertext.setText("Male")
      		           print 'malegender'
			if femalegender == True:
      			   Gender = gender_tuple[1]
 			   print 'femalegender'
			if othergender == True:
      			   Gender = gender_tuple[2]
			   print 'othergender'
			#Gender = self.gendertext.text()
			Age = self.agetext.text()
			Site = self.sitetext.text()
			Size = self.sizetext.text()
			Doctor = self.doctortext.text()

			#dataname = Name
			#wb = openpyxl.Workbook()
  			#wb.save("datapath+dataname")	
			#tempname = Qstring.Name 	
			ws1['A1'] = str(Name)
			ws1['A2'] = str(Gender)
			ws1['A3'] = str(Age)
			ws1['A4'] = str(Site)
			ws1['A5'] = str(Size)
			ws1['A6'] = str(Doctor)
			wb.save("test.xlsx")

		        print ('Name:' + Name) 
			print('---------------------------------')
			print ('Gender:' + Gender) 
			print('---------------------------------')
			print ('Age:' + Age) 
			print('---------------------------------')
			print ('Site:' + Site) 
			print('---------------------------------')
			print ('Size:' + Size) 
			print('---------------------------------')
			print ('Doctor:' + Doctor)        

			self.close()
			self.previousapp.show()	

		def newappbackbutton(self):
		        print ('back')
			self.close()
			self.userapp = userApp()		        
			self.userapp.show()
		     #self.previousapp = previousApp()


class intermediateApp(QtGui.QMainWindow,  intermediate.Ui_MainWindow):
		#global dateTimeEdit   		
		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		        self.dateTimeEdit.setDateTime(QtCore.QDateTime(year,month,date,hour,minute,sec))
		        #global Inter_Pressure
		        #self.targetpressure_text.setText('str(Target_Pressure )')
			#self.name_textdisplay.setText('str(Name)')
			#self.intermediateapp.pressuretext.setText(str(Inter_Pressure))
			#self.intermediate_back.clicked.connect(self.intermediateAppback)
			self.editherapybutton.clicked.connect(self.inter_therapy_setting)
			self.intermediatesettingsapp = intermediatesettingsApp()

			self.intermediateplay.setCheckable(True)
      			self.intermediateplay.pressed.connect(self.intermediate_PlayPause)

#			self.intermediateplay.pressed.connect(self.intermediateplay)
#			self.intermediateplay.released.connect(self.intermediate_pause)			
			self.intermediatestop.clicked.connect(self.intermediate_stop)
			
			self.previous_back.clicked.connect(self.interAppbackbutton)

		def interAppbackbutton(self):
		        print ('interAppbackbutton')
			self.close()
			self.userapp = userApp()		        
			self.userapp.show()

			
		def intermediate_PlayPause(self):
			#w = QWidget()
			global temp_inter_cycle
		        print ('intermediatePlay')
			if self.intermediateplay.isChecked():
		              self.intermediateplay.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -14.png'))
                 	      #format Inter:200+C:10+TON:18+TOFF:12 print(Inter_cycle)
			      #if len(str(Inter_Pressure)) == 1:
 				     #Inter_Pressure = '0'+str(Inter_Pressure)
                                     #print Inter_Pressure
			      ser.write("Inter:200+C:"+str(Inter_cycle)+"+TON:"+str(Inter_Pump_on)+"+TOFF:"+str(Inter_Pump_off)+"+Inp:"+str(Inter_Pressure)) 
                              print"Inter:200+C:"+str(Inter_cycle)+"+TON:"+str(Inter_Pump_on)+"+TOFF:"+str(Inter_Pump_off)
			      #self.temp_inter_cycle = 0
			      self.timer_on = QtCore.QTimer()
                              self.value_on = Inter_Pump_on
        	              self.update_timer_on()
        		      self.timer_on.timeout.connect(self.count_on)
        		      self.timer_on.start(1000)


			      #self.timer_off = QtCore.QTimer()
                              #self.value_off = Inter_Pump_off
        	              #self.update_timer_off()
        		      #self.timer_off.timeout.connect(self.count_off)
        		      #self.timer_off.start(1000)
			      
				
     		        else:
                            self.intermediateplay.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -10.png'))
                            print "button released"
			    #ser.close()
                            #ser.open()

		def update_timer_on(self):
			self.runtime = "%d:%02d" % (self.value_on,self.value_on)
        		self.inter_lcdon.display(self.runtime)

		def update_timer_off(self):
			self.runtime = "%d:%02d" % (self.value_off,self.value_off)
        		self.inter_lcdoff.display(self.runtime)

		def count_on(self):                                        # Here's the 
    			global temp_inter_cycle
			if self.value_on > 0:
    			       self.value_on = self.value_on-1
			       self.update_timer_on()
			else:
			       self.timer_on.stop()
			       self.timer_off = QtCore.QTimer()
                               self.value_off = Inter_Pump_off
        	               self.update_timer_off()
        		       self.timer_off.timeout.connect(self.count_off)
        		       self.timer_off.start(1000)

		def count_off(self):                                        # Here's the 
    			global temp_inter_cycle
			if self.value_off > 0:
    			       self.value_off = self.value_off-1
			       temp_inter_cycle = temp_inter_cycle + 1
			       self.update_timer_off()
			 
		        elif temp_inter_cycle < Inter_cycle:
			       print "cycle less: "+str(temp_inter_cycle)
                               self.value_on = Inter_Pump_on
        	               self.timer_on.start()
			       self.count_on()
                               	
			elif temp_inter_cycle == Inter_cycle:
			       print "cycle equal: "+str(temp_inter_cycle)
			       self.timer_on.stop()				      
			       self.timer_off.stop()	
                               
 

		def intermediate_pause(self):
		        print ('intermediatePause')
			
			
		def intermediate_stop(self):
		        print ('intermediateStop')
			ser.write("I") 		        
			
		def intermediateAppback(self):
		        print ('intermediateAppback')
			self.close()
			self.newapp = newApp()		        
			self.newapp.show()
		
		def inter_therapy_setting(self):
			#temp_name = self.nametext.text()
			global Inter_Pressure, Pump_on, Pump_off, Cycle, Total_Duration
			
			print('Intermediate Settings')	
			#self.close()	
			self.intermediatesettingsapp.show()
			#Pressure = 0
			self.intermediatesettingsapp.press_inc.clicked.connect(self.pressure_inc)
			self.intermediatesettingsapp.press_dec.clicked.connect(self.pressure_dec)

			self.intermediatesettingsapp.pumpoff_inc.clicked.connect(self.pumpoff_inc)
			self.intermediatesettingsapp.pumpoff_dec.clicked.connect(self.pumpoff_dec)

			self.intermediatesettingsapp.pumpon_inc.clicked.connect(self.pumpon_inc)
			self.intermediatesettingsapp.pumpon_dec.clicked.connect(self.pumpon_dec)

			self.intermediatesettingsapp.cycle_inc.clicked.connect(self.cycle_inc)
			self.intermediatesettingsapp.cycle_dec.clicked.connect(self.cycle_dec)

                def pressure_inc(self):
			#global 	temp_Target_Pressure	        
			print ('pressure_inc')
			global Inter_Pressure 
			Inter_Pressure = Inter_Pressure + 1
			#if Inter_Pressure < 10:
			#print(len(str(Inter_Pressure)))
			   
		#       self.intermediatesettingsapp.pressuretext.setText('0'+str(Inter_Pressure).zfill(2))
			   #print (str(Inter_Pressure).zfill(2))
			self.intermediatesettingsapp.pressuretext.setText(str("{:02d}".format(Inter_Pressure)))
			#self.intermediateapp.pressuretext.setText(str(Inter_Pressure))
			ws1['A7'] = str(Inter_Pressure)
			wb.save("test.xlsx")

			#temp_Target_Pressure = temp_Target_Pressure + 1
			#pressuretext.setText(11)
                        #print (temp_Target_Pressure)

		def pressure_dec(self):
		        print ('pressure_dec')
			global Inter_Pressure 
    			Inter_Pressure = Inter_Pressure - 1
			self.intermediatesettingsapp.pressuretext.setText(str("{:02d}".format(Inter_Pressure)))
			#self.intermediateapp.pressuretext.setText(str(Inter_Pressure))
			

		def pumpoff_inc(self):
		        print ('pumpoff_inc')
			global Inter_Pump_off
			Inter_Pump_off = Inter_Pump_off + 1
			
			self.intermediatesettingsapp.pumpofftext.setText(str("{:02d}".format(Inter_Pump_off)))

		def pumpoff_dec(self):
		        print ('pumpoff_dec')
			global Inter_Pump_off
			Inter_Pump_off = Inter_Pump_off - 1
			self.intermediatesettingsapp.pumpofftext.setText(str("{:02d}".format(Inter_Pump_off)))

		def pumpon_inc(self):
		        print ('pumpon_inc')
			global Inter_Pump_on
			Inter_Pump_on = Inter_Pump_on + 1
			self.intermediatesettingsapp.pumpontext.setText(str("{:02d}".format(Inter_Pump_on)))

		def pumpon_dec(self):
		        print ('pumpon_dec')
			global Inter_Pump_on
			Inter_Pump_on = Inter_Pump_on - 1
			self.intermediatesettingsapp.pumpontext.setText(str("{:02d}".format(Inter_Pump_on)))

		def cycle_inc(self):
		        print ('cycle_inc')
			global Inter_cycle
			Inter_cycle = Inter_cycle + 1
			self.intermediatesettingsapp.cycletext.setText(str("{:02d}".format(Inter_cycle)))

		def cycle_dec(self):
		        print ('cycle_dec')
			global Inter_cycle
			Inter_cycle = Inter_cycle - 1
			self.intermediatesettingsapp.cycletext.setText(str("{:02d}".format(Inter_cycle)))

class intermediatesettingsApp(QtGui.QMainWindow,  intermediate_settings.Ui_MainWindow):
    		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			self.intersettingback.clicked.connect(self.cancel_fun)
			self.startintermediateButton.clicked.connect(self.start_interprocess)
			#self.startintermediateButton.clicked.connect(self.intermediate_profile)
			
			
			
		def cancel_fun(self):
                        
			self.close()
			print('cancel') 
		
		def start_interprocess(self):
			print('interprocess') 
			print(Inter_Pressure)
			self.close()
			#self.intermediateapp.show()	
                        #self.intermediateapp.pressuretext.setText(str(Inter_Pressure))
                        	
			'''
			#self.intermediateapp.nametext.setText(str(Name))
			
			global Target_Pressure, Pump_on, Pump_off, Cycle, Total_Duration
			#Total_Duration = ( (Target_Pressure * Pump_on) + (Target_Pressure * Pump_off)) * 10
			print('ok') 
		    	temp_Target_Pressure = int(self.tp_text.text())
		    	temp_Pump_on = int(self.pon_text.text())
		    	temp_Pump_off = int(self.poff_text.text())
			temp_Cycle = int(self.cycle_text.text())
			temp_Total_Duration = (temp_Pump_on+ temp_Pump_off) * temp_Cycle 
			print(temp_Target_Pressure)
			print(temp_Total_Duration  ) 
			
			Target_Pressure = temp_Target_Pressure
			Pump_on = temp_Pump_on
			Pump_off = temp_Pump_off 
			Cycle = temp_Cycle 
			Total_Duration = temp_Total_Duration
			self.close()
			self.intermediateapp = intermediateApp()
			self.intermediateapp.targetpressure_text.setText('str(temp_Target_Pressure)')
			#print(targetpressure_text)
			temp_Target_Pressure = None
			print(temp_Target_Pressure)
                  '''

class continousApp(QtGui.QMainWindow,  continous.Ui_MainWindow):
		#global dateTimeEdit   		
		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
		
			self.previous_back.clicked.connect(self.contiAppbackbutton)
			self.Conti_editherapybutton.clicked.connect(self.cont_therapy_setting)
			self.continioussettingsapp = continioussettingsApp()

			self.Conti_play.setCheckable(True)
      			self.Conti_play.pressed.connect(self.Conti_PlayPause)

#			self.intermediateplay.pressed.connect(self.intermediateplay)
#			self.intermediateplay.released.connect(self.intermediate_pause)			
			self.Conti_stop.clicked.connect(self.continous_stop)
			

		def Conti_PlayPause(self):    
			#w = QWidget()
		        print ('Conti_PlayPause')
			if self.Conti_play.isChecked():
		              self.Conti_play.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -14.png'))
                 	     
			      ser.write("Conti:200"+"+TON:"+str('%0d' % cont_pumpon_inc)+"+P:"+str(cont_pressuretext)) 
                              print"Conti:200"+"+TON:"+str(cont_pumpon_inc)+"+P:"+str(cont_pressuretext)
			      self.Conti_presstext.setText(str("{:02d}".format(cont_pressuretext)))
			      self.Conti_totaltext.setText(str("{:02d}".format(cont_pumpon_inc)))			      

			      self.timer = QtCore.QTimer()
                              self.value = cont_pumpon_inc
        # Update display and start timer
        	              self.update_timer()
        		      self.timer.timeout.connect(self.count)
        		      self.timer.start(60000)
			      #self.Conti_cdNumber.setProperty("intValue", self.value)
			      
			      #def count(self):                                        # Here's the 
    			         # self.display(self.value)
    			          #self.value = self.value-1
				
     		        else:
                            self.Conti_play.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -10.png'))
                            print "button released"
			    #self.timer.stop()
			    #ser.close()
                            #ser.open()
			    self.timer.stop()

		def update_timer(self):
        		#self.runtime = "%d:%02d" % (self.value/60,self.value % 60)
			self.runtime = "%d:%02d" % (self.value,self.value)
        		self.Conti_lcdon.display(self.runtime)

		def count(self):                                        # Here's the 
    			#self.display(self.value)
			if self.value > 0:
    			       self.value = self.value-1
			       self.update_timer()
			else:
			       self.timer.stop()

  		def continous_stop(self):
		        print ('continous_stop')
			self.Conti_lcdon.display(0)
			ser.write("C") 
			ser.write("C")
			self.timer.stop()

		def cont_therapy_setting(self):
			#temp_name = self.nametext.text()
			
			
			print('Continous Settings')	
			#self.close()	
			self.continioussettingsapp.show()
			#Pressure = 0
			self.continioussettingsapp.cont_press_inc.clicked.connect(self.cont_pressure_inc)
			self.continioussettingsapp.cont_press_dec.clicked.connect(self.cont_pressure_dec)
		
			self.continioussettingsapp.cont_pumpon_inc.clicked.connect(self.cont_pumpon_inc)
			self.continioussettingsapp.cont_pumpon_dec.clicked.connect(self.cont_pumpon_dec)

		def cont_pressure_inc(self):
			#global 	temp_Target_Pressure	        
			print ('cont_pressure_inc')
			global cont_pressuretext 
			cont_pressuretext = cont_pressuretext + 1
			self.continioussettingsapp.cont_pressuretext.setText(str("{:02d}".format(cont_pressuretext)))

		def cont_pressure_dec(self):
		        print ('cont_pressure_dec')
			global cont_pressuretext 
    			cont_pressuretext = cont_pressuretext - 1
			self.continioussettingsapp.cont_pressuretext.setText(str("{:02d}".format(cont_pressuretext)))

		def cont_pumpon_inc(self):
		        print ('cont_pumpon_inc')
			global cont_pumpon_inc
			cont_pumpon_inc = cont_pumpon_inc + 1
			
			self.continioussettingsapp.cont_pumpontext.setText(str("{:02d}".format(cont_pumpon_inc)))

		def cont_pumpon_dec(self):
		        print ('cont_pumpon_dec')
			global cont_pumpon_inc
			cont_pumpon_inc = cont_pumpon_inc - 1
			
			self.continioussettingsapp.cont_pumpontext.setText(str("{:02d}".format(cont_pumpon_inc)))	

		def contiAppbackbutton(self):
		        print ('interAppbackbutton')
			self.close()
			self.userapp = userApp()		        
			self.userapp.show()

class continioussettingsApp(QtGui.QMainWindow,  continous_settings.Ui_MainWindow):
    		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			self.contsettingback.clicked.connect(self.cont_cancel_fun)
			self.startcontiniousButton.clicked.connect(self.start_contprocess)

		def cont_cancel_fun(self):
			self.close()
			print('cancel') 
		
		def start_contprocess(self):
			print('contprocess') 
			self.close()
		

class variableApp(QtGui.QMainWindow,  variable.Ui_MainWindow):
		#global dateTimeEdit   		
		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			#self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		        self.dateTimeEdit.setDateTime(QtCore.QDateTime(year,month,date,hour,minute,sec))
		      
			self.var_editherapybutton.clicked.connect(self.vareditherapybutton)
			self.variablesettingsapp = variablesettingsApp()

			self.Var_play.setCheckable(True)
      			self.Var_play.pressed.connect(self.var_PlayPause)
			
			self.Var_stop.clicked.connect(self.var_stop)
			
			self.previous_back.clicked.connect(self.varAppbackbutton)
	
		def varAppbackbutton(self):
		        print ('interAppbackbutton')
			self.close()
			self.userapp = userApp()		        
			self.userapp.show()

			
		def var_PlayPause(self):
			
			global temp_inter_cycle
		        print ('intermediatePlay')
			if self.Var_play.isChecked():
		              self.Var_play.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -14.png'))
                 	     
			      ser.write("Inter:200+C:"+str(Inter_cycle)+"+TON:"+str(Inter_Pump_on)+"+TOFF:"+str(Inter_Pump_off)+"+Inp:"+str(Inter_Pressure)) 
                              print"Inter:200+C:"+str(Inter_cycle)+"+TON:"+str(Inter_Pump_on)+"+TOFF:"+str(Inter_Pump_off)
			      #self.temp_inter_cycle = 0
			      self.timer_var_on1 = QtCore.QTimer()
                              self.value_var_on1 = Inter_Pump_on
        	              self.update_timer_var_on1()
        		      self.timer_var_on1.timeout.connect(self.var_count_on)
        		      self.timer_var_on1.start(1000)


			      #self.timer_off = QtCore.QTimer()
                              #self.value_off = Inter_Pump_off
        	              #self.update_timer_off()
        		      #self.timer_off.timeout.connect(self.count_off)
        		      #self.timer_off.start(1000)
			      
				
     		        else:
                            self.Var_play.setIcon(QtGui.QIcon('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/Intermediate page/Buttons/vac_screens (Intermediate page ) 800px X 480px (5.2.18) -10.png'))
                            print "button released"
			    #ser.close()
                            #ser.open()

		def update_timer_var_on1(self):
			self.runtime = "%d:%02d" % (self.value_var_on1,self.value_var_on1)
        		self.var_lcdon.display(self.runtime)

		def update_timer_var_off(self):
			self.runtime = "%d:%02d" % (self.value_var_off,self.value_var_off)
        		self.var_lcdoff.display(self.runtime)

		def var_count_on(self):                                        # Here's the 
    			global temp_inter_cycle
			if self.value_var_on1 > 0:
    			       self.value_var_on1 = self.value_var_on1-1
			       self.update_timer_var_on1()
			else:
			       self.timer_var_on1.stop()
			       self.timer_var_off = QtCore.QTimer()
                               self.value_var_off = Inter_Pump_off
        	               self.update_timer_off()
        		       self.timer_var_off.timeout.connect(self.var_count_off)
        		       self.timer_var_off.start(1000)

		def var_count_off(self):                                        # Here's the 
    			global temp_inter_cycle
			if self.value_var_off > 0:
    			       self.value_var_off = self.value_var_off-1
			       temp_inter_cycle = temp_inter_cycle + 1
			       self.update_timer_var_off()
			 
		        elif temp_inter_cycle < Inter_cycle:
			       print "cycle less: "+str(temp_inter_cycle)
                               self.value_var_on1 = Inter_Pump_on
        	               self.timer_var_on1.start()
			       self.var_count_on()
                               	
			elif temp_inter_cycle == Inter_cycle:
			       print "cycle equal: "+str(temp_inter_cycle)
			       self.timer_var_on1.stop()				      
			       self.timer_var_off.stop()	
                               
 

		def intermediate_pause(self):
		        print ('variablePause')
			
			
		def var_stop(self):
		        print ('variableStop')
			ser.write("V") 		        
			
		
		def vareditherapybutton(self):
			#temp_name = self.nametext.text()
			global Inter_Pressure, Pump_on, Pump_off, Cycle, Total_Duration
			
			print('Intermediate Settings')	
			#self.close()	
			self.variablesettingsapp.show()
			#Pressure = 0
			self.variablesettingsapp.var_press_inc1.clicked.connect(self.pressure_inc1)
			self.variablesettingsapp.var_press_dec1.clicked.connect(self.pressure_dec1)

			self.variablesettingsapp.var_press_inc2.clicked.connect(self.pressure_inc2)
			self.variablesettingsapp.var_press_dec2.clicked.connect(self.pressure_dec2)

			self.variablesettingsapp.var_inc_off.clicked.connect(self.var_pumpoff_inc)
			self.variablesettingsapp.var_dec_off.clicked.connect(self.var_pumpoff_dec)

			self.variablesettingsapp.var_inc_on1.clicked.connect(self.pumpon_inc1)
			self.variablesettingsapp.var_dec_on1.clicked.connect(self.pumpon_dec1)

			self.variablesettingsapp.var_inc_on2.clicked.connect(self.pumpon_inc2)
			self.variablesettingsapp.var_dec_on2.clicked.connect(self.pumpon_dec2)

			self.variablesettingsapp.var_cycle_inc.clicked.connect(self.varcycle_inc)
			self.variablesettingsapp.var_cycle_dec.clicked.connect(self.varcycle_dec)

		def pressure_inc1(self):
		        print ('pressure_inc1')
			#global Inter_Pressure 
    			#Inter_Pressure = Inter_Pressure - 1
			#self.variablesettingsapp.var_pressuretext1.setText(str(Inter_Pressure))
		
		def pressure_dec1(self):
		        print ('pressure_dec1')
			#global Inter_Pressure 
    			#Inter_Pressure = Inter_Pressure - 1
			#self.variablesettingsapp.var_pressuretext1.setText(str(Inter_Pressure))
		
		def pressure_inc2(self):
		        print ('pressure_inc2')
			#global Inter_Pressure 
    			#Inter_Pressure = Inter_Pressure - 1
			#self.variablesettingsapp.var_pressuretext2.setText(str(Inter_Pressure))
		
		def pressure_dec2(self):
		        print ('pressure_dec2')
			#global Inter_Pressure 
    			#Inter_Pressure = Inter_Pressure - 1
			#self.variablesettingsapp.var_pressuretext2.setText(str(Inter_Pressure))

		def var_pumpoff_inc(self):
		        print ('varpumpoff_inc')
			#global Inter_Pump_off
			#Inter_Pump_off = Inter_Pump_off + 1
			#self.variablesettingsapp.var_durationoff.setText(str(Inter_Pump_off))

		def var_pumpoff_dec(self):
		        print ('varpumpoff_dec')
			#global Inter_Pump_off
			#Inter_Pump_off = Inter_Pump_off - 1
			#self.variablesettingsapp.var_durationoff.setText(str(Inter_Pump_off))

		def pumpon_inc1(self):
		        print ('pumpon_inc1')
			#global Inter_Pump_on
			#Inter_Pump_on = Inter_Pump_on + 1
			#self.variablesettingsapp.var_durationon1.setText(str(Inter_Pump_on))

		def pumpon_dec1(self):
		        print ('pumpon_dec1')
			#global Inter_Pump_on
			#Inter_Pump_on = Inter_Pump_on - 1
			#self.variablesettingsapp.var_durationon1.setText(str(Inter_Pump_on))

		def pumpon_inc2(self):
		        print ('pumpon_inc2')
			#global Inter_Pump_on
			#Inter_Pump_on = Inter_Pump_on + 1
			#self.variablesettingsapp.var_durationon2.setText(str(Inter_Pump_on))

		def pumpon_dec2(self):
		        print ('pumpon_dec2')
			#global Inter_Pump_on
			#Inter_Pump_on = Inter_Pump_on - 1
			#self.variablesettingsapp.var_durationon2.setText(str(Inter_Pump_on))

		def varcycle_inc(self):
		        print ('cycle_inc')
			#global Inter_cycle
			#Inter_cycle = Inter_cycle + 1
			#self.variablesettingsapp.var_cycle.setText(str(Inter_cycle))

		def varcycle_dec(self):
		        print ('cycle_dec')
			#global Inter_cycle
			#Inter_cycle = Inter_cycle - 1
			#self.variablesettingsapp.var_cycle.setText(str(Inter_cycle))


class variablesettingsApp(QtGui.QMainWindow,  variable_settings.Ui_MainWindow):
    		def __init__(self):
        		super(self.__class__, self).__init__()
        		self.setupUi(self) 
			self.setWindowFlags(QtCore.Qt.CustomizeWindowHint )
			self.varsettingback.clicked.connect(self.cancel_fun)
			self.startvariableButton.clicked.connect(self.var_interprocess)
			
			
			
			
		def cancel_fun(self):    
			self.close()
			print('cancel') 
		
		def var_interprocess(self):
			print('varprocess') 
			self.close()


def main():
    		app = QtGui.QApplication(sys.argv) 
		app.setStyle('GTK+')
		
		#dateTimeEdit = QtCore.QDateTime(year,month,date,hour,minute,sec)
    		thread = threading.Thread(target=read_from_port, args=(ser,))
                thread.start()     
   		#mainapp = mainApp()
		#mainapp.show() 
		#time.stamp()
		'''
		w = QWidget()
                w.resize(800, 480)
		label = QLabel(w)
		pixmap = QPixmap('/media/user/B0CC7EBFCC7E7F80/GUI/Design7/UiScreens/1.jpg')
		label.setPixmap(pixmap)
		w.resize(pixmap.width(),pixmap.height())
                w.show()
		w.close()
		'''
	
		mainapp = mainApp() 
    		mainapp.show()                   
    		app.exec_()                         

if __name__ == '__main__':  
    #thread = threading.Thread(target=read_from_port, args=(ser,))
    #thread.start() 
      
    main() 


