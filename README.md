# NCT Taeyong Taco TTS

NCT 태용 TTS with Tacotron2, Google Text-to-Speech, Google.

GPU에서 멈춰있나...? GPU로 학습할 수 있는 서비스를 이용해보자.

with [chldkato/Tacotron-Korean-Tensorflow2](https://github.com/chldkato/Tacotron-Korean-Tensorflow2)

using pytorch instead of tf2

## 순서

### 개발환경 설정

[chldkato/Tacotron-Korean-Tensorflow2](https://github.com/chldkato/Tacotron-Korean-Tensorflow2)

해당 레포지토리 클론

### 학습할 인물의 음성 데이터 수집 및 전처리

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

### 인물 음성 데이터 만들기

#### Google Speech Recognition API

Google Storage Bucket에 업로드한 wav 파일들을 Text-To-Speech API 사용해서 변환

작게 분리된 음성들을 Google Speech Recognition API를 사용해 대략적인 문장들을 예측하고, `음성<->텍스트` 쌍 정보를 `./output/script.json`에 저장합니다.

`$python3 speech-recog.py`

#### KSS Kaggle File Download

<https://www.kaggle.com/datasets/bryanpark/korean-single-speaker-speech-dataset>

### 학습 데이터 준비

데이터셋을 아래와 같은 형태로 압축 해제

```text
datasets
|- kss
  |- 1
  |- 2
  |- 3
  |- 4
  |- transcript.v.1.x.txt
|-taeyong
 |-alignment.json
  |-1.wav
  |-2.wav
  ...

```

내 환경은 macbook m1 air 이여서, 이 프로그램의 환경 중 python3.7과 호환이 되지 않는다는 문제가 있다

그래서 Python 3.7을 사용할 수 있는 가상 환경에 kss 데이터셋(4GB)과 내 데이터셋 (4.34GB)을 업로드하여 직접 `preprocess.py`와 `train.py`를 실행할 수 있는 환경을 만드는 중이다.

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

## Errors

### Python3.7 install on M1 Chip

M1에 Homebrew에는 깔리지 않는다.

문제 해결 - [참고 링크 - macbook m1에 python3.7을 설치하는 방법(영문)](https://diewland.medium.com/how-to-install-python-3-7-on-macbook-m1-87c5b0fcb3b5)

  > Problem is python 3.7 from homebrew only work on x86.

해결 방법은 다음과 같다.

1. brew x86 version을 설치

    ```bash
    $arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

2. rc 파일에 `ibrew` alias를 추가한다.

    `alias ibrew="arch -x86_64 /usr/local/bin/brew"`

3. `$ibrew install python@3.7` 를 통해 python3.7을 설치
   1. Python 3.7에 맞게 스크립트에서 사용하는 라이브러리 설치
   2. `$python3.7 -m pip install ${library_name}`
      1. `pandas`, `numpy`, `librosa`, `tqdm`, `jamo` 등

### Too many open files error

Adding the `ulimit -n 10240` statement to your shell profile using sudo rc file makes it permanent.

### Python 3.6 install on M1 Mac

<https://okke-formsma.github.io/>

1. Set up ‘ibrew’, or a x86 brew

    ```sh
    arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "alias ibrew=\"arch -x86_64 /usr/local/bin/brew\"" >> ~/.zshrc
    ```

2. Install anaconda x86-64

    ```sh
    ibrew install anaconda
    /usr/local/anaconda3/bin/conda init zsh
    ```

3. Create python 3.6 x86-64 venv

    ```sh
    conda create --name venv_py36 python=3.6
    ibrew install libpq
    export PKG_CONFIG_PATH="/usr/local/opt/libpq/lib/pkgconfig"
    export LDFLAGS="-L/usr/local/opt/libpq/lib"
    export CPPFLAGS="-I/usr/local/opt/libpq/include"
    pip install psycopg2==2.8.6 --force-reinstall --no-cache-dir
    ibrew install imagemagick freetype
    pip install python-magic
    ```

### Install requirements.txt failed

#### Install ipdb failed

```sh
pip3 install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

requirements.txt의 ipdb를 설치할 수 없었다.

conda로는 설치가 불가능하고, pipenv를 통해 설치할 수 있다.

#### ImportError: cannot import name 'Feature', ERROR: No matching distribution found for MarkupSafe==1.0

`MarkupSafe==1.0.0`으로 되어있는 `requirements.txt` 파일을 `MarkupSafe==1.1.1`로 바꿔줬다



## 예제 음성들

1. 저는 사실 사람이 아니라 강아집니다 - 민정씨
