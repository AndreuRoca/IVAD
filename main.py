from automatic_actions import gesture_1_open_google_docs, gesture_2_toggle_speach_writing, gesture_3_selec_copy_paste_to_new_email, gesture_1_close, gesture_3_seach_IVAD_mails
from model import train_model, predict, find_peaks_num
from serial_read import serial_signal_read, wait_until_serial_port_is_available_and_connect
import os
from joblib import load

def run():
    ser=wait_until_serial_port_is_available_and_connect()
    model_path='model.joblib'
    if os.path.isfile(model_path)==False:
        print ("Training model... This may take some time")
        dataset_path='dataset.csv'
        if os.path.isfile(dataset_path)==True:
            model=train_model(dataset_path, model_path, train_test_split_var=False, debug=False)
            print("Model trained!")
        else:
            print("Traning unavailable: Dataset missing or wrong path")
            return "exit"
    else:
        model=load(model_path)
    google_docs_open=False #0 is for google docs closed, 1 is for open
    gmail_open=False
    while (1):
        min_confidence=0.70
        data,threshold_times_crossed=serial_signal_read(ser)
        peaks=find_peaks_num(data)
        gesture_done, confidence=predict([data+[threshold_times_crossed]+[peaks]],model)
        if confidence>min_confidence:
            if gesture_done==1:
                if google_docs_open==False and gmail_open==False:
                    gesture_1_open_google_docs()
                    google_docs_open=1
                elif google_docs_open==True and gmail_open==False:
                    gesture_1_close()
                    google_docs_open=False
                elif google_docs_open==False and gmail_open==True:
                    gesture_1_close()
                    gmail_open=False

            elif gesture_done==2 and google_docs_open==True:
                gesture_2_toggle_speach_writing()

            elif gesture_done==3:
                if google_docs_open==True:
                    gesture_3_selec_copy_paste_to_new_email()

                elif google_docs_open==False and gmail_open==False:
                    gesture_3_seach_IVAD_mails()
                    gmail_open=True
        else:
            #gesture not detected with suficient confidence.
            pass


if __name__ == '__main__':
    run()
