#!/usr/bin/python3
"""
CPU temperature PID controller
The program *must* run in root user.

Tested it on this environment:
Computer: Lenovo-Y50-70 Laptop
CPU: Intel(R) Core(TM) i5-4200H CPU @ 2.80GHz
OS: Ubuntu 20.04 LTS
Load: BOINC Client 7.16.6
"""
import os
import time
import psutil
import math


# CPU params
N = psutil.cpu_count(logical=True)
pmin = psutil.cpu_count(logical=False)/N*100
# please edit Freq(MHz) for your computer
m = 800   # min
M = 2800  # max

# PID params
Target = 72
Kp = 2
Ki = 0.75
Kd = 0.5

def get_temp():
    temps = psutil.sensors_temperatures()
    return temps['coretemp'][0].current

def set_clock(MHz):
    kHz = int(MHz*1000)
    for i in range(N):
        fn = f'/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_max_freq'
        with open(fn, 'w') as f:
            f.write(str(kHz))

def get_clock():
    f = int(psutil.cpu_freq().current)
    if f > M:
        return M - 100
    if f < m:
        return m + 100
    return f

# I did't find way to get CPU Voltage, so estimate Power only by Frequency.
# This parameters isn't measurement, it's estimated by TDP.
# P = f*(1 + f)*5
# f = (sqrt(1 + 4*P/5) - 1)/2
# units f:GHz, P:W
def set_power(x):
    if x < 0:
        x = 0
    clock = (math.sqrt(1 + 4*x/5) - 1)/2
    clock *= 1000
    ret = 0
    if x < 0 or clock < m:
        clock = m
        ret = -1
    elif clock > M:
        clock = M
        ret = 1
    set_clock(clock)
    return ret, clock

def get_power():
    clock = get_clock()/1000
    return clock*(1 + clock)*5

def main():
    delta = Target - get_temp()
    inte = (get_power() - delta*Kp)/Ki
    d_ = delta
    c = 10000
    while True:
        while psutil.cpu_percent() < pmin and get_clock() >= c-200:
            time.sleep(0.5)
        now = get_temp()
        delta = Target - now
        diff = delta - d_
        d_ = delta
        if abs(diff) <= 1 or abs(delta) <= 2:
            diff = 0
        if abs(delta) <= 1:
            delta *= 0.75
        power = diff*Kd + delta*Kp + inte*Ki
        r, c = set_power(power)
        if r == 0 or r*delta<0:  # r == 0 或 r与delta异号
            inte += delta
        print(f'{-delta:+2.0f}, {power:4.1f}, {c:4.0f}')
        time.sleep(1)

def Is_ready_running():
    thepid = os.getpid()
    for pid in psutil.pids():
        p = psutil.Process(pid)
        try:
            name = p.name()
        except Exception:
            pass
        else:
            if name == 'cpupid.py' and pid != thepid:
                return pid
    return None


if __name__ == '__main__':
    r = Is_ready_running()
    if r is not None:
        print(f'same name program is running, PID={r}')
    else:
        main()
