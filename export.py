
# encoding:utf-8
# We enable the new python 3 print syntax
from __future__ import print_function
import os
import shutil
import time
import subprocess
'''
prop_method		= Guid('792f2eb6-721e-4e64-ba20-bc98351056db')
tp				= Guid('2db5746d-d284-4425-9f7f-2663a34b0ebc') #dut
libm			= Guid('adb5cb65-8e1d-4a00-b70a-375ea27582f3')
method_no_ret	= Guid('f89f7675-27f1-46b3-8abb-b7da8e774ffd')
act				= Guid('8ac092e5-3128-4e26-9e7e-11016c6684f2')
fb				= Guid('6f9dac99-8de1-4efc-8465-68ac443b7d08')
itf				= Guid('6654496c-404d-479a-aad2-8551054e5f1e')
folder			= Guid('738bea1e-99bb-4f04-90bb-a7a567e74e3a')
gvl				= Guid('ffbfa93a-b94d-45fc-a329-229860183b1d')
prop			= Guid('5a3b8626-d3e9-4f37-98b5-66420063d91e')
textlist		= Guid('2bef0454-1bd3-412a-ac2c-af0f31dbc40f')
global_textlist	= Guid('63784cbb-9ba0-45e6-9d69-babf3f040511')
Device			= Guid('225bfe47-7336-4dbc-9419-4105a7c831fa')
task_config		= Guid('ae1de277-a207-4a28-9efb-456c06bd52f3')
method			= Guid('f8a58466-d7f6-439f-bbb8-d4600e41d099')
gvl_Persistent	= Guid('261bd6e6-249c-4232-bb6f-84c2fbeef430')
Project_Settings	=Guid('8753fe6f-4a22-4320-8103-e553c4fc8e04')
Plc_Logic			=Guid('40b404f9-e5dc-42c6-907f-c89f4a517386')
Application			=Guid('639b491f-5557-464c-af91-1471bac9f549')
Task				=Guid('98a2708a-9b18-4f31-82ed-a1465b24fa2d')
Task_pou			=Guid('413e2a7d-adb1-4d2c-be29-6ae6e4fab820')
Visualization		=Guid('f18bec89-9fef-401d-9953-2f11739a6808')
Visualization_Manager=Guid('4d3fdb8f-ab50-4c35-9d3a-d4bb9bb9a628')
TargetVisualization	=Guid('bc63f5fa-d286-4786-994e-7b27e4f97bd5')
WebVisualization	=Guid('0fdbf158-1ae0-47d9-9269-cd84be308e9d')
__VisualizationStyle=Guid('8e687a04-7ca7-42d3-be06-fcbda676c5ef')
ImagePool			=Guid('bb0b9044-714e-4614-ad3e-33cbdf34d16b')
Project_Information	=Guid('085afe48-c5d8-4ea5-ab0d-b35701fa6009')
SoftMotion_General_Axis_Pool=Guid('e9159722-55bc-49e5-8034-fbd278ef718f')

'''

print("--- Saving files in the project: ---")

# git 
has_repo=False

save_folder=r'D:\Gitlab\codesys\Yao'

if not os.path.exists(save_folder):
	os.makedirs(save_folder) 
else:
	#非空文件夹 删除多余
	a=os.listdir(save_folder)
	for f in a:
		if not f.startswith("."): #保留 svn,git 目录
			sub_path= os.path.join(save_folder,f)
			if os.path.isdir(sub_path):
				shutil.rmtree(sub_path)
			else:
				os.remove(sub_path)
		elif f==".git":
			has_repo=True

info={}

type_dist={
'792f2eb6-721e-4e64-ba20-bc98351056db':'pm',  #property method
'2db5746d-d284-4425-9f7f-2663a34b0ebc':'dut',  #dut
'adb5cb65-8e1d-4a00-b70a-375ea27582f3':'lib',  #lib manager
'f89f7675-27f1-46b3-8abb-b7da8e774ffd':'m', 	 #method no ret
'8ac092e5-3128-4e26-9e7e-11016c6684f2':'act',  #action 
'6f9dac99-8de1-4efc-8465-68ac443b7d08':'pou',  #pou
'6654496c-404d-479a-aad2-8551054e5f1e':'itf',  #interface 
'738bea1e-99bb-4f04-90bb-a7a567e74e3a':'',	   # folder
'ffbfa93a-b94d-45fc-a329-229860183b1d':'gvl',  #global var
'5a3b8626-d3e9-4f37-98b5-66420063d91e':'prop', #property
'2bef0454-1bd3-412a-ac2c-af0f31dbc40f':'tl',   #textlist
'63784cbb-9ba0-45e6-9d69-babf3f040511':'gtl',  #global textlist
'225bfe47-7336-4dbc-9419-4105a7c831fa':'dev',	 #device
'ae1de277-a207-4a28-9efb-456c06bd52f3':'tc',   #task configuration
'f8a58466-d7f6-439f-bbb8-d4600e41d099':'m',    #method with ret
'261bd6e6-249c-4232-bb6f-84c2fbeef430':'gvl',   #gvl_Persistent
'98a2708a-9b18-4f31-82ed-a1465b24fa2d':'task'
};

