from pynput import keyboard
import threading

# Define what happens when a key is pressed
def on_press(key):
    try:
        print(f"Key {key.char} was pressed")
    except AttributeError:
        print(f"Special key {key} was pressed")

    if key == keyboard.Key.left:
        print('lol')

    # Exit when the 'Esc' key is pressed
    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

# Function to start the keyboard listener
def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Run the listener in a separate thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Main program logic (can run alongside the listener)
print("Main program is running. Press 'Esc' to exit.")
listener_thread.join()  # Wait for the listener thread to complete

