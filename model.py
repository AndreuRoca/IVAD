import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.fft import fft
from sklearn.svm import SVC
from joblib import dump, load
import serial
from scipy.signal import find_peaks, peak_prominences
from serial_read import serial_signal_read, wait_until_serial_port_is_available_and_connect
import matplotlib.pyplot as plt

def train_model(dataset_path,model_path,train_test_split_var=True, debug=True):
    '''
    Trains from "dataset_path" and saves the model with persistence in "model_path", and overrides it.
    You can choose to train it with the full dataset, or do a train-test split to calculate the accuracy score
    Debug to enable Prints

    Return model instance
    '''
    dataset = pd.read_csv(dataset_path)
    y=dataset.iloc[:,-1]
    X=dataset.iloc[:,:-1]
    if debug:
        print ("1Dataset shape: ",dataset.shape)
    if train_test_split_var==True:
        X_train, X_test, y_train, y_test = train_test_split(X_f, y, test_size=0.30)
        if debug:
            print ("Train and test shape: ",X_train.shape, X_test.shape)
        model=SVC(random_state=1, kernel='rbf', C=80, gamma=0.0001,probability=True).fit(X_train, y_train)
        if debug:
            print("Test model accuracy score: ",model.score(X_test, y_test))
    else:
        model=SVC(random_state=1, kernel='rbf', C=80, gamma=0.0001,probability=True).fit(X,y)
    print("model traied succesfully")
    dump(model, model_path)
    return model


def find_peaks_num(data):
    '''
    Encapsulation of "find_peaks" function from scypy signal processing.
    "Find peaks" return the position given the "data" as input

    Return the number of peaks
    '''
    peaks, _ =find_peaks(data, prominence=0.95 ,distance=250, threshold=3)
    return len(peaks)


def predict(data, model):
    '''
    Receives the data with all the features,the already trained model, and elaborates a prediction.

    Returns the predictes class "gesture_done" and the confidence of this prediction being a float between (0.251-1].
    '''
    #done this way so the program doesn't call predict 2 times which takes more time.
    probabilities=model.predict_proba(data)[0]
    print (probabilities)
    index=0
    high=0

    for i in range(len(probabilities)):
        if probabilities[i]>high:
            high=probabilities[i]
            index=i
    return index+1, probabilities


def evaluate_model_in_live(idle_treshold, num_of_evaluations,debug=True):
    '''
    Demo and testing function (not used in final model). Reads serial port and evaluates the data received.
    Repeats "num_of_evaluations" times.Waits until idle_treshold is surpased (can also be ajusted for calibration).
    Debug bool used for verbose.

    Prints:
    - the probability of pertenence to each class "model.predict_proba"
    - class with most probability "model.predict"
    - number of times the signal cross the threshod "threshold_times_crossed"
    '''
    model = load('model.joblib')
    ser=wait_until_serial_port_is_available_and_connect()
    while num_of_evaluations!=0:
        sample_value=ser.read()
        while sample_value[-1]<idle_treshold:
            #stuck here untill some movement is detected
            sample_value=ser.read()
            if debug==True:
                print ("")
        data, threshold_times_crossed=serial_signal_read(ser)
        peaks=find_peaks_num(data)
        print("Go!")
        gesture_done,confidence=predict([data+[threshold_times_crossed]+[peaks]],model)
        print("probability: ",confidence)
        print ("class: ", gesture_done)
        print("Threshold: ", threshold_times_crossed, "Peak: ", peaks)
        num_of_evaluations-=1
    print("exit evaluation")


if __name__ == '__main__':
    model=train_model("dataset.csv","model.joblib", train_test_split_var=False)
    evaluate_model_in_live(2, 15, debug=False) #low treshold, value of 3 of the adc, 15 iterarions, and prints deactivated
