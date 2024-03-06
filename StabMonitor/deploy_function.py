import subprocess
import platform
# 导入pip模块,用于管理Python包
from pip._internal.main import main as pip_main
import os
import sys
# 定义一个函数,用于安装Python包
def install_package(package, source=None):
    try:
        # 如果指定源,使用-i参数添加源
        if source:
            pip_main(["install", "-i", source, package])
        else:
            pip_main(["install", package])
        print(f"{package} 安装成功")
    except:
        print(f"{package} 安装失败")
print("开始安装pip包")
# 安装需要的Python包,指定清华源
libraries = ["psutil", "PrettyTable", "matplotlib", "paramiko"]
for lib in libraries:
    install_package(lib, source="https://pypi.tuna.tsinghua.edu.cn/simple")
print("安装pip包完成")
print("**************************")
import paramiko

host = "10.25.10.110"
username = "user"
password = "Netvine123"
port = 22
# 定义sftp目录
base_dir = "/home/ethr_3"
ethr_dir = f"{base_dir}/pcap/firewall_test/ethr/"
monitor_dir = f"{base_dir}/pcap/firewall_test/monitor/进程监控/"

# 定义本地和远程配置文件
local_file_ethrc_conf = f"{ethr_dir}superv_ethrc.conf"
local_file_ethrs_conf = f"{ethr_dir}superv_ethrs.conf"
conf_dir = "/etc/supervisor/conf.d/"

# 定义创建目录和日志文件的命令
commands = [
    f"mkdir {base_dir}",
    f"mkdir /data/logs",
    f"mkdir /data/logs/superv_ethr",
    f"mkdir /data/logs/superv_monitor",
    f"touch /data/logs/superv_ethr/superv_ethrc.log",
    f"touch /data/logs/superv_ethr/superv_ethrs.log",
    f"touch /data/logs/superv_ethr/superv_monitor.log",
]

# 定义一个函数,用于准备环境
def clean_env():
    # 删除已有目录
    subprocess.run(["rm", "-r", base_dir])

    # 逐步创建目录和文件
    for cmd in commands:
        run_comand(cmd)
    run_comand(f"cd base_dir")
    # # 下载和解压工具包
    # get_alltools()
    # command_tar = f"tar -xvf pcap-play.tar -C {base_dir}"
    # run_comand(command_tar)

    # # 重命名解压后的目录
    # new_dir = "pcap-play"
    # subprocess.run(["mv", f"{base_dir}pcap-play", f"{base_dir}/{new_dir}"])

    # run_comand(f"chmod -R 777 {base_dir}")

## 下载ftp中的文件
def download_file(project_name,file_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)

    with client.open_sftp() as sftp:
        print(f"{project_name}/{file_name}")
        sftp.get(f"{project_name}/{file_name}", f"{base_dir}/{file_name}")
        # sftp.get(f"/home/user/documents/审计系统/测试软件/{file_name}", f"{base_dir}/{file_name}")
    
    client.close()
    print(f"下载{file_name}成功")

# 解压tar文件
def tarcvf_file(other_file_name):
    print(f"开始解压{other_file_name},并提权")
    run_comand(f"tar -xvf {base_dir}/{other_file_name} -C {base_dir}")
    run_comand(f"chmod -R 777 {base_dir}")
    print("解压和提权成功")
    print("**************************")

def detect_architecture():
    arch = platform.machine()
    
    if arch == "x86_64":
        return "x86_64"
    elif arch == "armv7l":
        return "ARM (32-bit)"
    elif arch == "aarch64":
        return "ARM (64-bit)"
    else:
        return "Unknown"

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

# 定义一个函数,用于配置conda环境
def configure_conda(prefix):
    # 设置环境变量,将conda的bin目录加入path
    conda_dir = os.path.join(prefix, "/etc/profile.d/conda.sh")
    with open(conda_dir, "w") as f:
        f.write('export PATH("{}/bin:$PATH")'.format(prefix))



def apt_install(package):
    """安装指定的 apt 软件包。

    Args:
        package (str): 需要安装的软件包名称。

    Returns:
        int: 命令执行状态码。
    """
    command = ["apt", "install", package]
    return subprocess.run(command, check=True).returncode


# if detect_architecture()=="x86_64":
#     Miniconda3_sh_name="Miniconda3-latest-Linux-x86_64.sh"
# else:
#     Miniconda3_sh_name="Miniconda3-latest-Linux-armv7l.sh"
other_file_name="pcap-play.tar"
project_name = "/home/user/documents/审计系统/测试软件"
# # 安装目录为当前用户家目录下的miniconda3
# miniconda_prefix = os.path.join(os.environ["HOME"], "miniconda3")
# file_names=[Miniconda3_sh_name,other_file_name]

def auto_deploy():
    print("开始清理环境")
    clean_env()
    print("清理环境完成")
    print("**************************")

    print("开始下载脚本文件")
    # download_file(Miniconda3_sh_name)

    download_file(project_name,other_file_name)
    print("下载脚本文件完成")
    print("**************************")

    # print("开始安装Miniconda3")
    # # print(f"bash {Miniconda3_sh_name} -b -p {miniconda_prefix}", shell=True, check=True)yes
    # # subprocess.run(f"rm -rf /root/miniconda3")

    # subprocess.run(f"bash {Miniconda3_sh_name} -b -p {miniconda_prefix}", shell=True, check=True)
    # print("安装Miniconda3完成")
    # print("**************************")

    # print("开始配置conda环境")
    # configure_conda(miniconda_prefix)
    # print("配置conda环境完成")
    # print("**************************")

    print("开始安装pip包")
    # 安装需要的Python包,指定清华源
    libraries = ["psutil", "PrettyTable", "matplotlib", "paramiko"]
    for lib in libraries:
        # install_package(lib, source="https://pypi.tuna.tsinghua.edu.cn/simple")
        install_package(lib, source="https://mirrors.aliyun.com/pypi/simple/")
    print("安装pip包完成")
    print("**************************")

    print(f"开始解压{other_file_name},并提权")
    run_comand(f"tar -xvf {base_dir}/{other_file_name} -C {base_dir}")
    run_comand(f"chmod -R 777 {base_dir}")
    print("解压和提权成功")
    print("**************************")

def pcap_dev():
    print("开始下载pcap包")
    file_name = "long_time_pcap.tar"
    download_file(project_name, file_name)
    tarcvf_file(file_name)
    print("下载pcap包完成")
    print("**************************")