import paramiko
import time
import os
import os.path
import datetime
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
LOG_FILE = '/home/backup-Log.txt'
#LOG_FILE = 'D:/BACKUP/backup-log.txt'
LOG_FILE = open(LOG_FILE, 'a')
total = 0
success = 0
failed = 0
fi = 0
custvfw = 0
custvfwsuccess = 0
netdevice = 0
netdevicesuccess = 0
execerror = ''
e_to = []
username = 'abc'
password = 'pass'
#Email
e_smtp_server = 'alerts.abc.co.in'
e_smtp_port = 25
e_from = 'network.backup@alerts.abc.co.in'
EID_LIST = open ('/home/to-email-ids.txt')
#EID_LIST = open ('D:/abc/IMP/BACKUP/to-email-ids.txt')
for e_id in EID_LIST:
	e_id = e_id.rstrip('\n')
	e_id = e_id.strip()
	fi = fi + 1
	e_to.append(fi-1)
	e_to[fi-1] = e_id
#email password
e_password = 'pass'
try:
	msg = MIMEMultipart()
	msg['From'] = e_from
	msg['To'] = ','.join(e_to)
	msg['Subject'] = "Device config Backup to Start"
	body = "\n Device config backup to start"
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP(e_smtp_server, e_smtp_port)
	server.starttls()
	server.login(e_from, e_password)
	text = msg.as_string()
	server.sendmail(e_from, e_to, text)
	server.quit()
except Exception as err:
   LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) + ' Email failed error - ' + str(err) + ' \n\n')
SWITCH_LIST = open ('/home/Device_IP_list.txt')
#SWITCH_LIST = open ('D:/abc/IMP/BACKUP/IP.txt')
#print(str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute))
for RTR in SWITCH_LIST:
	try:
		custifcount = 0
		netifcount = 0
		#time.sleep(5)
		RTR = RTR.rstrip('\n')
		RTR=RTR.strip()
		total = total + 1
		if RTR == 'ip':
			#netdevice = netdevice + 1
			backupfilename = '/home/custvfirewall/' + RTR
			#backupfilename = 'D:/abc/IMP/BACKUP/' + RTR
			custvfw = custvfw + 1
		else:
			backupfilename = '/home/netbackup/' + RTR
			netdevice = netdevice + 1
		if not os.path.exists(backupfilename):
			os.makedirs(backupfilename)            
#       #backupfilename = os.path('E:/SW/BACKUP0/', RTR ,'/')
#		#backupfilename= os.path.join(backupfilename, RTR)
			time.sleep(10)
		LOG_FILE.write( '\n======  ' + (str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) + '  device ' + RTR + '   ====== \n')
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2)  +' Backup server to device ' + RTR + ' initiating connection \n')
#        print ('\n ###CONNECTING TO abc' + RTR + '### \n')
		ssh = paramiko.SSHClient() 
