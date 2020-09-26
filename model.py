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
        #model= KNeighborsClassifier(7).fit(X_train, y_train)

        if debug:
            print("Test model accuracy score: ",model.score(X_test, y_test))
    else:
        model=LogisticRegression(random_state=0, max_iter=10000, penalty='none', solver='sag', multi_class='multinomial').fit(X_f,y)
        #model= KNeighborsClassifier(7).fit(X, y)

    dump(model, 'model1.joblib')
    return model


def evaluate_model_in_live(Idle_treshold, num_of_evaluations,debug=True):
    #Serial read. When lectura>5, Take 12000 samples. Apply prediction.
    model = load('model1.joblib')
    while True:
         try:
             ser=serial.Serial('/dev/ttyACM1',115200)
             print("Device connected!\n\n")
             break
         except FileNotFoundError and serial.serialutil.SerialException:
             print("No device conected")
             print("Reconnecting...")
             time.sleep(3)

    while num_of_evaluations!=0:
        sample_value=ser.read()
        while sample_value[-1]<Idle_treshold:
            #stuck here
            sample_value=ser.read()
            if debug==True:
                print ("")
        n_sample=0
        evaluation_data=[]
        while n_sample<12000:
            #collect 12000 samples
            evaluation_data+=ser.read()
            n_sample+=1
        print("Go!")
        evaluation_data_fft=fft(evaluation_data)
        evaluation_data_abs=np.abs(evaluation_data_fft)
        #evaluation=pd.DataFrame.from_records(evaluation_data_abs)
        class_pertenance_probabilities=model.predict_proba([evaluation_data_abs])
        print("probability: ",class_pertenance_probabilities)
        print ("class: ", model.predict([evaluation_data_abs]))
        num_of_evaluations-=1

    print("exit evaluation")


if __name__ == '__main__':
    model=train_model("dataset_clone.csv", train_test_split_var=False)

    evaluate_model_in_live(3, 15, debug=False)
