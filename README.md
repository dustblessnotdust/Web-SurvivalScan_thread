# Web-SurvivalScan_thread
一个多线程快速验活，并且结果可以通过.html形式直观查看

基于Web-SurvivalScan项目二开，项目地址https://github.com/AabyssZG/Web-SurvivalScan

一万多个IP，并列出了对应的Web资产地址，这个时候就需要快速验证资产存活网上找了一圈，都没什么好用的工具。

于是，就写了这个Web资产存活检测小工具：Web-SurvivalScan_thread

**二开的地方**
- 由单线程变成了多线程，通过-t参数指定
- 从原本的运行程序之后输入参数，变成了命令行输入
- 删除了之前的又要指定文件又要知道路径，变成了-f参数指定文件和路径

```
usage: Web-SurvivalScan_thread.py [-h] -f FILE_PATH [-p PROXY] [-t THREADS]

Batch website scanner.

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        Input target TXT file path (e.g., /some/path/test.txt)
  -p PROXY, --proxy PROXY
                        Proxy IP and port
  -t THREADS, --threads THREADS
                        Number of threads to use (default: 10)

```
# 使用
## 安装python库
```
pip3 install -r requirements.txt
```
## 常规使用
线程默认是10
```
python3 .\test.py -f .\test.txt -t 15
```
跑完后，即可拿到导出的两个文件：output.txt 和 outerror.txt

output.txt：导出验证存活成功（状态码200）的Web资产
outerror.txt：导出其他状态码的Web资产，方便后期排查遗漏和寻找其他脆弱点
.data/report.json：所有资产的运行数据，按JSON格式导出，方便处理
report.html：将所有资产进行HTML可视化导出，方便整理
![image](https://github.com/user-attachments/assets/4d01efae-2816-48e8-997b-77e8463640f6)