def save(text,path,name,tp):
	if not tp:
		tp=''
	else:
		tp='.'+tp
	with open(os.path.join(path,name+tp),'w') as f:
		f.write(text.encode('utf-8'))
'''
def get_mtype(a):
	b=a.text
	b=b.split("\n")
	for a in b: 
		if a.find('FUNCTION_BLOCK ') >=0 :
			return "fb"
		elif a.find("FUNCTION ") >=0:
			return "fct"
		elif a.find('METHOD ')>=0 :
			return "m"
		elif a.find("INTERFACE ")>=0:
			return "itf"
		elif a.find("TYPE ")>=0:
			#
			return "tp"
		elif a.find("PROPERTY ")>=0 or a.find("PROPERTY\r\n")>=0:
			return "prop"
		elif a.find("PROGRAM ")>=0 or a.find("PROGRAM\r\n")>=0:
			return "prg"
		elif a.find("VAR_GLOBAL")>=0 or a.find("VAR_CONFIG") >=0:
			return 'gvl'
	return ""
'''			
	
def print_tree(treeobj, depth,path):
	global info
	#record current Path
	curpath=path 
	isfolder=False
	
	t='' #text
	tp='' #type
	
	# get object name
	name = treeobj.get_name(False)
	id = treeobj.type.ToString()
	
	if id in type_dist:
		tp = type_dist[treeobj.type.ToString()]
	else:
		info[id]=name
		
		
	if treeobj.is_device:
		deviceid = treeobj.get_device_identification()
		t = 'type='+str(deviceid.type) +'\nid=' +str(deviceid.id) + '\nver='+ str(deviceid.version)

	try:
		if treeobj.is_folder :
			#system.ui.prompt('folder:'+u, PromptChoice.YesNo, PromptResult.Yes)
			isfolder=true
			pass
	except:
		pass

	if treeobj.has_textual_declaration :
		t=t+'(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n'
		a=treeobj.textual_declaration
		t=t+a.text
		
	if treeobj.has_textual_implementation:
		t=t+'(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n'
		a=treeobj.textual_implementation
		t=t+a.text
		
	'''	
	if treeobj.is_task_configuration:
		exports=[treeobj]
		projects.primary.export_native(exports,os.path.join(curpath,name+'.tc'))
		
	'''
	
	if treeobj.is_task :
		exports=[treeobj]
		projects.primary.export_native(exports,os.path.join(curpath,name+'.task'))
	
		
	if treeobj.is_libman:
		exports=[treeobj]
		projects.primary.export_native(exports,os.path.join(curpath,name+'.lib'))
	
	if treeobj.is_textlist:
		treeobj.export(os.path.join(curpath,name+'.tl'))
		
	children = treeobj.get_children(False)

	if children or isfolder:
		if tp:
			curpath=os.path.join(curpath,name+'.'+tp)
		else:
			curpath=os.path.join(curpath,name)
		
		if not os.path.exists(curpath):
			os.makedirs(curpath)
			
	if t:
		save(t,curpath,name,tp)

	for child in treeobj.get_children(False):
		print_tree(child, depth+1,curpath)
		

for obj in projects.primary.get_children():
    print_tree(obj,0,save_folder)

with open(os.path.join(save_folder,'s.txt'),'w') as f:
	f.write(str(info))

if has_repo:
	os.chdir(save_folder)
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	subprocess.call('"D:\\Program Files\\Git\\bin\\git.exe" add .', startupinfo=si)
	subprocess.call('"D:\\Program Files\\Git\\bin\\git.exe" commit -m "'+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))+'"', startupinfo=si)
else:
	os.chdir(save_folder)
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	subprocess.call('"D:\\Program Files\\Git\\bin\\git.exe" init', startupinfo=si)#'cd '+ save_folder + " && " + 'git init')
	subprocess.call('"D:\\Program Files\\Git\\bin\\git.exe" add .', startupinfo=si)

	subprocess.call('"D:\\Program Files\\Git\\bin\\git.exe" commit -m "'+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))+'"', startupinfo=si)
print("--- Script finished. ---")
system.ui.info('save ok')