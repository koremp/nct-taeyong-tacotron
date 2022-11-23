# -*- coding: utf-8 -*-

import functools

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from google.cloud import storage
from google.cloud import speech


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "taeyong"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    return list(blobs)

def transcribe_gcs(bucket_name, blob):
    client = speech.SpeechClient()

    # wav 파일이라 2채널 오디오
    # https://cloud.google.com/speech-to-text/docs/multi-channel 참조
    # https://cloud.google.com/speech-to-text/docs/sync-recognize 참조
    gcs_uri = f'gs://{bucket_name}/{blob}'
    print('transcribe: ' + gcs_uri)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='ko-KR',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=False)

    # 동기식 방법 https://cloud.google.com/speech-to-text/docs/sync-recognize
    # response = client.recognize(config=config, audio=audio)

    # 비동기식 방법 https://cloud.google.com/speech-to-text/docs/async-recognize
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    # results = response.results
    # results_string_list = map(lambda x: '"' + gcs_uri + '": ' + u'{}'.format(x.alternatives[0].transcript) + '",\n', results)
    # json_strings = functools.reduce(lambda a, b: a + b, results_string_list)

    # return json_strings

    with open("./output/script.json", "a") as script:
        for result in response.results:
            print('"'+gcs_uri+'": "'+u'{}'.format(result.alternatives[0].transcript)+'",')
            script.write('"'+gcs_uri+'": "'+u'{}'.format(result.alternatives[0].transcript)+'",\n')

if __name__ == "__main__":
    bucket_name = 'taeyong'

    blobs = list_blobs(bucket_name)
    print(len(blobs))

    with ThreadPoolExecutor(max_workers = 32) as executor:
        futures = [executor.submit(transcribe_gcs, bucket_name, blob.name) for blob in blobs]
            # process results as tasks are completed
        for future in as_completed(futures):
            print(future.result())
            with open("./script.json", "a", encoding="utf-8") as handle:
                # write to file
                handle.write(future.result())
                handle.close()

    print("Done.")
