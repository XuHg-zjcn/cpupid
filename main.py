#!/usr/bin/python3
import time
import psutil

N = 4
m = 800
M = 2800

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
    return int(psutil.cpu_freq().current)

if __name__ == '__main__':
    Target = 72
    delta = Target - get_temp()
    inte = (get_clock() - delta*100)/2
    d_ = delta
    while True:
        now = get_temp()
        delta = Target - now
        diff = delta - d_
        d_ = delta
        if abs(diff)<=1 or abs(delta)<=1:
            diff = 0
        MHz = diff*50 + delta*100 + inte*2
        if m <= MHz <= M:
            inte += delta
        else:
            if MHz < m:
                MHz = m
            if MHz > M:
                MHz = M
        print(delta, inte, MHz)
        set_clock(MHz)
        time.sleep(1)
