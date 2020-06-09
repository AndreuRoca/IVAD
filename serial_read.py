import serial
import time
import os
import csv
import matplotlib.pyplot as plt

first_line=['data','classification']

ser=serial.Serial('/dev/ttyACM0',115200)
data=[]
n_reps=0

while (n_reps<10): #number of repetitions
    print("reading serial port acm0")
    i=0
    data=[]
    while (i<50000): #readding 5000 
        n_data=ser.read()
        data+=n_data
        i+=1
    
    print("stop reading")
    print("plotting...")
    plt.plot(data)
    plt.ylabel('wave form')
    plt.show(1)
    n_reps+=1



    


with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([data, '1'])
	
