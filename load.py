# encoding:utf-8
from __future__ import print_function
import os
import shutil
PROJECT = r"D:\project\CoDeSys\HMI\a.project"

from_folder=r'D:\Gitlab\codesys\Yao'


def check(func):
    def wrapper(proj,path,name):  # 指定宇宙无敌参数
		#call func
		func(proj,path,name)
		#check
		name=name.split(".")[0]
		found = proj.find(name, False)
		assert(found is not None and len(found) == 1, 'No object with the name {0} found '.format(name))
		#assert(found[0].is_folder, 'Found object is not a folder')
		item = found[0]
		return item
    return wrapper  # 返回


def insert_text(proj,path,name):
	with open(path,'r') as f:
		text = f.read()
		index = text.find('(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n')
		
		if index >=0:
			t1= text[index:].replace('(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n','')
			proj.textual_implementation.replace(t1)
			#print(name+"*** t1")
			try:
				t1= text[:index].replace('(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n','')
				proj.textual_declaration.replace(t1)
			except:
				pass
			
		else:
			t1= text.replace('(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)\r\n','')
			proj.textual_declaration.replace(t1)

	
def export_visu(projects):
	proj = projects.primary
	device = proj.find('_3S_Testspec_Device')[0]
	device.export_xml(reporter, ExportFileName, recursive = True)

def create_taskconfig(proj,path,name):
	proj = proj.create_task_configuration()
	return proj
	#projects.primary.import_native(path)
	
	
def create_task(proj,path,name):
	name=name.split('.')[0]
	proj.import_native(path)
	
	
def create_task_old(proj,path,name):
	name=name.split('.')[0]
	proj=proj.create_task(name)
	
	pou_names=[]
	interval=''
	priority=''
	kindOftask=''
	try:

		with open(path,'r') as f:
			t=f.readline()
			pou_names=t.split("=")[1].replace("\r","").replace("\n","").split(',')
			t=f.readline()
			interval=t.split("=")[1].replace("\r","").replace("\n","")
			t=f.readline()
			kindOftask=t.split("=")[1].replace("\r","").replace("\n","")
	except:
		system.ui.info('open file:\n{0} \nfailed!'.format(path))
		return
	try:
		proj.interval=interval
		proj.priority=priority
	
		for i in pou_names:
			if i:
				try:
					proj.pous.add(i)
				except:
					pass
	
		proj.kind_of_task= kindOftask		
	except:
		pass
		
		
@check		
def create_dev(proj,path,name):
	type=0
	id=''
	ver=''
	
	with open(os.path.join(path,name),'r') as f:
		type=f.readline()
		type=int(type.split("=")[1].replace("\r\n",""))
		id=f.readline()
		id=id.split("=")[1].replace("\r","").replace("\n","")
		ver=f.readline()
		ver=ver.split("=")[1].replace("\r","").replace("\n","")
		
	#system.ui.info("create device:\ntype:{0}\nid:{1}\nver:{2}".format(type,id,ver))
	
	devId = device_repository.create_device_identification(type, id, ver)
	devDesc = device_repository.get_device(devId)
	
	if devDesc is None:
		system.ui.info("create device ERR:\n{0}\n{1}\n{2}".format(type,id,ver))
		raise Exception('No WinV3 PLC available in device repo')
	
	name=name.split('.')[0]
	# Add PLC to an empty project using a DeviceId instance
	proj.add(name, devId)



def create_app(proj,path,name):
	pass
	
@check	
def create_pou(proj,path,name):
	name=name.split('.')[0]
	proj.create_pou(name, PouType.Program)
	
@check	
def create_gvl(proj,path,name):
	name=name.split(".")[0]
	proj.create_gvl(name)
	
@check
def create_property(proj,path,name):
	name=name.split(".")[0]
	proj.create_property(name)
	

def create_method(proj,path,name):
	name=name.split(".")[0]
	proj = proj.create_method(name)
	return proj
	
def create_act(proj,path,name):
	name=name.split(".")[0]
	try:
		proj = proj.create_action(name)
	except:
		system.ui.info("create action:{0}\nfailed".format(name))
			
	return proj

