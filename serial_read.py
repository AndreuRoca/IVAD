import serial
import time
import os
import csv
import matplotlib.pyplot as plt
import sys
from scipy.signal import find_peaks, peak_prominences


def array_generator():
    '''
    Returns a array of 12000 numbers. Used fot the plots and the dataset header.
    '''
    number_list=[]
    n_samples=12000
    for i in range(n_samples):
        number_list.append(i)
    return number_list


def check_existing_dataset(dataset_file_name):
    '''
    Check for existing datasets. If there is an existing one that
    matches the "dataset_file_name" input, use it. If not
    create one with this name.

    Return dataset_file_name string.
    '''
    if os.path.isfile(dataset_file_name):
        print ("Appending new entries to current dataset "+ dataset_file_name)
    else:
        print("There isn't any dataset in the directory...\nCreating a fresh one...\n")
        number_list=array_generator()
        with open(dataset_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(number_list+["threshold_pas"]+["peak_number"]+["classification"])
        time.sleep(1)
    return dataset_file_name


def serial_signal_read(ser,inferior_threshold=2, superior_threshold=9,num_of_samples=12000):
    '''
    Read "num_of_samples" samples from serial port "ser", and appends to a list. Computes also the
    hysteresis threshold with variables "superior_threshold" and "inferior_threshold"

    Returns data list and number_of_threshold_pass int.
    '''
    i=0
    data=[]
    high_state=False
    threshold_times_crossed=0

    while (i<num_of_samples):
        sample_data=ser.read()
        data+=sample_data
        if sample_data[-1]>superior_threshold and high_state==False: #sample_data is type byte, if you select the last digit you get the int transformation
            high_state=True
            threshold_times_crossed+=1
        elif sample_data[-1]<inferior_threshold and high_state==True:
            high_state=False
            #threshold_times_crossed+=1
        i+=1
    return data, threshold_times_crossed


def iterator(dataset_file_name,ser,total_num_repetitions=100,total_num_classification=5):
    classification=1
    number_list=array_generator()
    while (classification<total_num_classification):
        repetition=0
        print("=================")
        print("Gesture number: ", classification, "\n")

        while (repetition<total_num_repetitions): #number of repetitions for each gesture.
            data, threshold_times_crossed=serial_signal_read(ser)
            peaks, _ =find_peaks(data, prominence=0.95 ,distance=250, threshold=3)
            print("reading serial port. Iteration n "+ str(repetition))
            print ("Times threshold was pass: ", threshold_times_crossed)
            print ("Num of peaks: ", len(peaks), "\n")

            #Matplotlib plotting. Untill you don't close the graph window
            #it doesnt' continue.
            plt.plot(number_list,data)
            plt.ylabel('entry n '+str(repetition))
            plt.xlabel('samples')
            plt.show()
            data+=[threshold_times_crossed,len(peaks),classification]
            with open(dataset_file_name, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

            repetition+=1

        print("Gesture number ", classification, "done, next \n\n\n")
        classification+=1



if __name__ == '__main__':
#Serial check and connection. ACM0 for default.
    while True:
         try:
             ser=serial.Serial('/dev/ttyACM0',115200)
             print("Device connected!\n\n")
             break
         except FileNotFoundError and serial.serialutil.SerialException:
             print("No device conected")
             print("Reconnecting...")
             time.sleep(3)

    iterator(check_existing_dataset("dataset_new_features.csv"),ser)
    ser.close()
