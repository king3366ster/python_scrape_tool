#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import multiprocessing
import subprocess, sys
import time, json, random

class MultiProcess:
    def __init__(self, fn_name, process_num = 1, process_params = []):
        self.fn_name = fn_name
        self.process_num = process_num
        self.process_params = process_params
        self.process_list = []
        self.name_pre = 'process_%03d_' % int(random.random() * 1000)

    # isDaemon 是否是守护进程， isJoin 是否时序并行
    # isJoin True => 串行，False => 并行
    def run(self, isDaemon = False, isJoin = False):
        for i in range(0, self.process_num):
            name = '%s%03d' % (self.name_pre, i)
            if len(self.process_params) > i:
                param = self.process_params[i]
                if isinstance(param, list):
                    args = tuple(param)
                elif isinstance(param, tuple):
                    args = param
                else:
                    args = (param,)
            else:
                args = ()
            proc = multiprocessing.Process(name = name, target = self.fn_name, args = args)
            proc.daemon = isDaemon # # 则主线程结束时，会把子线程B也杀死，与C/C++中得默认效果是一样的。
            self.process_list.append(proc)
            proc.start()
            if isJoin:
                proc.join()
        print ('processs run')

    def stop(self):
        for proc in self.process_list:
            if proc.is_alive():
                proc.terminate()
                print ('pid %d stoped' % proc.pid)
                proc.join()
        print ('process stoped')

def test_process(num, msg_queue):
    print ('Process:', num)
    name = multiprocessing.current_process().name
    print ('Starting:', name)
    # sys.exit(0)
    pid = multiprocessing.current_process().pid
    time.sleep(2)
    msg_queue.put(pid)
    print ('Exiting :', name)

if __name__ == '__main__':
    msg_queue = multiprocessing.Queue()

    t = MultiProcess(test_process, process_num = 3, process_params = [(6, msg_queue),(4, msg_queue),(5, msg_queue)])
    t.run(isJoin = False)

    flag = 2
    time.sleep(3)
    while msg_queue.empty() != True:
        msg = msg_queue.get()
        print ('main proc get:%d' % msg)
##        time.sleep(1)

##    t.stop()
    print ('process end')
