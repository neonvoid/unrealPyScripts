from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
import cv2
import tensorflow as tf
import numpy as np
import os
import csv

cats = ['closeup','medium','wide']
ip = '127.0.0.1'
recievePort = 8000
outputPort = 7000

#load model
model = tf.keras.models.load_model('osc/addedDataCNN.keras')

def prep(filepath):
    img_size=100
    img=cv2.imread(filepath,cv2.IMREAD_COLOR)
    if img is None:
        print(f'no image, path:{filepath}')
    else:
        resized = cv2.resize(img,(img_size,img_size))
        return resized.reshape(-1,img_size,img_size,3)

def fromUnreal(address,msg):
    #print('msg recieved from unreal')
    fp = "osc/oscTests/"+ msg +".png"
    print(fp)
    pred = model.predict(prep(fp))
    frame=cats[np.argmax(pred)]+','
    print(frame)
    #client.send_message('/fromVS',frame)
    with open ('shotTypes.txt','a') as f:
        f.write(frame)

def fromUnrealCam(add,msg):
    fp = msg
    split = fp.split(',')
    loc=[split[0],split[1],split[2]]
    with open('camChoices.csv','a',newline=('')) as f:
         writer = csv.writer(f)
         writer.writerow(loc)
         
#catches messages
dispatcher = dispatcher.Dispatcher()
dispatcher.map('/fromUnreal',fromUnreal)
dispatcher.map('/fromUnrealCam',fromUnrealCam)
# dispatcher.map('/fromMax',fromMax)

#client
client = SimpleUDPClient(ip,outputPort)


#server
server = osc_server.BlockingOSCUDPServer((ip,recievePort),dispatcher)
print(f"server listening on {server.server_address}")
server.serve_forever()

# def fromMax(address,*args):
#     print('msg recieved from max')
#     # pred = model.predict(prep('testingSS/3.png'))
#     # print(cats[np.argmax(pred)])
#     print(args[0])

