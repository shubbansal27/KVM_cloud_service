import socket     

ipnc1 ='10.42.0.1'
ipnc2='10.42.0.253'
ipclc='10.42.0.38'
ipcc='10.42.0.38'

def splitterInt(st):
	return map(int,st.split(","))

s = socket.socket()         
host = socket.gethostname() 
portclc = 12345                
s.bind((ipcc, portclc))        
s.listen(5)       
          
while True:
	c, addr = s.accept()     
	clcRequest= c.recv(1024)
	mcode,rReq=clcRequest.split(":")
	if(mcode=="1"):
		vname,vdisk,vram,vcore = rReq.split(",")#new VM config
		ncsock1 = socket.socket() 
		portnc=12346
		ncsock1.connect((ipnc1, portnc)) 
		msg="101"#free disk and RAM in NC
		ncsock1.send(msg)	   
		aReq1=ncsock1.recv(1024)
		print aReq1
		ncsock1.close()
		ncsock2 = socket.socket() 
		portnc=12346
		ncsock2.connect((ipnc2, portnc)) 
		msg2="101"
		ncsock2.send(msg2)	   
		aReq2=ncsock2.recv(1024)
		print aReq2
		ncsock2.close()	
		#rq=splitterInt(rReq)
		rq = map(float,rReq.split(",")[1:])
		#aRq1=splitterInt(aReq1)
		rcode,reMsg=aReq1.split(":")		
		aRq1=map(float,reMsg.split(","))
		#aRq2=splitterInt(aReq2)
		rcode2,reMsg2=aReq2.split(":")		
		aRq2=map(float,reMsg2.split(","))
		if(rq[1]<aRq1[1] and rq[1]<aRq2[1]):
			frg1=aRq1[1]-rq[1]
			frg2=aRq2[1]-rq[1]
			if(frg1<frg2):
				ncsock = socket.socket() 
				portnc=12346
				ncsock.connect((ipnc1, portnc)) 
				msg1="103:"+vname+","+vdisk+","+vram#create VM
				ncsock.send(msg1)
				ncresponse1=ncsock.recv(1024)
				print "response received from nc:",ncresponse1
				ncsock.close()
				c.send(ncresponse1)	
			else:
				ncsock = socket.socket() 
				portnc=12346
				ncsock.connect((ipnc2, portnc)) 
				msg1="103:"+vname+","+vdisk+","+vram#create VM
				ncsock.send(msg1)
				ncresponse2=ncsock.recv(1024)
				print "response received from nc:",ncresponse2
				ncsock.close()
				c.send(ncresponse2)
	
		elif(rq[1]<aRq1[1]):
			ncsock = socket.socket() 
			portnc=12346
			ncsock.connect((ipnc1, portnc)) 
			msg1="103:"+vname+","+vdisk+","+vram#create VM
			ncsock.send(msg1)
			ncresponse1=ncsock.recv(1024)
			print "response received from nc:",ncresponse1
			ncsock.close()
			c.send(ncresponse1)	
		elif(rq[1]<aRq2[1]):
			ncsock = socket.socket() 
			portnc=12346
			ncsock.connect((ipnc2, portnc)) 
			msg1="103:"+vname+","+vdisk+","+vram#create VM
			ncsock.send(msg1)
			ncresponse2=ncsock.recv(1024)
			print "response received from nc:",ncresponse2
			ncsock.close()
			c.send(ncresponse2)
		'''
		elif((valNc=createVM)>0):
			#create Vm on valNc

		else:
			#not possible

		'''
