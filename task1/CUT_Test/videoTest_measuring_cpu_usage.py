import cv2
import numpy as np
import time
import statistics
import psutil
import threading

from datetime import datetime
from CUTGan import CUTGan

def start_measuring_cpu():
    cpu_usage_list = []
    mem_usage_list = []
    PROCNAME = "python.exe"
    python_pid = 0

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            print(proc)
            python_pid = proc.pid
    p = psutil.Process(python_pid)

    print("Thread Started")

    while True:
        '''stop after 10 sec'''
        time_delta = datetime.now() - start
        if time_delta.total_seconds() >= 10:
            print('CPU Average Usage', statistics.mean(cpu_usage_list))
            print('Memory Average Usage', statistics.mean(mem_usage_list))
            break
        cpu_usage_list.append(p.cpu_percent()/psutil.cpu_count())
        mem_usage_list.append(p.memory_percent())
        time.sleep(0.5)


if __name__ == '__main__':
    #total_cpu_usage = []
    cut_gan = CUTGan('./images\\4.png')

    t = threading.Thread(target=start_measuring_cpu)

    start = datetime.now()
    cap = cv2.VideoCapture(0)
    t.start()

    while cv2.waitKey(33) < 0:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, dsize=(512, 512), interpolation=cv2.INTER_LINEAR)
            image_result = cut_gan.start_converting(frame)
            cv2.imshow('video', image_result)
    #print(total_cpu_usage)
    #print('# of Count', len(total_cpu_usage))
    #print('Average CPU Usage', statistics.mean(total_cpu_usage))


    cap.release()
    cv2.destroyAllWindows()
