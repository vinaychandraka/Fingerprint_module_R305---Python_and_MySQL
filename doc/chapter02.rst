R305 FINGERPRINT MODULE BASICS
==============================

`Click to Download datasheet <http://www.rhydolabz.com/documents/finger-print-module.pdf>`_

Operation principle:
--------------------

	Fingerprint processing includes two parts: fingerprint enrollment and fingerprint matching (the matching can be 1:1 or 1:N).When enrolling, user needs to enter the finger two times. The system will process the two time finger images, generate a template of the finger based on processing results and store the template. When matching, user enters the finger through optical sensor and system will generate a template of the finger and compare it with templates of the finger library.


Hardware connection:
--------------------

	Via serial interface, the Module may communicate with MCU of 3.3V or 5V power: TD (pin 3 of P1) connects with RXD (receiving pin of MCU), RD (pin 4 of P1) connects with TXD (transferring pin of MCU). 

Communication Protocol:
-----------------------

	We can communicate with the module using a packet of hex codes in a specific format. The data package format for communication is shown below.

	.. image:: /image/3.jpg

	Thus a data package transferred to or from the module will include a Header, Address, Package Identifier, Package Length, Package Content and Checksum.
	
	The example shown below asks the module to collect the finger image.

	eg.EF 01 FF FF FF FF 01 00 03 01 00 05

	Header: EF 01 

	Address: FF FF FF FF

	Package Identifier: 01

	Package Length: 00 03 

	Package Content: 01

	Checksum: 00 05

	For more details on the data package contents see the table below:

	.. image:: /image/4.jpg

