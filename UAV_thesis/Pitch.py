import time
import numpy

time.sleep(3)
numpy.save('Roll.npy',[123])
time.sleep(3)
numpy.save('testfile.npy',[345])
t=numpy.load('testfile.npy')
print t
h=t+6
def main():
    start = time.time()
    for i in range(1,62):
        if i <= 10: 
            value=h*i/10
            
        elif 10< i <=50:
            value=h
            
        elif 50< i <=60:
            value=h*(60-i)/10
            
        else:
            value=0
            stop = time.time()
            print stop-start


        time.sleep(0.05)
        value=round(value)
        print value
    

if __name__ == "__main__":
    main()



