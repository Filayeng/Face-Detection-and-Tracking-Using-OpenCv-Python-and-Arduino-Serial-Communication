import time,cv2,numpy,serial

port = serial.Serial("COM3", baudrate = 115200, timeout=1)
time.sleep(2)

camera = cv2.VideoCapture(1)   # 0 - laptop camera  1 - webcam

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

wait = 0
x_axis= 90     # Initially servo X motor position
y_axis = 115   # Initially servo Y motor position

while True:
    start = time.time()
    _,frame = camera.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 4)     # Face detection sensitivity

    frame_center = int(frame.shape[1]/2) , int(frame.shape[0]/2) 

    for x,y,w,h in faces:
        face_center = (x+int(w/2),y+int(h/2))

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        cv2.line(frame, (face_center[0],0), (face_center[0],480), (0,0,255),2)  
        cv2.line(frame, (0,face_center[1]), (640,face_center[1]), (0,0,255),2)
        cv2.line(frame, (face_center), frame_center, (0,255,255),2)

        cv2.circle(frame, face_center, 2, (0,255,255), 2)
        cv2.circle(frame, frame_center, 2, (0,255,255), 2)


        x_distance = round(abs(face_center[0] - frame_center[0]) / 18, 0)   # Proportions the distance between Image Center and Target Center according to the Servo Motor degree .
        y_distance = round(abs(face_center[1] - frame_center[1]) / 25, 0)   # Proportions the distance between Image Center and Target Center according to the Servo Motor degree .
         
        x_direction = 1
        y_direction = 1
        
        
        if (face_center[0] >= 320):
            cv2.putText(frame, "x_dist = " + str(-1 * x_distance), (20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,150), 1)
            x_direction = 0    # x_axis - pan_distance  
        else:
            cv2.putText(frame, "x_dist = " + str(x_distance), (20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,150), 1)
            x_direction = 1    # x_axis + x_distance

        if (face_center[1] >= 240):
            cv2.putText(frame, "y_dist = "  + str(-1 * y_distance), (20,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,150), 1)
            y_direction = 0   # y_axis - y_distance
        else:
            cv2.putText(frame, "y_dist = "  + str(y_distance), (20,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,150), 1)
            y_direction = 1   # y_axis + y_distance


        wait = wait + (time.time() - start)

        if wait >= 0.4:  # wait time of data sending
            if (x_distance >= 2 or y_distance >=2):  #average sensitivity

                if (x_direction == 1):
                    x_axis = x_axis + x_distance
                    print("x_distance = " + str(x_axis))

                else:
                    x_axis = x_axis - x_distance
                    print("x_distance = " + str(x_axis))

            
                if (y_direction == 1):
                    y_axis = y_axis + y_distance
                    print("y_distance = " + str(y_axis))
                    
                else:
                    y_axis = y_axis - y_distance
                    print("y_distance = " + str(y_axis))
                    
                port.write(str.encode(str(-1 * x_axis)))    # Sends X axis via serial port
                time.sleep(0.005)
                port.write(str.encode(str(y_axis)))         # Sends Y axis via serial port

                print("-------------------")
                
            wait = 0
            
        break  
    
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    frame = cv2.resize(frame, (640, 480)) 
    cv2.imshow("output", frame)
                                      
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
