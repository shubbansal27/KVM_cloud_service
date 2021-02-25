
from __future__ import print_function
import sys
import libvirt
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

class VM_Module:

	originalvm = 'baseVM'
	
	def __init__(self):
		self.conn = libvirt.open('qemu:///system')
		if self.conn == None:
		    print('Failed to open connection to qemu:///system', file=sys.stderr)

	
	def destroyKVM(self):
		self.conn.close()
		


	def createVM(self,vmname,ramsize,disksize):
		#clone an existing (base) VM 
		diskpath = '/var/lib/libvirt/images/'+ vmname + '.img'
		subprocess.check_call(['virt-clone', '--original', self.originalvm , '--name',vmname,'--file',diskpath])
		
		#update RAM		
		xmlpath = '/etc/libvirt/qemu/'+ vmname +'.xml'
		tree = ET.parse(xmlpath) #enter path here
		root = tree.getroot()
		ramsize = int(ramsize) * 1024
		for mry in root.iter('memory'):
			mry.text=str(ramsize)    #enter value here
		for cmry in root.iter('currentMemory'):
			cmry.text=str(ramsize)    #enter value here
		
		tree.write(xmlpath)    #output the changes
		
		# To set the max VM's RAM
		ramsize = str(ramsize)
		subprocess.check_call(['virsh', 'setmaxmem',vmname, ramsize,'--config'])
	

		# To set the actual VM's RAM
		ramsize = str(ramsize)
		p = subprocess.check_call(['virsh', 'setmem',vmname, ramsize,'--config'])

		
			
		#update DISK_SIZE
		disksize = str(disksize) + 'G'
		subprocess.check_call(['qemu-img', 'resize', diskpath,disksize])	
		

	def startVM(self,domName):

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.create() < 0:
			print('Can not boot guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has booted', file=sys.stderr)




	def shutdownVM(self,domName):

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.shutdown() < 0:
			print('Can not shutdown guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has stopped', file=sys.stderr)
	


	def removeVM(self,vmname):
		
		#destroying the VM to be removed. Only required if VM is running.
		self.destroyVM(vmname)
		
		#undefine the VM to be removed.
		self.undefineVM(vmname)
	
		#now delete volume file (i.e disk file)
		pool = self.conn.storagePoolLookupByName('default')
		if pool == None:
			print('Failed to locate any StoragePool objects.', file=sys.stderr)
			return
		
		stgvolname = vmname + '.img'
		stgvol = pool.storageVolLookupByName(stgvolname)
		if stgvol == None:
			print('Failed to locate volume of that VM.', file=sys.stderr)
			return
			
		stgvol.delete(0)

	
	def checkVMExistence(self,domName):
		dom = self.conn.lookupByName(domName)
                if dom == None:
                    return -1
		else:
		    return 1	

 

	def destroyVM(self,domName):

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.destroy() < 0:
			print('Can not force shutdown guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has been forcefully shutdown', file=sys.stderr)

	
	def undefineVM(self,domName): #To undefine the VM
		
		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.undefine() < 0:
			print('Can not undefine VM.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has been undefined', file=sys.stderr)



	def suspendVM(self,domName):

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.suspend() < 0:
			print('Can not suspend guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has been suspended', file=sys.stderr)

	def resumeVM(self,domName):

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.resume() < 0:
			print('Can not resume guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has resumed', file=sys.stderr)	

	def scaleUpVM(self,domName):     #To scale up VM

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.resume() < 0:
			print('Can not resume guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has been scaledUP', file=sys.stderr)	

	
	def scaleDownVM(self,domName):  #To scale Down VM

		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.resume() < 0:
			print('Can not resume guest domain.', file=sys.stderr)
			

		print('Guest '+dom.name()+' has scaled Down', file=sys.stderr)
	
	
	def triggerScaling(self,domName): 
		
		dom = self.conn.lookupByName(domName)
		if dom == None:
		    print('Failed to find the domain '+domName, file=sys.stderr)
		    

		if dom.undefine() < 0:
			print('Can not undefine VM.', file=sys.stderr)
			

		print('Guest RAM'+dom.name()+' is going to get full', file=sys.stderr)

		
#a = VM_Module()
#a.createVM('vm11',1,5)
#a.startVM('baseVM')
#a.removeVM('vm8')
#a.shutdownVM('baseVM')
#a.destroyVM('baseVM')
#a.suspendVM('baseVM')
#a.resumeVM('baseVM')
#a.destroyKVM()




