# Run on linux 
#!pip install pyttsx3
#!pip install pydub
#!sudo apt install espeak

import pyttsx3
from pydub import AudioSegment
import threading

class AudioGenerator:
    def __init__(self):
        self.engine = pyttsx3.init("espeak")  # Initialize pyttsx3 engine with the "espeak" driver

        self.lock = threading.Lock()  # Create a lock to control thread synchronization
        self.finished = False  # Flag to indicate if speech synthesis has finished

        # Set the event handler for the end of utterance
        self.engine.connect('finished-utterance', self._on_end)

        self.engine.setProperty('rate', self.engine.getProperty('rate')-20)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[11].id)

    def _on_end(self, name, completed):
        self.finished = True  # Set the finished flag to indicate speech synthesis is complete
        self.lock.release()  # Release the lock to allow the main thread to proceed

    def generate_audio_file(self, text, filename):
        self.lock.acquire()  # Acquire the lock to prevent the main thread from proceeding
        self.finished = False  # Reset the finished flag for the new synthesis
        #save to file is just what i do. its not necessary.
        self.engine.save_to_file(text, filename)  # Save the speech to the specified file
        self.engine.startLoop(False)  # Start the engine loop
        self.engine.iterate()  # Run the engine loop iteration
        self.engine.endLoop()  # End the engine loop

    def get_audio(self,filename):
      return AudioSegment.from_file(filename, format="mp3") # returns an audo object which can be played directly

# Example usage
text = "Hi. How are you? what are you doing?"
file_path = "test.mp3" #save to file is just what i do. its not necessary.

audio_generator = AudioGenerator()
x = audio_generator.generate_audio_file(text, file_path) #save to file is just what i do. its not necessary.
audio_generator.lock.acquire()  # Wait for the synthesis to complete
audio_generator.lock.release()  # Release the lock
audio = audio_generator.get_audio(file_path) # i do save to file so i can do this. now you can play this audio (for example send it to frontend)



