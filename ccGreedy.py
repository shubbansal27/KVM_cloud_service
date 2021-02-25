#cc
import socket               

ipnc1='10.42.0.1'
ipclc='10.42.0.38'
ipcc='10.42.0.38'
ipnc2 = '10.42.0.253'

def modifyVM(code,successCode,failureCode):
	portnc=12346
	ncsock1=socket.socket()
	ncsock1.connect((ipnc1, portnc)) 
	vname1 = rMsg	
	msg1=code+":"+vname1
	print msg1
	ncsock1.send(msg1)			   
	ncresponse1=ncsock1.recv(1024)
	print ncresponse1
	if (ncresponse1=="1"):
		c.send(successCode)
	else:
		ncsock2=socket.socket()
		ncsock2.connect((ipnc1, portnc)) 
		vname2 = rMsg	
		msg2=code+":"+vname2
		print msg2
		ncsock2.send(msg2)				   
		ncresponse2=ncsock2.recv(1024)
		print ncresponse2
		if (ncresponse2=="1"):
			c.send(successCode)
		else:
			c.send(failureCode)


s = socket.socket()         
host = socket.gethostname() 
portclc = 12345                
s.bind((ipcc, portclc))        
s.listen(5)                 
while True:
	c, addr = s.accept()     
	clcRequest= c.recv(1024)
	ncresponse=""
	print "request received from clc:",clcRequest
	mcode,rMsg=clcRequest.split(":")
	if(mcode=="1"):#create VM request from clc
		ncsock1 = socket.socket() 
		portnc=12346
		ncsock1.connect((ipnc1, portnc)) 
		msg="101"#free disk and RAM in NC
		ncsock1.send(msg)	   
		ncresponse1=ncsock1.recv(1024)
		ncsock1.close()
		ncsock2 = socket.socket() 
		portnc=12346
		ncsock2.connect((ipnc2, portnc)) 
		msg2="101"
		ncsock2.send(msg2)	   
		ncresponse2=ncsock2.recv(1024)
		ncsock2.close()	
			
		print "response received from nc:",ncresponse1
		vname,vdisk,vram,vcore = rMsg.split(",")#new VM config
		print "vdisk",vdisk
		print "vram",vram
		print "vcore",vcore		
		rcode,reMsg=ncresponse1.split(":")		
		rdisk,rram=reMsg.split(",")#free disk and RAM in NC
		print "rdisk",rdisk
		print "rram",rram
		ncresponse2="" 
		if (rcode =="102"):
			
			if (int(rdisk)>int(vdisk) and float(rram)>float(vram)):
				ncsock = socket.socket() 
				portnc=12346
				ncsock.connect((ipnc1, portnc)) 
				msg1="103:"+vname+","+vdisk+","+vram#create VM
				ncsock.send(msg1)
				ncresponse1=ncsock.recv(1024)
				print "response received from nc:",ncresponse1
				ncsock.close()
				c.send(ncresponse1)							

			else:#check in NC2
				print "ncresponse2",ncresponse2
				rcode2,reMsg2=ncresponse2.split(":")
				rdisk2,rram2,rcore2=reMsg2.split(",")
				print "rdisk",rdisk2
				print "rram",rram2
				if (rcode2 =="102"):
					if (rdisk2>vdisk and rram2>vram):
						ncsock = socket.socket() 
						portnc=12346
						ncsock.connect((ipnc2, portnc)) 
						msg1="103:"+vname+","+vdisk+","+vram#create VM
						ncsock.send(msg1)				
							
		
	elif (mcode=="2"):#delete VM request from clc
		modifyVM("105","VM successfully deleted!!","VM not found!!");		
		
	elif (mcode =="3"):# start VM request from clc
		modifyVM("106","VM successfully started!!","VM not found!!");		
			
	elif (mcode =="4"):# start VM request from clc
		modifyVM("107","VM successfully stopped!!","VM not found!!");
	c.send(ncresponse)
	c.close()                
