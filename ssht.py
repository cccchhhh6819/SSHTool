#-*- coding: utf-8 -*-
#!/usr/bin/python
import paramiko
import threading
import datetime
import sys
import os
import re

print '##########################'
print '#        SSH Tool        #'
print '#       by Chainer       #'
print '##########################'


#获取输入并处理
if (len(sys.argv)<5) or (len(sys.argv)>6):
	print 'Illegal input, please retry.'
	sys.exit()
SSHT_USERNAME=sys.argv[1]#登陆用户名
SSHT_PASSWORD=sys.argv[2]#登陆密码
SSHT_TYPE=sys.argv[3]#操作类型
SSHT_REMOTEDIR=''#远程目录
SSHT_LOCALDIR=''#本地目录
SSHT_REMOTEFILE=''#单个文件下载时的远程文件路径
SSHT_LOCALFILE=''#单个文件上传时的本地文件路径
SSHT_EXEPATH=''#执行命令操作时的命令文件路径
SSHT_NEWPW=''#修改密码时用的新密码

DEFAULT_PORT=22

#根据输入设置基本参数
if SSHT_TYPE=='cmd':#执行命令
	SSHT_EXEPATH=sys.argv[4]
elif SSHT_TYPE=='upd':#批量上传文件
	if(len(sys.argv)<6):
		print 'Illegal params, please retry.'
		sys.exit()
	SSHT_LOCALDIR=sys.argv[4]
	SSHT_REMOTEDIR=sys.argv[5]
elif SSHT_TYPE=='downd':#批量下载文件
	SSHT_REMOTEDIR=sys.argv[4]
	if(len(sys.argv)==6):
		SSHT_LOCALDIR=sys.argv[5]
	else:
		SSHT_LOCALDIR='./DOWNLOAD'
elif SSHT_TYPE=='up':#上传单个文件
	if(len(sys.argv)<6):
		print 'Illegal params, please retry.'
		sys.exit()
	SSHT_LOCALFILE=sys.argv[4]
	SSHT_REMOTEDIR=sys.argv[5]
elif SSHT_TYPE=='down':#下载单个文件
	SSHT_REMOTEFILE=sys.argv[4]
	if(len(sys.argv)==6):
		SSHT_LOCALDIR=sys.argv[5]
	else:
		SSHT_LOCALDIR='./DOWNLOAD'
elif SSHT_TYPE=='pass':#批量更改密码
	SSHT_NEWPW=sys.argv[4]
else:
	print 'Illegal measure, please retry.'
	sys.exit()


#执行命令操作函数
def sshcmd(ip,cmd):#执行命令
	try:
#		paramiko.util.log_to_file('paramiko_cmd.log')
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,DEFAULT_PORT,SSHT_USERNAME,SSHT_PASSWORD,timeout=5)

		result=open('./CMDRESULT/'+ip+'.txt','a')
		for m in cmd:
			result.write(m+'\n\n')
			stdin,stdout,stderr=ssh.exec_command(m)
			out=stdout.readlines()
			for o in out:
				result.write(o)
			result.write('------------------------------------\n')

		result.close()
		ssh.close()
		print '%s\t Execute CMD Completed.\n'%(ip)
	except:
		print '%s\t Error in executing command.\n'%(ip)


def sshup(ip,localfile,remotedir):#单个文件上传
	if not os.path.exists(localfile):
		print 'file not found, please retry'
		sys.exit()
	try:
#		paramiko.util.log_to_file('paramiko_up.log')
		t = paramiko.Transport((ip, DEFAULT_PORT))
		t.connect(username=SSHT_USERNAME, password=SSHT_PASSWORD)
		sftp = paramiko.SFTPClient.from_transport(t)

		print ('Uploading file:'+localfile)
		sftp.put(localfile, (remotedir+'/'+localfile.split('/')[-1]))
		print 'Upload file success %s ' % datetime.datetime.now()

		t.close()
		print '%s\t Upload Completed.\n'%(ip)
	except:
		print '%s\t Error in uploading file.\n'%(ip)


def sshupd(ip,localdir,remotedir):#批量上传
	try:
#		paramiko.util.log_to_file('paramiko_up.log')
		t = paramiko.Transport((ip, DEFAULT_PORT))
		t.connect(username=SSHT_USERNAME, password=SSHT_PASSWORD)
		sftp = paramiko.SFTPClient.from_transport(t)

		files = os.listdir(localdir)
		for f in files:
			print ('Uploading file:'+localdir+'/'+f)
			sftp.put((localdir+'/'+f), (remotedir+'/'+f))
			print 'Upload file success %s ' % datetime.datetime.now()

		t.close()
		print '%s\t Upload Completed.\n'%(ip)
	except:
		print '%s\t Error in uploading file.\n'%(ip)


