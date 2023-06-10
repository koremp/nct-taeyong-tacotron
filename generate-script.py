from google.cloud import storage
from google.cloud import speech

def transcribe_gcs(gcs_uri):

    client = speech.SpeechClient()

    # wav 파일이라 2채널 오디오
    # https://cloud.google.com/speech-to-text/docs/multi-channel 참조
    # https://cloud.google.com/speech-to-text/docs/sync-recognize 참조

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 44100,
        language_code='ko-KR',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=False)

    # 동기식 방법 https://cloud.google.com/speech-to-text/docs/sync-recognize
    response = client.recognize(config=config, audio=audio)

    # 비동기식 방법 https://cloud.google.com/speech-to-text/docs/async-recognize
    # operation = client.long_running_recognize(config=config, audio=audio)
    # response = operation.result(timeout=90)

    # json 파일에 내용추가
    with open("./alignment.json", "a") as script:
        for result in response.results:
            print('"'+gcs_uri+'": "'+u'{}'.format(result.alternatives[0].transcript)+'",')
            script.write('"'+gcs_uri+'": "'+u'{}'.format(result.alternatives[0].transcript)+'",\n')

# while(cnt <= 783):
#     # gs://~ 는 버킷 내부의 오디오 데이터 경로
#     transcribe_gcs("gs:///210213/"+str(cnt)+".wav")
#     cnt+=1

# for i in range(1, 13423):
for i in range(1, 13423):
    try:
        transcribe_gcs("gs://taeyong-audio-wav/{0}.wav".format(i))
    except:
        print("except - {0}".format(i))
