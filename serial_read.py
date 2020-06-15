import serial
import time
import os
import csv
import matplotlib.pyplot as plt

first_line=['data','classification']
ser=serial.Serial('/dev/ttyACM0',115200)

#creating file and writing the two headers stored on "first_line". Opening a file as 'W' erases everything it had before so in case you want to add new rows, comment this 3 lines

with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(first_line)

#loop that cycles all the gestures a n_rep amount of times for a period of n samples

classification=1
n_samples=12000

while (classification<9):
    n_reps=0
    print("Gesture number", classification)
    while (n_reps<100): #number of repetitions
        print("reading serial port acm0")
        i=0
        data=[]
        while (i<n_samples): 
            n_data=ser.read()
            data+=n_data
            i+=1
        print("stop reading")
        print("plotting...")
        plt.plot(data)
        plt.ylabel('wave form')
        plt.show(1)
        n_reps+=1
        
        with open('dataset.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data, classification])
        
    print("Gesture done, next")
    print("\n")
    classification+=1





