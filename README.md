# Web-SurvivalScan_thread
基于Web-SurvivalScan项目二开，项目地址https://github.com/AabyssZG/Web-SurvivalScan

二开的地方
- 又单线程变成了多线程，通过-t参数指定
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
