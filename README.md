# NCT Taeyong Taco TTS

NCT 태용 TTS with Tacotron2, Google Text-to-Speech, Google.

with [chldkato/Tacotron-Korean-Tensorflow2](https://github.com/chldkato/Tacotron-Korean-Tensorflow2)

## 순서

### 개발환경 설정

[chldkato/Tacotron-Korean-Tensorflow2](https://github.com/chldkato/Tacotron-Korean-Tensorflow2)

* 해당 레포지토리 클론
* Python 3.7
  * M1에 Homebrew에는 깔리지 않는다.
  * 문제 해결 - [참고 링크](https://diewland.medium.com/how-to-install-python-3-7-on-macbook-m1-87c5b0fcb3b5)
    * Problem is python 3.7 from homebrew only work on x86.
  * `ibrew`를 통해 해결 가능
    * `arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
    * `.zshrc`, `.bashrc`, etc =>  `alias ibrew="arch -x86_64 /usr/local/bin/brew"`
    * `$ ibrew install python@3.7`
  * Python 3.7에 맞게 해당 라이브러리 설치
    * `python3.7 -m pip install library_name`
      * pandas, numpy, librosa, tqdm, jamo

### 데이터 수집 및 전처리

#### 데이터 수집

유튜브의 V Live, Instagram Live 영상들을 WAV 파일로 다운로드.

* [V Live](https://youtube.com/playlist?list=PLPwEopeBCewQlMIZGGUKyT3yip2GDFJoL)
* [Instagram Live](https://youtube.com/playlist?list=PLA8UnQkZ80qiovpOZlo6N7_J3OYr6CP9H)

1. wav file로 다운로드
2. `silent-divide.py` 의 path 설정을 잘 바꿔서 wav 파일의 무음을 기준으로 파일을 나누기
   1. 나의 경우 20000개 정도 걸렸고, 멀티쓰레드로 돌리지 않아서 1시간 좀 넘게 걸렸다.
3. Google Cloud Storage의 Bucket에 업로드하기
   1. 직접 명령어로 업로드하는게 아니면 업로드하는 wav 파일의 갯수가 한번에 1000개가 넘지 않도록 해야 좋을 것 같다.
   2. <https://cloud.google.com/storage/docs/uploading-objects>
      1. install `gcloud`
         1. <https://computingforgeeks.com/how-to-install-gcloud-gcp-cli-on-apple-m1-macos/>
      2. `gcloud cp --recursive dir gs://my-bucket`

#### KSS Kaggle Download

<https://www.kaggle.com/datasets/bryanpark/korean-single-speaker-speech-dataset>

#### 데이터 전처리

#### 학습 데이터 준비

KSS 데이터셋을 아래와 같은 형태로 압축 해제

```text
Tacotron-Korean-Tensorflow2
  |- kss
      |- 1
      |- 2
      |- 3
      |- 4
      |- transcript.v.1.x.txt
```

위에서 클론한 레포지토리의 `preprocess.py`를 실행

```bash
python3 preprocess.py
```

### Train

```sh
python3.7 train1.py
python3.7 train2.py
```

### 인물 음성 데이터 만들기

<https://github.com/carpedm20/multi-Speaker-tacotron-tensorflow>

1. Google TTS API 사용하기
   1. API 키 설정
2. 음성을 정적을 기준으로 분리합니다.
   1. `python3.7 -m audio.silence --audio_pattern "./datasets/son/audio/*.wav" --method=pydub`
3. 작게 분리된 음성들을 Google Speech Recognition API를 사용해 대략적인 문장들을 예측하고, `음성<->텍스트` 쌍 정보를 `./script.json`에 저장합니다.
   1. `python3 speech-recog.py`
   2. Google Storage Bucket에 업로드한 wav 파일들을 Text-To-Speech API 사용해서 변환
   3. `Too many open files error`
      1. Adding the "ulimit -n 10240" statement to your bash profile using sudo nano .bash_profile makes it permanent.
4. asdf



<!-- 4. 마지막으로 학습에 사용될 numpy 파일들을 만듭니다.
   1. `python3.7 -m datasets.generate_data ./datasets/son/alignment.json` -->

### 구글 TTS, MS Azure TTS, ETC

* Azure
  * <https://learn.microsoft.com/ko-kr/azure/cognitive-services/speech-service/language-support?tabs=stt-tts#prebuilt-neural-voices>
  * <https://learn.microsoft.com/ko-kr/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python>
* Google
  * Google Text to Speech
  * Google Storage


### Tacotron

<https://github.com/carpedm20/multi-Speaker-tacotron-tensorflow>

## References

* [carpedm20/multi-Speaker-tacotron-tensorflow](https://github.com/carpedm20/multi-Speaker-tacotron-tensorflow)
* [GSByeon/multi-speaker-tacotron-tensorflow](https://github.com/GSByeon/multi-speaker-tacotron-tensorflow/blob/master/README_ko.md)
* [chldkato/Tacotron-Korean-Tensorflow2](https://github.com/chldkato/Tacotron-Korean-Tensorflow2)
* [DJ You Prjoect](https://welcome-to-dewy-world.tistory.com/106)
* 아이유 - 시리
  * <https://blog.crux.cx/iu-siri-1/>
  * <https://blog.crux.cx/iu-siri-2/>
  * <https://blog.crux.cx/iu-siri-3/>
  * <https://blog.crux.cx/iu-siri-4/>
  * <https://blog.crux.cx/iu-siri-5/>

## 예제 음성들

1. 저는 사실 사람이 아니라 강아집니다 - 민정씨