def sshdown(ip,localdir,remotefile):#单个文件下载
	localdir=localdir+'/'+ip+'/'
	isExists=os.path.exists(localdir)
	if not isExists:
		os.makedirs(localdir)
	try:
#		paramiko.util.log_to_file('paramiko_down.log')
		t = paramiko.Transport((ip,DEFAULT_PORT))
		t.connect(username=SSHT_USERNAME,password=SSHT_PASSWORD)
		sftp = paramiko.SFTPClient.from_transport(t)

		print ('Downloading file: '+ip+' '+remotefile)
		sftp.get(remotefile, (localdir+remotefile.split('/')[-1]))
		print 'Download file success %s ' % datetime.datetime.now()

		t.close()
		print '%s\t Download Completed.\n'%(ip)
	except:
		print '%s\t Error in downloading file.\n'%(ip)


def sshdownd(ip,localdir,remotedir):#批量下载
	localdir=localdir+'/'+ip+'/'
	isExists=os.path.exists(localdir)
	if not isExists:
		os.makedirs(localdir)
	try:
#		paramiko.util.log_to_file('paramiko_down.log')
		t = paramiko.Transport((ip,DEFAULT_PORT))
		t.connect(username=SSHT_USERNAME,password=SSHT_PASSWORD)
		sftp = paramiko.SFTPClient.from_transport(t)

		files = sftp.listdir(remotedir)
		for f in files:
			print ('Downloading file: '+remotedir+f)
			sftp.get((remotedir+'/'+f), (localdir+'/'+f))
			print 'Download file success %s ' % datetime.datetime.now()

		t.close()
		print '%s\t Download Completed.\n'%(ip)
	except:
		print '%s\t Error in downloading file.\n'%(ip)


def sshpass(ip,newpasswd):#批量修改密码
	try:
#		paramiko.util.log_to_file('paramiko_passwd.log')
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,DEFAULT_PORT,SSHT_USERNAME,SSHT_PASSWORD,timeout=5)

		stdin,stdout,stderr=ssh.exec_command('id')
		result=stdout.read()

		stdin,stdout,stderr=ssh.exec_command("passwd")
		print (ip+' '+result)
		if not ("uid=0" in result):#is not root
			stdin.write("%s\n" % (SSHT_PASSWORD))
		stdin.write("%s\n" % (newpasswd))
		stdin.write("%s\n" % (newpasswd))
		stdout.read()
		error_message = stderr.read()[:-1]
		if "success" in error_message:
			print '%s\t Change Passwd Completed.\n'%(ip)
		else:
			print '%s\t Change Passwd Failed.\n'%(ip)
	except:
		print '%s\t Error in changing passwd.\n'%(ip)

if __name__=='__main__':
	try:
		iplist=open('iplist.txt')
		ips=iplist.readlines()
		iplist.close()
	except:
		print 'IPlist not found!'
		sys.exit()

	for ip in ips:
		ip=ip.strip('\n')
		if(re.match(r"^(25[0-5]|2[0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[1-9])(\.(25[0-5]|2[0-4][0-9]|[1][0-9]{2}|[1-9][0-9]|[0-9])){3}$",ip)):#是正确的IP格式才进行处理
			if SSHT_TYPE=='cmd':#执行命令
				if not os.path.exists('./CMDRESULT'):
					os.makedirs('./CMDRESULT')
				try:
					cmds=open(SSHT_EXEPATH)
					cmd=cmds.readlines()
					cmds.close()
				except:
					print 'Command file not found!'
					sys.exit()
				th=threading.Thread(target=sshcmd,args=(ip,cmd))
				th.start()
			elif SSHT_TYPE=='upd':#批量上传
				th=threading.Thread(target=sshupd,args=(ip,SSHT_LOCALDIR,SSHT_REMOTEDIR))
				th.start()
			elif SSHT_TYPE=='downd':#批量下载
				if not os.path.exists(SSHT_LOCALDIR):
					os.makedirs(SSHT_LOCALDIR)
				th=threading.Thread(target=sshdownd,args=(ip,SSHT_LOCALDIR,SSHT_REMOTEDIR))
				th.start()
			elif SSHT_TYPE=='up':#单个文件上传
				th=threading.Thread(target=sshup,args=(ip,SSHT_LOCALFILE,SSHT_REMOTEDIR))
				th.start()
			elif SSHT_TYPE=='down':#单个文件下载
				if not os.path.exists(SSHT_LOCALDIR):
					os.makedirs(SSHT_LOCALDIR)
				th=threading.Thread(target=sshdown,args=(ip,SSHT_LOCALDIR,SSHT_REMOTEFILE))
				th.start()
			elif SSHT_TYPE=='pass':#修改密码
				th=threading.Thread(target=sshpass,args=(ip,SSHT_NEWPW))
				th.start()


