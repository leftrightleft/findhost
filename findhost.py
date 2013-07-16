import paramiko
import re
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-m', help='MAC address')
parser.add_argument('-u', help='Username')
parser.add_argument('-p', help='password')
args = parser.parse_args()
arg_mac = args.m
arg_uname = args.u
arg_pw = args.p

swt_list = ['swt1', 'swt2', 'swt3', 'swt4']


###############################################################################
#This is the function to verify the input of the MAC address - If it's not valid, this 
#function will attempt to correct it and form it as a Cisco compatible MAC (xxxx.xxxx.xxxx)
###############################################################################

def validate_mac():
  lower_mac = arg_mac.lower() #Lowercase the characters
	pattern = re.compile('([0-9a-f]{4}[\.]){2}([0-9a-f]{4})') #Check to see if the MAC address is already valid (Cisco compatible)
	if pattern.findall(lower_mac):
		return lower_mac
	else:
		lower_mac = ''.join(e for e in lower_mac if e.isalnum()) #If not already valid, drop all the special characters and modify it to be compatible
		lower_mac = re.sub(r'(.{4})(?!$)', r'\1.', lower_mac)
		pattern = re.compile('([0-9a-f]{4}[\.]){2}([0-9a-f]{4})')
		if pattern.findall(lower_mac): #Validate that it's good
			return lower_mac
		else:
			print 'MAC in wrong format' #If not good, throw an error
	
###############################################################################
#This is the function to actually connect to the hosts 
###############################################################################

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect():
	try:
		print 'Trying:', host, 
		client.connect(host, username=arg_uname, password=arg_pw)
		stdin, stdout, stderr = client.exec_command('sh mac address-table address %s' % mac)
		output = stdout.read()
		pattern = re.search(r'(\sPo\d+\s)|(\sGi\d+/\d+\s)', output)
		if pattern:
			found = pattern.group()
			print 'Found at:', found, 
			client.close()
		else:
			print 'not found'
	except:
		client.close()
mac = validate_mac()

for host in swt_list:	
	validate_mac()
	connect()
	


	
