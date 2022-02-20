#!/usr/bin/python3
import time
import psutil

N = 4
m = 800
M = 2800

Target = 72
Kp = 100
Ki = 20
Kd = 40

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
        if abs(diff) >= 4:
            diff *= 1.5
        if abs(delta) <= 2:
            delta /= 2
        MHz = diff*Kd + delta*Kp + inte*Ki
        if m <= MHz <= M:
            inte += delta
        else:
            if MHz < m:
                MHz = m
            if MHz > M:
                MHz = M
        print(f'{-delta:+2.0f}, {MHz:4.0f}')
        set_clock(MHz)
        time.sleep(1)
