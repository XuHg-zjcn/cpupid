#!/usr/bin/python3
import time
import psutil
import math

N = 4
m = 800
M = 2800

Target = 72
Kp = 2
Ki = 0.75
Kd = 0.5

def get_temp():
    temps = psutil.sensors_temperatures()
    return temps['acpitz'][0].current

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

# P = f*(1 + f)*5
# f = (sqrt(1 + 4*P/5) - 1)/2
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


if __name__ == '__main__':
    delta = Target - get_temp()
    inte = (get_power() - delta*Kp)/Ki
    d_ = delta
    while True:
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
