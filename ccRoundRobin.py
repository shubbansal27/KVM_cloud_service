import socket     

ipnc1 ='10.42.0.1'
ipnc2='10.42.0.253'
ipclc='10.42.0.38'
ipcc='10.42.0.38'
def splitterInt(st):
	return map(int,st.split(","))

def decoder(rstat):
	mcode,mdata=rstat.split(":")
	vms=mdata.split(",")
	vmData={}
	for i in vms:
		t=i.split(" ")
		vmData[t[0]]=int(t[1])
	return vmData
'''
def createVM(aReq1,aReq2,rReq):
	rtVal=-1
	ncsock1 = socket.socket() 
	portnc=12346
	ncsock1.connect((ipnc1, portnc)) 
	msg="101"#free disk and RAM in NC
	ncsock1.send(msg)	   
	r1Stat=ncsock1.recv(1024)
	ncsock1.close()
	r1=splitterInt(aReq)
	r2=splitterInt(aReq)
	rq=splitterInt(rReq)
	rstat=""
	rSpc=0
	rMspc=0
	selnc=1
	#request for VMstatus into r2Stat
	#request for VMstatus into r1Stat
	if(r1[1]<r2[1]):		
		rstat=r2Stat
		rSpc=r2[1]
		rMspc=r1[1]
		selnc=2
	else:		
		rstat=r1Stat
		rSpc=r1[1]
		rMspc=r2[1]
		selnc=1
	vmData=decoder(rstat)
	migVms=[]
	flag=0
	for k in vmData:
		migVms.append(k)
		mov=vmData[k]
		rMspc-=mov
		rSpc+=mov
		if(rMspc<0):
			flag=0
			break
		if(rSpc>=rq[1]):
			flag=1
			break
	if(flag==1):
		migSt=migVms[0]
		for i in range(1,len(migVms)):
			migSt=migSt+","+migVms[i]
		#request for Migration of Vms based on selnc
		rtVal=selnc
	else:
		if(selnc==2):
			rstat=r1Stat
			rSpc=r1[1]
			rMspc=r2[1]
			selnc=1
		else:
			rstat=r2Stat
			rSpc=r2[1]
			rMspc=r1[1]
			selnc=2
		vmData=decoder(rstat)
		migVms=[]
		flag=0
		for k in vmData:
			migVms.append(k)
			mov=vmData[k]
			rMspc-=mov
			rSpc+=mov
			if(rMspc<0):
				flag=0
				break
			if(rSpc>=rq[1]):
				flag=1
				break
		if(flag==1):
			migSt=migVms[0]
			for i in range(1,len(migVms)):
				migSt=migSt+","+migVms[i]
			#request for Migration of Vms based on selnc
			rtVal=selnc
		return rtVal
		
'''		
		
		
		
		
	
def checkAvailabilty(aReq,rReq):
	r1 = map(float,aReq.split(",")[1:])
	rcode,reMsg=rReq.split(":")		
	r2=map(float,reMsg.split(","))
	print "r1 =",r1
	print "r2 =",r2
	rtVal=False
	if(r2[0]>=r1[0] and r2[1] >= r1[1]):
		rtVal=True
		print rtVal
	return rtVal
	
cnt=0
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
		if(cnt%2==0):
	
			if(checkAvailabilty(rReq,aReq1)):
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
	
			if(checkAvailabilty(rReq,aReq2)):
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
			else:
				cnt+=2
				#selVm=createVM(aReq1,aReq2,rReq)
				if(selNc==1):
					#create Vm on Nc1
				elif(selNc==2):
					#create Vm on Nc2
				else:
					#respond cannot create
		'''
		cnt+=1
		
	
		
	
