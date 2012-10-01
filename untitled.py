from fabric.api import *
'''
	1 git pull the newest data code 
	2 configure mysql 
	3 configure nginx
	4 replace the data base
	5 restart mysql
	6 restart nginx
'''
env.GIT_REPO_URL= 'git@github.com:magicshui/vzi.git'
# path to store code base
env.REMOTE_CODEBASE_PATH = '/home/ubuntu/temp/vzi'
# path to install pip file
env.PIP_REQUIREMENTS_PATH ='%s/requirements.pip' %env.REMOTE_CODEBASE_PATH
# name of the virtualenv
env.REMOTE_VIRTUAL_NAME = 'vzi'

env.user = 'ubutnu'
env.hosts= ['http://movie.shui.us']

# aws-db-vzi
# ubuntu
# shuishui123
def git_setup():
	print('=== CLONE FROM GITHUB ===')
	with cd(os.path.dirname(env.REMOTE_CODEBASE_PATH)):
		# git clone the base database
		run("git clone %s %S"%(env.GIT_REPO_URL,os.path.basename(env.REMOTE_CODEBASE_PATH)))
	with cd(os.path.join(env.REMOTE_CODEBASE_PATH,))
def database_migrate():
	pass
def pack():
	pass


def git_pull():
	# pull the newest data base to one folder /temp
	# then copy it to the new database
	run()
	# remove the data
	run('rm %s'%PRODUCTION_FOLDER)
	pass

def deploy_nginx(restart=True):
	# configure nginx
	# 
	# restart nginx
	run("/etc/init.d/nginx restart")
	pass
def configure_nginx():
	pass
def configure_mysql():
	pass
