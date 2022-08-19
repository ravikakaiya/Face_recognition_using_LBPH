#import numpy as np
import cv2
import urllib
import os
import serial
import requests
import numpy as np
import sqlite3,time,datetime
class detection:
    def __init__(self):
        self.c=0
    def detect(self):
        #arduino = serial.Serial('com6',9600)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read('reconizer\\traindata.yml')
        font = cv2.FONT_HERSHEY_SIMPLEX
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture('http://10.174.117.168:8080')#TO use laptop cam comment next line and use this
        #@url = 'http://10.174.117.168:8080/shot.jpg'#add own server name using Ipwebcam android app
        
        def get_name(_id):
            path = "dataset"
            name =[i for i in os.listdir(path)]
            for n in name:
                if n.split('.')[1] == str(_id):
                    return n.split('.')[0]
        while 1:
            _,frame = cap.read()
            #img_re = urllib.request.urlopen(url)
            #img_arr = np.array(bytearray(img_re.read()),dtype=np.uint8)
            #frame = cv2.imdecode(img_arr,-1)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.2,6)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                Id, conf = rec.predict(gray[y:y+h,x:x+w])
                name = get_name(Id)
                data = str(name)+' '+str(int(conf))
                if int(conf) > 50:
                    cv2.putText(frame,str(data),(x,y), font,1,255,2,cv2.LINE_AA)
                    #if name == 'ravi':
                     #  arduino.write(str.encode('0'))
                    #else:
                     #  arduino.write(str.encode('1')) 
                    self.save_data(Id)
            cv2.imshow('gray',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cap.release()
        cv2.destroyAllWindows()
    def save_data(self,Id):
        self.c+=1
        conn=sqlite3.connect('fd.db')
        c=conn.cursor()
        query="""CREATE TABLE IF NOT EXISTS mp(
                    ID integer,
                    intime timestamp,
                    outtime timestamp,
                    date date
                    )"""
        c.execute(query)
        ts = time.time()
        t = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        d = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        c.execute("SELECT ID FROM mp WHERE ID = ? and date =?", (Id,d,))
        data=c.fetchall()
        if len(data) == 0:
            query="INSERT INTO mp(ID,intime,date) VALUES (?,?,?)"
            c.execute(query,(Id,t,d))
        else:
            query="UPDATE mp SET outtime=?,date=? WHERE ID=?"
            c.execute(query,(t,d,Id))
        conn.commit()
        conn.close()
