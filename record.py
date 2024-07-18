import pyaudio
import wave
import threading


class Recording:
    def __init__(self, format, channels, frame_rate = 44100, frames_per_buffer=1024) -> None:
        
        #initialise variables
        self.audio = pyaudio.PyAudio()
        self.format = format
        self.n_channels = channels
        self.frame_rate = frame_rate
        self.frames_per_buffer = frames_per_buffer
        
        #initialise stream object
        self.stream = self.audio.open(format=self.format,
                        channels=self.n_channels,
                        rate=self.frame_rate,
                        input=True,
                        frames_per_buffer=self.frames_per_buffer)
       
        #intialise array to store frames
        self.frames=[]
    
    def start_recording (self):
        print('---------------------------------------------')
        print('Recording Audio. Press Any Key to Stop')
        print('---------------------------------------------')
 
        while self.recording is True:
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

        
    
    def stop_recording(self):
        #create input stream for key press
        input()
        #change recording status
        self.recording = False
        print('Recording Ended')
        print('---------------------------------------------')
    
    def run (self):
        
        #update recording status
        self.recording = True

        #create voice input thread
        record_thread = threading.Thread(target=self.start_recording)
        record_thread.start()

        #create key input thread
        stop_thread = threading.Thread(target=self.stop_recording)
        stop_thread.start()

        #join threads to main thread
        record_thread.join()
        stop_thread.join()

        #clear resources
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        #write to file
        with wave.open ('recording.wav', 'wb') as recording:
            recording.setnchannels(self.n_channels)
            recording.setsampwidth(pyaudio.get_sample_size(self.format))
            recording.setframerate (self.frame_rate)
            recording.writeframes(b"".join(self.frames))

        




