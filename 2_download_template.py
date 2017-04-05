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
			print (ret)
			
	return ret

def readPacket1():
        
        time.sleep(1)
        w = ser.inWaiting()
        print (w)

        time.sleep(1)
        pack_str='B'* 688
        
        cur.execute("select finger from fingertb where name='%s'"%name)
        row=cur.fetchone()
        #print type(row)
        srow = str(row[0])
        #print 'row is ',type(srow)
        v=binascii.unhexlify(srow)
        print 'v is',v
        form1='B'*688
        ret1=[]
        ret1.extend(struct.unpack(form1, v))
        x=ret1
        print x
        s = struct.pack(pack_str, *x)
        ser.write(s)
        if store(idno):
                print 'store error'
                sys.exit(0)
                print "Enrolled successfully at id %d"%j	
                        
                
	
##	ret = []
##	form = 'B' * 700
##	s = ser.read(700)
##	ret.extend(struct.unpack(form, s))
##	print (ret)
##	j=ret.strip()   # Doesn't work
##	print (j)

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

def DownChar(buf):
	data = [0x9,buf]
	writePacket(data)
	s = readPacket1()

def store(id):
	data = [0x6, 0x1, 0x0, id]
	writePacket(data)
	s = readPacket()
	return s[4]	

name=raw_input('enter the name please')
print (type(name))
idno=int(raw_input('enter the store id'))
print (type(idno))
if verifyFinger():              # if password is correct zero gets returned , else a non zero value (13H) gets returned and 'Verification Error' gets printed
	print 'Verification Error'
	sys.exit(0)

if DownChar(1):
        print 'Template Error'
        sys.exit(0)


##id = 1
##if store(id):
##	print 'Store Error'
##	sys.exit(0)	
##
##print "Enrolled successfully at id %d"%id	