@check
def create_folder(proj,path,name):
	proj.create_folder(name)

@check	
def create_fb(proj,path,name):
	name=name.split('.')[0]
	proj.create_pou(name, PouType.FunctionBlock)
	
@check
def create_fuction(proj,path,name):
	name=name.split(".")[0]
	proj.create_pou(name,PouType.Function)

@check	
def create_itf(proj,path,name):
	name=name.split(".")[0]
	proj.create_interface(name)
	found = proj.find(name, False)
	
	
def create_dut(proj,path,name):
	name=name.split(".")[0]
	item=proj.create_dut(name,DutType.Union)
	
	return item
	
def add_library(proj,path,name):
	name=name.split(".")[0]
	#system.ui.info("add library:{0}".format(name))
	proj.import_native(path)
	

def add_textlist(proj,path,name):
	name=name.split(".")[0]
	try:
		proj=proj.create_textlist(name)
		proj.importfile(path)
		
	except:
		pass
		
@check	
def add_prop_method(proj,path,name):
	name = name.split(".")[0]
	
	
	
def walk_folder(proj,path,tp):
	
	curpath=path
	
	for fi in os.listdir(curpath):
		sub_path = os.path.join(curpath,fi)
		is_folder = os.path.isdir(sub_path)
		stp= fi.split('.')
		
		fn=stp[0]
		try :
			stp=stp[1]
		except:
			stp=''
			
		if tp!='' and tp==stp and not is_folder:
			insert_text(proj,sub_path,fi)
		else:
			if stp=='dev':

				sub_proj= create_dev(proj,sub_path,fi)
				sub_path=os.path.join(sub_path,'Plc Logic')
				sub_proj=sub_proj.find('Plc Logic',False)[0]
				if not sub_proj :
					raise Exception('No PLC Logic in device')
				
				for sfi in os.listdir(sub_path):
					sub_sub_path= os.path.join(sub_path,sfi)
					sub_sub_proj=sub_proj.find(sfi,False)[0]
					if sub_sub_proj :
						walk_folder(sub_sub_proj,sub_sub_path,'app')
					else:
						sub_sub_proj = create_app(sub_sub_proj,sub_sub_path,sfi)
						walk_folder(sub_sub_proj,sub_sub_path,'app')
			
			elif stp=='pou':
				sub_proj= create_pou(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'pou')

			elif stp=='itf':
				sub_proj= create_itf(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'itf')
			
			elif stp=='gvl' : #gvl resistant
				sub_proj=create_gvl(proj,sub_path,fi)
				#system.ui.info("GVL:"+sub_path)
				insert_text(sub_proj,sub_path,fi)
				
			elif stp=='prop':
				sub_proj=create_property(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'prop')
					
			elif stp=='pm': #property method
				sub_proj = add_prop_method(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'pm')
				
			elif stp=='m': #method 
				sub_proj=create_method(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'m')
					
			elif stp=='act': #action 
				sub_proj=create_act(proj,sub_path,fi)
				if not is_folder:
					insert_text(sub_proj,sub_path,fi)
				else:
					walk_folder(sub_proj,sub_path,'act')
					
			elif stp=='dut':
				sub_proj=create_dut(proj,sub_path,fi)
				insert_text(sub_proj,sub_path,fi)
			
			elif stp=='tc': #task configuration
				sub_proj=create_taskconfig(proj,sub_path,fi)
				if is_folder:
					walk_folder(sub_proj,sub_path,'tc')
			elif stp=='task':
				create_task(proj,sub_path,fi)
			
			elif stp=='': #folder
				sub_proj=create_folder(proj,sub_path,fi)
				walk_folder(sub_proj,sub_path,tp)
				
			elif stp=='lib':
				add_library(proj,sub_path,fi)
				
			elif stp=='tl': # textlist
				add_textlist(proj,sub_path,fi)
				
			elif stp=='gtl': #global_textlist
				add_textlist(proj,sub_path,fi)
			else:
				pass

if projects.primary:
	projects.primary.close()

proj = projects.create(PROJECT)

walk_folder(proj,from_folder,'')


system.ui.info("ok")