#        #For devices with TACACS enabled or with local backup user ########
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(RTR.strip(),port=22,username=username,password=password)
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#ssh.connect(RTR.strip(),port=22,username=username,password=password)        
		time.sleep(4)
		SWITCH_ACCESS = ssh.invoke_shell()
		time.sleep(5)
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +' Backup server to  device ' + RTR + ' connected \n')
		#For Dell switches  ########################
	#     SWITCH_ACCESS.send(b'terminal length 0\n')        
	#     SWITCH_ACCESS.send(b'show running-conf\n')
	#     #time.sleep(1)
	#     #netdevicesuccess = netdevicesuccess + 1	
			#For customer vFirewall ####
		if RTR == 'IP':
			#Palo Alto
			SWITCH_ACCESS.send(b'set cli pager off\n')
			SWITCH_ACCESS.send(b'configure\n')
			SWITCH_ACCESS.send(b'show\n') 
			#Fortigate
			SWITCH_ACCESS.send(b'config global\n')
			SWITCH_ACCESS.send(b'config system console\n')
			SWITCH_ACCESS.send(b'set output standard\n')
			SWITCH_ACCESS.send(b'end\n')
			SWITCH_ACCESS.send(b'show full-configuration\n')
			time.sleep(25)
			custifcount = 1
			#for network devices (switches, routers, mgmt firewalls etc.)
			#Dell or Cisco
			SWITCH_ACCESS.send(b'terminal length 0\n')        
			SWITCH_ACCESS.send(b'show running-conf\n')
			#Juniper
			SWITCH_ACCESS.send(b'set cli screen-length 0\n')
			SWITCH_ACCESS.send(b'show configuration | display set\n')
			#Fortigate
			SWITCH_ACCESS.send(b'config system console\n')
			SWITCH_ACCESS.send(b'set output standard\n')
			SWITCH_ACCESS.send(b'end\n') 
			SWITCH_ACCESS.send(b'show full-configuration\n')
			time.sleep(25)
			netifcount = 1
		# else:
		#netdevicesuccess = netdevicesuccess + 1
		#time.sleep(25)
		output = SWITCH_ACCESS.recv(99)
		time.sleep(2)
		print (output.decode('ascii'))
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +' Configuration of  device ' + RTR + ' copied \n')
		#save_path = (backupfilename,datetime.datetime.now())
		backupfilename = (backupfilename + '/' + (str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ '-' + (str(datetime.datetime.now().hour)).zfill(2)+'-' + (str(datetime.datetime.now().minute)).zfill(2)+ '-' + (str(datetime.datetime.now().second)).zfill(2)+ '.txt')
		SAVE_FILE = open(backupfilename, 'w+')
		#time.sleep(10)
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +' Configuration of  device ' + RTR + ' writing on backup server \n')
		SAVE_FILE.write(output.decode("ascii"))
		#SAVE_FILE.write(str(output))
		SAVE_FILE.close()      
		ssh.close()
		#        print ("Back up is successfull "+ RTR)
		success = success + 1
		if custifcount == 1:
			custvfwsuccess = custvfwsuccess + 1
		if netifcount == 1:
			netdevicesuccess = netdevicesuccess + 1
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +'  device ' + RTR + ' backup success \n')
	except:
		execerror = execerror + '\n' + RTR
		#LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +'  device ' + RTR + '  ' + str(erf) + ' \n\n')
		LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +'  device ' + RTR + ' backup failed \n\n')


failed = total - success
LOG_FILE.write(('\n' + str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) +' Total devices = ' + str(total) + ' (Net-devices = ' + str(netdevice) + ' + cust-v-fw = ' + str(custvfw) + ');'+ ' Backup Success = ' + str(success) + ' (Net-devices = ' + str(netdevicesuccess) + ' + cust-v-fw = ' + str(custvfwsuccess) + ');' + ' failed = ' + str(failed) + ' (Net-devices = ' + str(netdevice - netdevicesuccess) + ' + cust-v-fw = ' + str(custvfw - custvfwsuccess) + ');' + ' \n\n')
pathn = '/home/admin/device-backups/netbackup/'
pathc = '/home/admin/device-backups/custvfirewall/'
dsizen = subprocess.check_output(['du','-sh', pathn]).split()[0].decode('utf-8')
dsizec = subprocess.check_output(['du','-sh', pathc]).split()[0].decode('utf-8')
if dsizen[-1] == 'T' or dsizec[-1] == 'T':
	dsizechar = 'T'
elif dsizen[-1] == 'G' or dsizec[-1] == 'G':
	dsizechar = 'G'
elif dsizen[-1] == 'M' or dsizec[-1] == 'M':
	dsizechar = 'M'
elif dsizen[-1] == 'K' or dsizec[-1] == 'K':
	dsizechar = 'K'
try:
	dsizen = float(dsizen)
except:
	dsizenr = dsizen[-1]
	dsizen = dsizen[:-1]
try:
	dsizec = float(dsizec)
	dsizecr = ""
except:
	dsizecr = dsizec[-1]
	dsizec = dsizec[:-1]
