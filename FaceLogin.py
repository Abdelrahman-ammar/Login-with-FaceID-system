import tkinter
from tkinter import messagebox
import numpy as np
import cv2
import os
from PIL import  Image
import json


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

window = tkinter.Tk()
text_var = tkinter.StringVar()


def saving_data(data):
    file=open('data.txt','w',encoding='utf-8')
    json.dump(data,file,ensure_ascii=False)
    file.close()


def loading_data():
    file=open('data.txt','r',encoding='utf-8')
    data=json.load(file)
    file.close()
    return data

data = loading_data()


def register():
    username = username_entry.get()
    password = password_entry.get()
    if username != "" and password != "" and username.isdigit():
        if username not in data:
            count = 0
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)
            cam.set(4, 480)
            while True:
                ret, img = cam.read()
                img = cv2.flip(img, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(20, 20))
                count += 1
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    cv2.imwrite("dataset/user." + str(username_entry.get()) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                if count >= 30:
                    break
                cv2.imshow('video', img)
                cv2.waitKey(10)
            cam.release()
            cv2.destroyAllWindows()
            data[username] = password
            saving_data(data)
            text_var.set("Succesfully registered")
        else:
            text_var.set("User name Already Exists...Try another one or Login!!!")
    else:
        text_var.set("Please provide a numeric username and password!!!")




def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        faces = faceCascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids


# ids,images = getImagesAndLabels("D:\PyCharmProjects\dataset")

def trainmodel(path):
    images,ids = getImagesAndLabels(path)
    recognizer.train(images,np.array(ids))
    recognizer.write('trainer/trainer.yml')


def login():
    username = username_entry.get()
    password = password_entry.get()
    if username != "" and password !="" and username.isdigit():
        if username in data:
            if data[username] == password:
                cam = cv2.VideoCapture(0)
                cam.set(3, 640)
                cam.set(4, 480)
                trainmodel("D:\Projects\LoginWithFaceIDandPassword\dataset")
                recognizer.read("trainer/trainer.yml")
                while True:
                    ret, img = cam.read()
                    img = cv2.flip(img, 1)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(20, 20))
                    id, confidence = None, None
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                        cv2.putText(img, str(id), (x + 18, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if int(username) == id:
                        cv2.imshow("cam", img)
                        cv2.waitKey(10)
                        text_var.set("Logged in successfully")
                        cam.release()
                        cv2.destroyAllWindows()
                        break
                    else:
                        cv2.imshow("cam",img)
                        cv2.waitKey(5)
                        text_var.set("UserID doesn't match person")
                        cam.release()
                        cv2.destroyAllWindows()
                        break
            else:
                text_var.set("Invalid Password")
        else:
            text_var.set("Id is not valid,Please SignUp")
    else:
        text_var.set("Please provide a numeric username and password")



def clear_text():
    username_entry.delete(0, tkinter.END)
    password_entry.delete(0,tkinter.END)
    # hello_label.config(text="")


window.title("Login form")
window.geometry('800x500')
window.configure(bg='#333333')

frame = tkinter.Frame(bg='#333333')
login_label = tkinter.Label(
    frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))

message_label = tkinter.Label(frame,textvariable=text_var,font=("Arial", 16))
username_label = tkinter.Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))

password_label = tkinter.Label(
    frame,text="Password",bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_entry = tkinter.Entry(frame,font=("Arial",16))

# status_label = tkinter.Label(
#     frame, text="Status", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),command=login)
register_button = tkinter.Button(
    frame, text="Signup", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),command=register)
clear_button = tkinter.Button(
    frame, text="Clear", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16),command=clear_text)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)#clear must delete value inside this also
login_button.grid(row=4, column=0, padx=50, pady=30)
register_button.grid(row=4, column=1, padx=10, pady=30)
clear_button.grid(row=4, column=2, padx=10, pady=30)
message_label.grid(row=3,column=1,pady=20)
frame.pack()

window.mainloop()









