# -*- coding: utf-8 -*-
"""
@Name: envcheck.py.py 
@Auth: lmz
@Date: 2024/2/20
@Time: 14:30:03
@Desc: 
需求描述：环境检查
1.检查路径是否存在：
/data/logs/
/data/logs/supervisor
不存在则批量创建文件夹

2.批量创建supervisor进程所需要的日志文件夹名、conf文件名
命名方式：
sh文件名：superv-name.sh
conf文件名：superv-name.conf
日志名：superv-name.log
日志文件夹名：superv-name
路径：
/etc/supervisor/conf.d/superv-name.conf
/data/logs/superv-name/superv-name.log
/home/deploy/superv-name.sh

3.批量创建superv-name.conf文件
文件内容编写，提取共同内容（唯一变动的是command和日志名修改）
创建文件夹：mkdir -p 创建不存在的文件夹，省检查是否存在该文件夹
eg：
mkdir -p /2/3/4/5
tree 2

4.根据模板生成.conf文件

需求解析：
思路：
"""
import pathlib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

TEMPLATE_PATH = pathlib.Path(__file__).parent.joinpath("supervisor_ini.conf")
RESULT_PATH = ""

dirname = ['grafana', 'tcpreplay', 'monitor']
import subprocess
from string import Template

"""
怎么可扩充呢？
1.日志、conf文件
2.执行脚本，当前文件夹，（其余文件夹还要拷贝脚本文件）
3.grafana，直接写入conf文件，命令直接执行，主要是.node路径和命令
4.monitor，执行python文件，脚本路径和命令
5.tcpreplay，执行回放，包路径和命令
"""


# grafana:
def req_node(serverip="192.168.67.251", clientip="192.168.67.250"):
	"""
	# 注册node_exporter服务
	:param ip:
	:return:
	"""
	print(f"serverip:{serverip},clientip:{clientip}")
	url = "http://" + serverip + ":8500/v1/agent/service/register"
	# url = "http://" + serverip + ":8500/ui/dc1/services"
	print(url)
	data = {
		"id": "node-exporter-" + clientip,
		"name": "node-exporter-" + clientip,
		"address": clientip,
		"port": 9100,
		"tags": ["firewall-develop-device"],
		"checks": [{
			"http": "http://" + clientip + ":9100/metrics",
			"interval": "5s"
		}]
	}

	# response=requests.post(url, json=data) # post方法会返回405
	response = requests.put(url, json=data)  # curl 的PUT 和request 中的put方法对应
	print("Return registration results", response)


def generate_txt(TEMPLATE_PATH, RESULT_PATH, supervname, scriptpath, scriptcmd, logname):
	"""
	填充supervisor.conf模板
	"""
	with open(TEMPLATE_PATH, mode="r", encoding="utf-8") as r_f, open(
			RESULT_PATH, mode="w", encoding="utf8"
	) as w_f:
		template_content = r_f.read()
		print(f"template_content:{template_content}")
		template = Template(template_content)
		data = template.substitute(SUPERVNAME=supervname, SCRIPTPATH=scriptpath, SCRIPCOMMAND=scriptcmd,
								   LOGFILE=logname)
		w_f.write(data)


# 定义一个函数,用于执行系统命令
def run_comand(command):
	try:
		# 执行命令,获取输出
		result = subprocess.run(command, shell=True, capture_output=True, check=True)
		# 打印输出
		print(result.stdout.decode())
		print(result.stderr.decode())
	except:
		print(f"执行命令失败:{command}")


import requests

# 定义创建目录和日志文件的命令
for name in dirname:
	supervname = 'superv-' + name
	confpath = '/etc/supervisor/conf.d/'
	confname = confpath + supervname + '.conf'
	logpath = '/data/logs/' + supervname
	logname = logpath + '/' + supervname + '.log'
	scriptpath = ''
	# scriptname = scriptpath + supervname + '.sh'
	commands = [
		f"mkdir -p {confpath} {logpath}",
		f"touch {confname} {logname}",
	]
	for command in commands:
		run_comand(command)
	scriptcmd = ""
	if name == "grafana":
		# 下载解压node_exporter
		run_comand(f'tar -xf node_exporter-1.6.1.linux-amd64.tar.gz -C /home')
		scriptpath = "/home/node_exporter-1.6.1.linux-amd64"  # node路径
		# 处理node
		scriptcmd = '/bin/bash -c "./node_exporter --web.listen-address 0.0.0.0:9100"'
	elif name == "tcpreplay":
		# 下载并解压
		scriptpath = ""  # 包的路径
		scriptcmd = f'bash '
	elif name == "monitor":
		scriptcmd = 'python3 monitor_table.py'
	RESULT_PATH = confname
	generate_txt(TEMPLATE_PATH, RESULT_PATH, supervname, scriptpath, scriptcmd, logname)

command_start = f"service supervisor restart"
run_comand(command_start)

import sys

# 打印传入的参数
if len(sys.argv) == 3:
	print(f"Server IP: {sys.argv[1]}, Client IP: {sys.argv[2]}")
else:
	print("This script requires exactly two arguments.")
req_node(sys.argv[1], sys.argv[2])