#print('\nTotal size =  ' + str(float(dsizec)+float(dsizen)) + '; Net backup size = ' + str(dsizen) +'; Customer Firewall backup size = ' + str(dsizec))
backupsize = ('\nTotal size =  ' + str(float(dsizec)+float(dsizen)) + dsizechar + 'B; Net backup size = ' + str(dsizen) + dsizenr + 'B; Customer Firewall backup size = ' + str(dsizec) + dsizecr + 'B')
if failed != 0 and total != failed:
	msg = MIMEMultipart()
	msg['From'] = e_from
	msg['To'] = ','.join(e_to)
	msg['Subject'] = " config backup failed for " + str(failed) + " devices"
	body = "\n" + (str(datetime.datetime.now().day)).zfill(2) + "-" + (str(datetime.datetime.now().month)).zfill(2)+ "-" + (str(datetime.datetime.now().year)).zfill(4)+ " " + (str(datetime.datetime.now().hour)).zfill(2)  + ":" + (str(datetime.datetime.now().minute)).zfill(2)+ ":" + (str(datetime.datetime.now().second)).zfill(2) + "\n\nTotal devices = " + str(total) + " (Net-devices = " + str(netdevice) + " + cust-v-fw = " + str(custvfw) + ");"+ "\n\nBackup Success = " + str(success) + " (Net-devices = " + str(netdevicesuccess) + " + cust-v-fw = " + str(custvfwsuccess) + ");" + "\n\nfailed = " + str(failed) + " (Net-devices = " + str(netdevice - netdevicesuccess) + " + cust-v-fw = " + str(custvfw - custvfwsuccess) + ");" + "\n" + backupsize + "\n\n Backup Server: BackupServerIP   Path: /home/admin/device-backups/ \n\nList of failed devices IPs" + execerror
elif total == failed:
	msg = MIMEMultipart()
	msg['From'] = e_from
	msg['To'] = ','.join(e_to)
	msg['Subject'] = " config backup failed for all " + str(failed) + " devices"
	body = "\n" + (str(datetime.datetime.now().day)).zfill(2) + "-" + (str(datetime.datetime.now().month)).zfill(2)+ "-" + (str(datetime.datetime.now().year)).zfill(4)+ " " + (str(datetime.datetime.now().hour)).zfill(2)  + ":" + (str(datetime.datetime.now().minute)).zfill(2)+ ":" + (str(datetime.datetime.now().second)).zfill(2) + "\n\nTotal devices = " + str(total) + " (Net-devices = " + str(netdevice) + " + cust-v-fw = " + str(custvfw) + ");"+ "\n\nBackup Success = " + str(success) + " (Net-devices = " + str(netdevicesuccess) + " + cust-v-fw = " + str(custvfwsuccess) + ");" + "\n\nfailed = " + str(failed) + " (Net-devices = " + str(netdevice - netdevicesuccess) + " + cust-v-fw = " + str(custvfw - custvfwsuccess) + ");" + "\n" + backupsize + "\n\n Backup Server: BackupServerIP   Path: /home/admin/device-backups/ \n\nList of failed devices IPs" + execerror
elif total == success:
	msg = MIMEMultipart()
	msg['From'] = e_from
	msg['To'] = ','.join(e_to)
	body = ""
	msg['Subject'] = " config backup success for all " + str(success) + " devices"
	body = "\n" + (str(datetime.datetime.now().day)).zfill(2) + "-" + (str(datetime.datetime.now().month)).zfill(2)+ "-" + (str(datetime.datetime.now().year)).zfill(4)+ " " + (str(datetime.datetime.now().hour)).zfill(2)  + ":" + (str(datetime.datetime.now().minute)).zfill(2)+ ":" + (str(datetime.datetime.now().second)).zfill(2) + "\n\nTotal devices = " + str(total) + " (Net-devices = " + str(netdevice) + " + cust-v-fw = " + str(custvfw) + ");"+ "\n\nBackup Success = " + str(success) + " (Net-devices = " + str(netdevicesuccess) + " + cust-v-fw = " + str(custvfwsuccess) + ");" + "\n\nfailed = " + str(failed) + " (Net-devices = " + str(netdevice - netdevicesuccess) + " + cust-v-fw = " + str(custvfw - custvfwsuccess) + ");" + "\n" + backupsize + "\n\n Backup Server: BackupServerIP   Path: /home/admin/device-backups/\n"
try:
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP(e_smtp_server, e_smtp_port)
	server.starttls()
	server.login(e_from, e_password)
	text = msg.as_string()
	server.sendmail(e_from, e_to, text)
	server.quit()
except Exception as err:
	LOG_FILE.write((str(datetime.datetime.now().day)).zfill(2)+ '-' + (str(datetime.datetime.now().month)).zfill(2)+ '-' + (str(datetime.datetime.now().year)).zfill(4)+ ' ' + (str(datetime.datetime.now().hour)).zfill(2)+':' + (str(datetime.datetime.now().minute)).zfill(2)+ ':' + (str(datetime.datetime.now().second)).zfill(2) + ' Email failed error - ' + str(err) + ' \n\n')
LOG_FILE.close()
#print(str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute))
	
	

