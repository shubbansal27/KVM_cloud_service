from __future__ import division
import sys
import subprocess
import psutil

class NC_Module:

	def __init__(self):
		print 'object created'

        def fetchRamStatus(self):
                #subprocess.check_call(['virsh', 'setmaxmem',vmname, ramsize,'--config'])
                memory = psutil.virtual_memory()
                return memory.available/(1024*1024)   #in MB 
		#return memory


		def fetchDiskStatus(self):
                #subprocess.check_call(['virsh', 'setmaxdisk',vmname, disksize,'--config'])
                memory = psutil.virtual_memory()
                return memory.available/(1024*1024)   #in MB 

		
		def fetchCoreStatus(self):
                #subprocess.check_call(['virsh', 'setcorestate',vmname, coresize,'--config'])
                memory = psutil.virtual_memory()
                return memory.available/(1024*1024)   #in MB 

		def TcpConnects(self):
                #subprocess.check_call(['virsh', 'setmaxtcp',vmname, tcpcon,'--config'])
                memory = psutil.virtual_memory()
                return memory.available/(1024*1024)   #in MB 

				
		def ApacheServerStatus(self):
                #subprocess.check_call(['virsh', 'setmaxconn',vmname, serverconfig,'--config'])
                memory = psutil.virtual_memory()
                return memory.available/(1024*1024)   #in MB 


			
#a = NC_Module()
#a.fetchRamStatus()











