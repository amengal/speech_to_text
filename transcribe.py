import requests

API_KEY = 'f58e04cfdc404ad0990fa929d01dc264'
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

#header to include in our http requests
headers = {'authorization': API_KEY}

audio_file = 'recording.wav'


#function to upload file to server and receive url of uploaded audio file
def get_upload_url(file_name):
    
    def read_file (file_name, chunk_size=5242880):
        with open (file_name, 'rb') as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers = headers, data=read_file(file_name))
    audio_url = upload_response.json()['upload_url']
    return audio_url

#function to begin transcription of the uploaded audio url
def transcribe(audio_url):
    transcript_request = {'audio_url': audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    job_id = transcript_response.json()['id']

    return job_id

# function to poll server for transcription

def get_poll_response (transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    poll_response = requests.get(polling_endpoint, headers=headers)
    return poll_response.json()

#function to retrieve result
def get_transcription_result (transcript_id):
    
    while True:
        poll_response = get_poll_response(transcript_id)
        if poll_response['status'] == 'completed':
            return poll_response, None
        elif poll_response['status'] == 'error':
            return poll_response, poll_response['error']



#call functions and write to file
def voice_to_text (audio_file):
    #call functions
    audio_url = get_upload_url(audio_file)
    transcript_id = transcribe(audio_url)
    result, error = get_transcription_result(transcript_id)

    #write result to file
    if error == None:
        with open ('transcript.txt', 'w') as file:
            file.write(result['text'])











