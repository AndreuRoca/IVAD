import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.fft import fft
from joblib import dump, load
import serial
import time
from sklearn.neighbors import KNeighborsClassifier
from scipy.signal import find_peaks, peak_prominences
from serial_read import serial_signal_read

def train_model(dataset_path, train_test_split_var=True, debug=True):
    dataset = pd.read_csv(dataset_path)
    y=dataset.iloc[:,-1]
    X=dataset.iloc[:,:-1]
    if debug:
        print ("1Dataset shape: ",dataset.shape)
    X_fourier=fft(X)
    X_fourier_abs=np.abs(X_fourier)
    X_f=pd.DataFrame.from_records(X_fourier_abs)

    if train_test_split_var==True:
        X_train, X_test, y_train, y_test = train_test_split(X_f, y, test_size=0.30)
        if debug:
            print ("Train and test shape: ",X_train.shape, X_test.shape)
        model=LogisticRegression(random_state=0, max_iter=10000, penalty='none', solver='sag', multi_class='multinomial').fit(X_train, y_train)
        if debug:
            print("Test model accuracy score: ",model.score(X_test, y_test))
    else:
        model=LogisticRegression(random_state=0, max_iter=10000, penalty='none', solver='sag', multi_class='multinomial').fit(X_f,y)
    print("model traied succesfully")
    dump(model, 'model1.joblib')
    return model

def predict():

    gesture_done=1
    confidence=1
    return gesture_done, confidence

def evaluate_model_in_live(idle_treshold, num_of_evaluations,debug=True):
    #Serial read. When lectura>5, Take 12000 samples. Apply prediction.
    model = load('model1.joblib')
    while True:
         try:
             ser=serial.Serial('/dev/ttyACM0',115200)
             print("Device connected!\n\n")
             break
         except FileNotFoundError and serial.serialutil.SerialException:
             print("No device conected")
             print("Reconnecting...")
             time.sleep(3)

    while num_of_evaluations!=0:
        sample_value=ser.read()
        while sample_value[-1]<idle_treshold:
            #stuck here untill some movement is detected
            sample_value=ser.read()
            if debug==True:
                print ("")
        data, threshold_times_crossed=serial_signal_read(ser)
        peaks, _ =find_peaks(data, prominence=0.95 ,distance=250, threshold=3)
        print("Go!")
        evaluation_data_fft=fft(data)
        evaluation_data_abs=np.abs(evaluation_data_fft)
        class_pertenance_probabilities=model.predict_proba([data+[threshold_times_crossed]+[len(peaks)]])
        print("probability: ",class_pertenance_probabilities)
        print ("class: ", model.predict([data+[threshold_times_crossed]+[len(peaks)]]))
        print("Threshold: ", threshold_times_crossed, "Peak: ", len(peaks))

        num_of_evaluations-=1

    print("exit evaluation")


if __name__ == '__main__':
    #model=train_model("dataset_new_features.csv", train_test_split_var=False)
    evaluate_model_in_live(2, 15, debug=False) #low treshold, value of 3 of the adc, 15 iterarions, and prints deactivated
