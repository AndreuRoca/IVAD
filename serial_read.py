import serial
import time
import os
import csv
import matplotlib.pyplot as plt
import sys

dataset_file_name="dataset.csv"
n_samples=12000 #analog samples from arduino lectures. Not dataset sampels

while True:
     try:
         ser=serial.Serial('/dev/ttyACM0',115200)
         print("Device connected!\n\n")
         break
     except FileNotFoundError and serial.serialutil.SerialException:
         print("No device conected")
         print("Reconnecting...")
         time.sleep(3)

#Header of the dataset: [0,1,2...11999,classification]. Writing it if file doesn't exist.
number_list=[] #used as header and plots
for i in range(n_samples):
    number_list.append(i)

if os.path.isfile(dataset_file_name):
    print ("Appending new entries to current dataset "+ dataset_file_name)
else:
    print("There isn't any dataset in the directory...\nCreating a fresh one...\n")
    with open(dataset_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(number_list+["classification"])
    time.sleep(1)

classification=1

while (classification<9):
    n_reps=0
    print("=================")
    print("Gesture number: ", classification, "\n")
    while (n_reps<3): #number of repetitions for each gesture.
        print("reading serial port. Iteration n "+ str(n_reps))
        i=0
        data=[]
        while (i<n_samples):
            n_data=ser.read()
            data+=n_data
            i+=1

        #Matplotlib plotting. Untill you don't close the graph window
        #it doesnt' continue.
        plt.plot(number_list,data)
        plt.ylabel('entry n '+str(n_reps))
        plt.xlabel('samples')
        plt.show()
        n_reps+=1
        data+=[classification]
        with open(dataset_file_name, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    print("Gesture number ", classification, "done, next \n\n\n")
    classification+=1

ser.close()
