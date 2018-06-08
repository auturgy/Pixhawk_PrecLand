import pigpio
import time
pi=pigpio.pi()
if not pi.connected:
    exit()
    
def PWM():
    def foo():
        foo.counter += 1
    foo.counter = 0
    def bar():
        dc = bar.y - bar.x
        return dc
    def cbf(gpio,level,tick):
        #print(gpio,level,tick)
        if (level == 0) & (foo.counter == 1):
            bar.y = tick
        if level == 1:
            foo()
            if foo.counter == 1:
                bar.x = tick
            if foo.counter == 2:
                foo.counter = 0
                cb1.cancel()
                print(bar())
                
    cb1 = pi.callback(17,pigpio.EITHER_EDGE,cbf)

PWM()

