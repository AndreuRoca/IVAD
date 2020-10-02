from automatic_actions import action_1_open_google_docs, action_2_toggle_speach_writing, action_3_selec_copy_paste_to_new_email
from model import train_model, predict
from serial_read import serial_signal_read, wait_until_serial_port_is_available_and_connect

def run():
    ser=wait_until_serial_port_is_available_and_connect()
    while (1):
        min_confidence=0.70
        data=serial_signal_read(ser)
        gesture_done, confidence=prediction(data)
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
