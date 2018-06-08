import time

import RPi.GPIO as GPIO

 

GPIO.setmode(GPIO.BOARD) #Chọn layout là chân vật lý

GPIO.setup(12,GPIO.IN)   #Chọn chân số 12 làm input


pinlist=[37,36,38,40]

# Tạo list các chân GPIO để điều khiển đông cơ

for pin in range(0,4):

    GPIO.setup(pinlist[pin],GPIO.OUT)
    
    GPIO.output(pinlist[pin],False)

# Set các chân trong list là chân output và reset về mức 0

 

totalstep=8

# Một chu kì điều khiển là 8 bước(xem hình Phương pháp điều khiển động cơ bước)

 

wavedrive = list(range(0, totalstep))

wavedrive[0] = [1,0,0,0] # chân 7: 1, chân 11, 13, 15: 0

wavedrive[1] = [0,1,0,0]

wavedrive[2] = [0,0,1,0]

wavedrive[3] = [0,0,0,1]

wavedrive[4] = [1,0,0,0]

wavedrive[5] = [0,1,0,0]

wavedrive[6] = [0,0,1,0]

wavedrive[7] = [0,0,0,1]

# Phương pháp wave drive: tại một thời điểm hay 1 step sẽ có cuộn dây có điện và

# tiếp tục cuộn dây kế

 

halfstep = []

halfstep = list(range(0, totalstep))

halfstep[0] = [1,0,0,0] # chân 7: 1, chân 11, 13, 15: 0

halfstep[1] = [1,1,0,0] # chân 7, 11: 1 chân 13, 14: 0

halfstep[2] = [0,1,0,0]

halfstep[3] = [0,1,1,0]

halfstep[4] = [0,0,1,0]

halfstep[5] = [0,0,1,1]

halfstep[6] = [0,0,0,1]

halfstep[7] = [1,0,0,1]

# Phương pháp halfstep: Một rồi hai cuộn dây có điện rồi lại một cuộn rồi lại hai cuộn

 

fullstep = []

fullstep = list(range(0, totalstep))

fullstep[0] = [1,1,0,0] # chân 7, 11: 1, chân 13,15: 0

fullstep[1] = [0,1,1,0]

fullstep[2] = [0,0,1,1]

fullstep[3] = [1,0,0,1]

fullstep[4] = [1,1,0,0]

fullstep[5] = [0,1,1,0]

fullstep[6] = [0,0,1,1]

fullstep[7] = [1,0,0,1]

# Phương pháp fullstep: tại 1 thời điểm có 2 cuộn dây có điện

 

step=0

# biến chaỵ qua các bước

 

waitime=0.0008
# waitime best de quay nhanh nhat
# Thời gian cuộn dây có điện. Đây chính là tốc độ quay của động

# cơ, thời gian cuộn dây giữ điện càng ngắn thì động cơ quay

# càng nhanh
# khong them lenh printf vao vong while, vi se bi sai

seq=halfstep[::1]

for i in range(0,16):
        
    
    for pin in range(0,4): # Đọc giá trị bảng trạng thái và xuất port

        if seq[step][pin]!=0:

            GPIO.output(pinlist[pin],True)

        else:

            GPIO.output(pinlist[pin],False)

 

    step+=1 # Chuyển sang bước tiếp theo

    if step==totalstep:

        step=0 # Khi tới bước 8 thì trở về bước 1
 
    time.sleep(waitime)
    # Delay chuyển bước
