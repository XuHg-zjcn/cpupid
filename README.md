# CPU temperature PID controller
The program *must* run in root user.  
Please modify params in `cpupid.py` before run.  
Don't run this kind program multiply, else CPU Frequency unable be stable seted.  

## Test environment
| Parts | Parameter |
| :--: | :-- |
|Model | Lenovo-Y50-70 Laptop
| CPU  | Intel(R) Core(TM) i5-4200H CPU @ 2.80GHz
|  OS  | Ubuntu 20.04 LTS
| Load | BOINC Client 7.16.6

## Install
1. modify params in `cpupid.py`
2. copy files
   ```sh
   sudo cp cpupid.py /usr/local/bin/   # copy to install path
   sudo cp cpupidd /etc/init.d/        # auto startup
   ```
