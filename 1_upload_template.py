import serial, time, datetime, struct
import sys
import os
import binascii
import mysql.connector
cnx=mysql.connector.connect(user='root',password='',host='localhost',database='fingerdb')
cur=cnx.cursor()


#ser = serial.Serial('/dev/ttyUSB0',57600)
ser = serial.Serial("COM6", baudrate=9600, timeout=1)

pack = [0xef01, 0xffffffff, 0x1]

def printx(l):
	for i in l:
		print hex(i),
	print ''

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
			print (ret)
	return ret

def readPacket1():
	time.sleep(1)
	w = ser.inWaiting()
	print (w)
	ret = []
	form = 'B' * 700
	s = ser.read(700)
	t=binascii.hexlify(s)   # convert to hex
	print len(t)
	print 'value stored in t is \n',t
	u=t[24:]
	print 'value stured in u is \n', u
	cur.execute("insert into fingertb(name,finger) values('%s','%s')" %(name,u) )     # upadate database
	cnx.commit()
	v=binascii.unhexlify(u)
	print 'value of v is',v
	form1='B'*688
	ret1=[]
	ret1.extend(struct.unpack(form1, v))
	print 'value of ret1 is', ret1
	#print (binascii.hexlify(s))
	ret.extend(struct.unpack(form, s))
	print 'value in ret is \n', ret
	
##	j=ret.strip()   # Doesn't work
##	print (j)


def readPacket2():
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
			print (ret)

		w = ser.inWaiting()
		print (w)
		ret0=[]
		form = 'B' * 688
		s = ser.read(700)
		ret0.extend(struct.unpack(form, s))
		print (ret0)
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

def regModel():
	data = [0x5]
	writePacket(data)
	s = readPacket()
	return s[4]
def UpChar(buf):
	data = [0x8,buf]
	writePacket(data)
	s = readPacket1()
##	return s[4]

def store(id):
	data = [0x6, 0x1, 0x0, id]
	writePacket(data)
	s = readPacket()
	return s[4]	

	
print ("Type done to exit")
name=raw_input("Enter name : ")
while (name!='done'):
        
        if verifyFinger():              # if password is correct zero gets returned , else a non zero value (13H) gets returned and 'Verification Error' gets printed
                print 'Verification Error'
                sys.exit(0)

        print 'Put finger',
        sys.stdout.flush()

        time.sleep(1)	
        while genImg():         # Confirmation code=00H: finger collection successs . Otherwise a non zero value is returned and dot (. . . . ) gets printed
                time.sleep(0.1)
                print '.',
                sys.stdout.flush()

        print ''
        sys.stdout.flush()

        if img2Tz(1):                   # use buffer 1 (page 17 datasheet)
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

        if img2Tz(2):           # use buffer 2 (page 17 datasheet)
                print 'Conversion Error'
                sys.exit(0)

        if regModel():
                print 'Template Error'
                sys.exit(0)

        if UpChar(2):
                print 'Template Error'
                sys.exit(0)

        name=raw_input("Enter name : ")




##id = 2
##if store(id):
##	print 'Store Error'
##	sys.exit(0)	
##
##print "Enrolled successfully at id %d"%id	
