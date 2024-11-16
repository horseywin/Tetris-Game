from pynput import keyboard

# Define what happens when a key is pressed
def on_press(key):
    try:
        print(f"Key {key.char} was pressed")
    except AttributeError:
        print(f"Special key {key} was pressed")
    
    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

# Set up the listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()