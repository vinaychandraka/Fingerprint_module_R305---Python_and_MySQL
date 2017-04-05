PYTHON CODE
===========
.. note:: Use Python2.7 version
.. note:: Linux users install LAMP. Windows user install WAMP. 
.. note:: Create a database. I have created a database named 'fingerdb'. Create a table. I have created a table named 'fingertb' with fields 'slno','name' and 'finger'

Upload to database
------------------

Code below uploads finger template to database::

	import serial, time, datetime
	import struct           #Convert between strings and binary data
	import sys
	import os
	import binascii
	import mysql.connector
	cnx=mysql.connector.connect(user='root',password='',host='localhost',database='fingerdb')	# connect to MySql database
	cur=cnx.cursor()

	#ser = serial.Serial('/dev/ttyUSB0',57600)      # serial communication in Linux
	ser = serial.Serial("COM6", baudrate=9600, timeout=1)   #serial communication in Windows

	pack = [0xef01, 0xffffffff, 0x1]        # Header, Address and Package Identifier

	def readPacket():       # Function to read the Acknowledge packet
		time.sleep(1)
		w = ser.inWaiting()
		ret = []
		if w >= 9:
			s = ser.read(9)         # Partial read to get length
			ret.extend(struct.unpack('!HIBH', s))   
			ln = ret[-1]
		
			time.sleep(1)
			w = ser.inWaiting()
			if w >= ln:
				s = ser.read(ln)
				form = '!' + 'B' * (ln - 2) + 'H'       # Specifying byte size
				ret.extend(struct.unpack(form, s))
		return ret

	def readPacket1():      # Function to read the Acknowledge packet
		time.sleep(1)
		w = ser.inWaiting()
		ret = []
		form = 'B' * 700        
		s = ser.read(700)
		t=binascii.hexlify(s)   # convert to hex
		u=t[24:]
		cur.execute("insert into fingertb(name,finger) values('%s','%s')" %(name,u) )     # upadate database
		cnx.commit()
		v=binascii.unhexlify(u)
		form1='B'*688
		ret1=[]
		ret1.extend(struct.unpack(form1, v))
		ret.extend(struct.unpack(form, s))
	
	def writePacket(data):          # Function to write the Command Packet
		pack2 = pack + [(len(data) + 2)]
		a = sum(pack2[-2:] + data)
		pack_str = '!HIBH' + 'B' * len(data) + 'H'
		l = pack2 + data + [a]
		s = struct.pack(pack_str, *l)
		ser.write(s)


	def verifyFinger():     # Verify Module’s handshaking password
		data = [0x13, 0x0, 0, 0, 0]
		writePacket(data)
		s = readPacket()
		return s[4]
	
	def genImg():   # Detecting finger and store the detected finger image in ImageBuffer
		data = [0x1]
		writePacket(data)
		s = readPacket()
		return s[4]	

	def img2Tz(buf):        # Generate character file from the original finger image in ImageBuffer and store the file in CharBuffer1 or CharBuffer2.
		data = [0x2, buf]
		writePacket(data)
		s = readPacket()
		return s[4]

	def regModel():         # Combine information of character files from CharBuffer1 and CharBuffer2 and generate a template which is stroed back in both CharBuffer1 and CharBuffer2.
		data = [0x5]
		writePacket(data)
		s = readPacket()
		return s[4]

	def UpChar(buf):        # Upload the character file or template of CharBuffer1/CharBuffer2 to upper computer
		data = [0x8,buf]
		writePacket(data)
		s = readPacket1()
	
	print ("Type done to exit")
	name=raw_input("Enter name : ")
	while (name!='done'):   
        
        	if verifyFinger():              
                	print 'Verification Error'
                	sys.exit(0)

        	print 'Put finger',
        	sys.stdout.flush()

        	time.sleep(1)	
        	while genImg():         
                	time.sleep(0.1)
                	print '.',
                	sys.stdout.flush()

        	print ''
        	sys.stdout.flush()

        	if img2Tz(1):                   
                	print 'Conversion Error'
                	sys.exit(0)

        	print 'Put finger again',
        	sys.stdout.flush()

        	time.sleep(1)	
        	while genImg():
                	time.sleep(0.1)
                	print '.',
                	sys.stdout.flush()

        	print ''
        	sys.stdout.flush()

        	if img2Tz(2):           
                	print 'Conversion Error'
                	sys.exit(0)

        	if regModel():
                	print 'Template Error'
                	sys.exit(0)

        	if UpChar(2):
                	print 'Template Error'
                	sys.exit(0)

        	name=raw_input("Enter name : ")

Download to R305 fingerprint module
-----------------------------------

.. note:: After entering 'name', enter integer values 1,2,3.... for 'store id'. 

.. warning:: Entering the same 'store id' for differnet names will overwrite the finger templete stored.

