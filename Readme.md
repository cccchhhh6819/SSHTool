ssht.py
=============

### 1. 工具说明
该工具为批量进行SSH登陆、上传、下载、执行命令等所使用的脚本

### 2. 使用所需要的文件
(1)工具同目录下必须有iplist.txt，其内容为对象IPv4地址，每行一个，不支持简写/子网/域名等模式

(2)如需执行命令，需将待执行的命令写入一个指定文件，每条命令一行

### 3. 使用方法
(1)批量执行命令

    ssht.py USERNAME PASSWORD cmd COMMAND_FILE

本方法实现批量执行COMMAND_FILE中的命令，并将结果分IP记录在同目录下的CMDRESULT文件夹中。

(2)批量上传文件

    ssht.py USERNAME PASSWORD upd LOCAL_DIR REMOTE_DIR

本方法实现将本地单个文件夹内全部内容上传至远程服务器的功能。远程目录参数建议为绝对路径。

(3)批量下载文件

    ssht.py USERNAME PASSWORD downd REMOTE_DIR [LOCAL_DIR]

本方法实现远程下载指定目录内容并保存的功能。LOCAL_DIR参数可不写，默认为工具同目录下的DOWNLOAD文件夹。远程目录参数建议为绝对路径。

(4)上传单个文件

    ssht.py USERNAME PASSWORD up LOCAL_FILE REMOTE_DIR

本方法实现将本地单个文件上传至远程服务器的功能。远程目录参数建议为绝对路径。

(5)下载单个文件

    ssht.py USERNAME PASSWORD down REMOTE_FILE [LOCAL_DIR]

本方法实现远程下载单个文件并保存的功能。LOCAL_DIR参数可不写，默认为工具同目录下的DOWNLOAD文件夹。远程目录参数建议为绝对路径。

(6)批量更改密码

    ssht.py USERNAME PASSWORD pass NEWPASSWORD

本方法实现批量修改SSH当前账户密码的功能。（密码应具有一定强度，否则系统处修改不成功）

### 4. 注意事项
- 不支持不同账号密码的同时批量处理
- 下载文件时请注意权限以及文件名大小写
- 上传文件时请确保目标目录存在并可写
- 改密码时请确保更改的密码有一定强度，否则过不了远程服务器验证，程序会直接卡死
- 脚本内有功能注释供参考，使用者可自行修改或增减内容
    