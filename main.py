from record import Recording
import transcribe
import pyaudio

if __name__ == "__main__":
    recorder = Recording(format=pyaudio.paInt16, channels=2)
    recorder.run()
    print ('Starting Transcription')
    transcribe.voice_to_text('recording.wav')