Code below downloads the finger template from database to R305 fingerprint module::

	import serial, time, datetime, struct
	import sys
	import os
	import mysql.connector
	import binascii
	cnx=mysql.connector.connect(user='root',password='',host='localhost',database='fingerdb')
	cur=cnx.cursor()
	ser = serial.Serial("COM6", baudrate=9600, timeout=1)
	pack = [0xef01, 0xffffffff, 0x1]

	def readPacket():
		time.sleep(1)
		w = ser.inWaiting()
		ret = []
		if w >= 9:
			s = ser.read(9) #partial read to get length
			ret.extend(struct.unpack('!HIBH', s))
			ln = ret[-1]
		
			time.sleep(1)
			w = ser.inWaiting()
			if w >= ln:
				s = ser.read(ln)
				form = '!' + 'B' * (ln - 2) + 'H'
				ret.extend(struct.unpack(form, s))
			
		return ret

	def readPacket1():
        
        	time.sleep(1)
        	w = ser.inWaiting()

        	time.sleep(1)
        	pack_str='B'* 688
        
        	cur.execute("select finger from fingertb where name='%s'"%name)
        	row=cur.fetchone()
        	srow = str(row[0])
        	v=binascii.unhexlify(srow)
        	form1='B'*688
        	ret1=[]
        	ret1.extend(struct.unpack(form1, v))
        	x=ret1
        	s = struct.pack(pack_str, *x)
        	ser.write(s)
        	if store(idno):
                	print 'store error'
                	sys.exit(0)
                	print "Enrolled successfully at id %d"%j	

	def writePacket(data):
		pack2 = pack + [(len(data) + 2)]
		a = sum(pack2[-2:] + data)
		pack_str = '!HIBH' + 'B' * len(data) + 'H'
		l = pack2 + data + [a]
		s = struct.pack(pack_str, *l)
		ser.write(s)


	def verifyFinger():
		data = [0x13, 0x0, 0, 0, 0]
		writePacket(data)
		s = readPacket()
		return s[4]	

	def DownChar(buf):	# download character file or template from upper computer to the specified buffer of Module
		data = [0x9,buf]
		writePacket(data)
		s = readPacket1()

	def store(id):		# store the template of specified buffer (Buffer1/Buffer2) at the designated location of Flash library
		data = [0x6, 0x1, 0x0, id]
		writePacket(data)
		s = readPacket()
		return s[4]	

	name=raw_input('enter the name please')
	idno=int(raw_input('enter the store id'))
	if verifyFinger():              # Verify Password
		print 'Verification Error'
		sys.exit(0)

	if DownChar(1):
        	print 'Template Error'
        	sys.exit(0)


Search and authenticate
-----------------------

Code below scans the finger and authenticates::

	import serial, time, datetime, struct
	import sys 

	ser = serial.Serial("COM6", baudrate=9600, timeout=1)

	pack = [0xef01, 0xffffffff, 0x1]

	def readPacket():
		time.sleep(1)
		w = ser.inWaiting()
		ret = []
		if w >= 9:
			s = ser.read(9)         #partial read to get length
			ret.extend(struct.unpack('!HIBH', s))
			ln = ret[-1]
		
			time.sleep(1)
			w = ser.inWaiting()
			if w >= ln:
				s = ser.read(ln)
				form = '!' + 'B' * (ln - 2) + 'H'
				ret.extend(struct.unpack(form, s))
		return ret


	def writePacket(data):
		pack2 = pack + [(len(data) + 2)]
		a = sum(pack2[-2:] + data)
		pack_str = '!HIBH' + 'B' * len(data) + 'H'
		l = pack2 + data + [a]
		s = struct.pack(pack_str, *l)
		ser.write(s)


	def verifyFinger():
		data = [0x13, 0x0, 0, 0, 0]
		writePacket(data)
		s = readPacket()
		return s[4]
	
	def genImg():
		data = [0x1]
		writePacket(data)
		s = readPacket()
		return s[4]	

	def img2Tz(buf):
		data = [0x2, buf]
		writePacket(data)
		s = readPacket()
		return s[4]

	def search():	# search the whole finger library for the template that matches the one in CharBuffer1 or CharBuffer2
		data = [0x4, 0x1, 0x0, 0x0, 0x0, 0x5]
		writePacket(data)
		s = readPacket()
		return s[4:-1]	
	

	if verifyFinger():
		print 'Verification Error'
		sys.exit(-1)

	print 'Put finger',
	sys.stdout.flush()

	time.sleep(1)	
	for _ in range(5):
		g = genImg()
		if g == 0:              
			break

		print '.',
		sys.stdout.flush()

	print ''
	sys.stdout.flush()
	if g != 0:
		sys.exit(-1)

	if img2Tz(1):
		print 'Conversion Error'
		sys.exit(-1)

	r = search()
	print 'Search result', r
	if r[0] == 0 :
		print 'Authentication Successful'
		sys.exit(0)

	else:
        	print 'Authentication fail'
	sys.exit(1)
