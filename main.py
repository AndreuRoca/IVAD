from automatic_actions import action_1_open_google_docs, action_2_toggle_speach_writing, action_3_selec_copy_paste_to_new_email
from model import train_model, predict, find_peaks_num
from serial_read import serial_signal_read, wait_until_serial_port_is_available_and_connect
import os
from joblib import load

def run():
    ser=wait_until_serial_port_is_available_and_connect()
    model_path='model.joblib'
    if os.path.isfile(model_path)==False:
        print ("Training model...\nThis may take some time")
        dataset_path='dataset_new_features.csv'
        if os.path.isfile(dataset_path)==True:
            model=train_model(dataset_path, model_path, train_test_split_var=False, debug=False)
            print("Model trained!")
        else:
            print("Traning unavailable: Dataset missing or wrong path")
            return "exit"
    else:
        model=load(model_path)
    while (1):
        min_confidence=0.70
        data,threshold_times_crossed=serial_signal_read(ser)
        peaks=find_peaks_num(data)
        gesture_done, confidence=predict([data+[threshold_times_crossed]+[peaks]],model)
        if confidence>min_confidence:
            if gesture_done==1:
                action_1_open_google_docs()
            elif gesture_done==2:
                action_2_toggle_speach_writing()
            elif gesture_done==3:
                action_3_selec_copy_paste_to_new_email()
        else:
            #gesture not detected with suficient confidence.
            pass


if __name__ == '__main__':
    run()
