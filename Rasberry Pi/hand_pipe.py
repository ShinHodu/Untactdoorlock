import cv2
import mediapipe as mp
import numpy as np
import keyboard
import time
import pymysql
max_num_hands=1

gesture={
  2:'1', 8:'2',10:'3',11:'4',24:'5',26:'spacing',27:'clear'
}

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands=mp_hands.Hands(
  max_num_hands=max_num_hands,
  min_detection_confidence=0.5,
  min_tracking_confidence=0.5
)
f=open('test.txt','w')
file=np.genfromtxt('dataSet.txt',delimiter=',')
angleFile=file[:,:-1]
labelFile=file[:,-1]
angle=angleFile.astype(np.float32)
label=labelFile.astype(np.float32)
knn=cv2.ml.KNearest_create()
knn.train(angle,cv2.ml.ROW_SAMPLE,label)

cap = cv2.VideoCapture(-1)

conn=pymysql.connect(host="localhost",user="root",passwd="uubbn",db="doorlock")
cur=conn.cursor()

startTime=time.time()
prev_index=0
sentence=''
recognizeDelay=2
while True:
      ret,img=cap.read()
      if not ret:
            continue
      imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      result=hands.process(imgRGB)
      
      if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                  joint=np.zeros((21,3))
                  for j,lm in enumerate(res.landmark):
                        joint[j]=[lm.x,lm.y,lm.z]
                  v1=joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:]
                  v2=joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:]
                  v=v2-v1
                  v=v/np.linalg.norm(v,axis=1)[:,np.newaxis]
                  
                  comparev1=v[[0,1,2,4,5,6,7,8,9,10,12,13,14,16,17],:]
                  comparev2=v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]
                  angle=np.arccos(np.einsum('nt,nt->n',comparev1,comparev2))
                  
                  angle=np.degrees(angle)
                  
                  if keyboard.is_pressed('a'):
                        for num in angle:
                              num=round(num,6)
                              f.write(str(num)) 
                              f.write(',')
                        
                        f.write("26.000000")
                        f.write('\n')
                 
                  data=np.array([angle],dtype=np.float32)
                  ret,results,neighbours,dist=knn.findNearest(data,3)
                  index=int(results[0][0])
                  if index in gesture.keys():
                        if index != prev_index:
                              startTime=time.time()
                              prev_index=index
                        else :
                              if time.time()-startTime >recognizeDelay:
                                    if index ==26:
                                          sentence +=' '
                                    elif index ==27 :
                                          sentence=''
                                    else :
                                          sentence+=gesture[index]
                                    startTime=time.time()
                        #cv2.putText(img,gesture[index].upper(),(int(res.landmark[0].x * img.shape[1]-10),int(res.landmark[0].y * img.shape[0]+40)),cv2.FONT_HERSHEY_SIMPLEX,1,3)
                  mp_drawing.draw_landmarks(img,res,mp_hands.HAND_CONNECTIONS)
      cv2.putText(img,sentence,(20,440),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3)
      cv2.imshow('HandTracking',img)
      cv2.waitKey(1)
      if keyboard.is_pressed('a'):
            f.write(sentence)
            f.write('\n')
      elif keyboard.is_pressed('b'):
            break;
f.close();
cap.release()
f=open('test.txt','r')
f2=open('answer.txt','r')

line=f.readline()
line2=f2.readline()


if line == line2:
     sql="INSERT INTO doorlock.hand(name) VALUES ('1')"
     print("ok")
else :
      sql="INSERT INTO doorlock.hand(name) VALUES ('0')"
      print("X")
cur.execute(sql)
conn.commit()      
f.close();
f2.close();
conn.close()              

                                    
 