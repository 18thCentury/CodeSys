# CodeSys
1. 使用方法:
    在CodeSys 软件内执行脚本
2. 脚本说明:

Export.py:
  将Codesys 内的ST语言的文本数据和Global_var,Textlist 和TaskConfiguration,library 备份到 Save_Folder 文件夹内.如果文件夹内存在.git 文件,则将文件夹更新到HEAD.
  
Load.py:
  将上述文件夹内的导入到一个新工程内.
  
3.问题:
  a. 除ST语言的文本外,其他如:Visu,imagePool,VisuConfiguration,Project Settings,Project Infomation 没有导出.
  b. GlobalTextList 会丢失ID Column 的数据.
