#################################### NC #####################
import socket
from random import randint
from Module_NC import NC_Module
from Module_VM import VM_Module     

ipnc='10.42.0.1'
ipclc='10.42.0.191'
ipcc='10.42.0.38'
#ipnc = ipclc


s = socket.socket()         
host = socket.gethostname() 
port = 12346                
s.bind((ipnc, port))        

s.listen(5)                 
while True:
	c, addr = s.accept()    
	recievedData = c.recv(1024)	 
	print 'recieved from cc: ', recievedData 	
	messageCode = int(recievedData.split(':')[0])
	print "messageCode =====  " , messageCode
   
	if messageCode == 101:

	# here use VM_Module 
	# fetch memory & disk space
		ncModule = NC_Module()  
                ramAvail = ncModule.fetchRamStatus()
		print 'ramAvail = ' + str(ramAvail)                
		c.send('102:160,'+str(ramAvail))
		c.close()   
   
	elif messageCode == 103:
		#create VM
		vmModule = VM_Module()
		
		vmname = recievedData.split(':')[1].split(',')[0]
		ramsize = recievedData.split(':')[1].split(',')[2]
		disksize = recievedData.split(':')[1].split(',')[1]
		vmModule.createVM(vmname,ramsize,disksize)
		vmModule.startVM(vmname)
		vmModule.destroyKVM()

		print('---end---')
		c.send("104:VM created successfully. [ip=192.168.1.1, port=2525]")
		print('----message sent----')
        	c.close()

	elif messageCode == 105: #delete
		print("Calling delete VM")
		 vmname = recievedData.split(':')[1].split(',')[0]

		vmModule = VM_Module()
		if(vmModule.checkVMExistence(vname) == 1):
			vmModule.removeVM(vname)
			c.send("1")
		else:
			c.send("-1")
		
        	vmModule.destroyKVM()
		c.close()


 	elif messageCode == 106: #start
		print("calling start VM")
		vmModule = VM_Module()
		if(vmModule.checkVMExistence(vname) == 1):
               		vmModule.startVM(vmname)
			c.send("1")
                else:
                        c.send("-1")

                vmModule.destroyKVM()
		c.close()
			
	elif messageCode == 107: #stop
		print('calling stop VM')
		vmModule = VM_Module()
		if(vmModule.checkVMExistence(vname) == 1):
                	vmModule.destroyVM(vmname)
               		c.send("1")
                else:
                        c.send("-1")
		
                vmModule.destroyKVM()
		c.close()	
	

