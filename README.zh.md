# CPU温度PID控制器
本程序*必须*在root用户下运行  
请在运行前修改`cpupid.py`中的参数  
不要运行同类程序，否则CPU频率无法被稳定的设置  

## 测试环境
| 部件 | 参数 |
| :--: | :-- |
| 型号 | Lenovo-Y50-70 笔记本电脑
| CPU  | Intel(R) Core(TM) i5-4200H CPU @ 2.80GHz
| 系统 | Ubuntu 20.04 LTS
| 负载 | BOINC Client 7.16.6

## 安装教程
1. 修改`cpupid.py`中的参数
2. 复制文件
   ```sh
   sudo cp cpupid.py /usr/local/bin/   # 复制到安装目录
   sudo cp cpupidd /etc/init.d/        # 开机自启动
   ```
