#CLC code
import socket               

host = socket.gethostname() 
port = 12345  

ipnc='10.42.0.1'
ipclc='10.42.0.191'
ipcc1='10.42.0.38'
ipcc2='10.42.0.191'
#ipnc=ipclc
while True:             
	s = socket.socket()         
	print "1:create VM"
	print "2:delete VM"
	print "3:start VM"
	print "4:stop VM"
	print "Enter your choice"
	chc=raw_input()
	print "Enter Availability Zone :"
	avzone = raw_input()

	if avzone=='1':
		s.connect((ipcc1, port))	
	else:
		s.connect((ipcc2,port))		

	if chc=='1':
		print "Enter the VM name:"
		name=raw_input()
		
		print "Enter the VM Disk size:"
		dsize=raw_input()
		
		print "Enter the VM RAM size:"
		rsize=raw_input()

		print "Enter the number of cores : "
		ncores = raw_input()
		
		msg=chc+":"+name+","+dsize+","+rsize+","+ncores    #+""+

	elif chc=='2':
		print "Enter VM Name : "
		vm_name = raw_input()
		msg=chc+":"+vm_name

	elif chc=='3':
		print "Enter VM Name : "
		vm_name = raw_input()
		msg=chc+":"+vm_name
	elif chc=='4':
		print "Enter VM Name : "
		vm_name = raw_input()
		msg=chc+":"+vm_name
	s.send(msg);
	success_message = s.recv(1024)
	print "response received from cc:",success_message
	s.close() 
