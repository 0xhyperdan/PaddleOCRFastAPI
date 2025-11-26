# PaddleOCRFastAPI

![GitHub](https://img.shields.io/github/license/cgcel/PaddleOCRFastAPI)

A simple way to deploy `PaddleOCR` based on `FastAPI`.

## Features

- [x] Local path image recognition
- [x] Base64 data recognition
- [x] Upload file recognition

## Deployment Methods

### Deploy Directly

1. Copy the project to the deployment path

   ```shell
   git clone https://github.com/cgcel/PaddleOCRFastAPI.git
   ```

   > _The master branch is the most recent version of PaddleOCR supported by the project. To install a specific version, clone the branch with the corresponding version number._

2. (Optional) Create new virtual environment to avoid dependency conflicts
3. Install required dependencies

   ```shell
   pip3 install -r requirements.txt
   ```

4. Run FastAPI

   ```shell
   uvicorn main:app --host 0.0.0.0
   ```

### Docker Deployment

Test completed in `Centos 7`, `Ubuntu 20.04`, `Ubuntu 22.04`, `Windows 10`, `Windows 11`, requires `Docker` to be installed.

1. Copy the project to the deployment path

   ```shell
   git clone https://github.com/cgcel/PaddleOCRFastAPI.git
   ```

   > _The master branch is the most recent version of PaddleOCR supported by the project. To install a specific version, clone the branch with the corresponding version number._

2. Building a Docker Image

   ```shell
   cd PaddleOCRFastAPI
   # 手工下载模型，避免程序第一次运行时自动下载，实现完全离线，加快启动速度
   sh pp-ocrv5/download_det_rec.sh

   # 使用宿主机网络
   # 可直接使用宿主机上的代理设置，例如在build时，用宿主机上的代理
   # docker build -t paddle-ocr-server:latest --network host --build-arg HTTP_PROXY=http://127.0.0.1:8888 --build-arg HTTPS_PROXY=http://127.0.0.1:8888 .
   docker build -t paddle-ocr-server:latest --network host .
   ```

3. Edit `docker-compose.yml`

   ```yaml
   version: "3"

   services:
     paddleocrfastapi:
       container_name: paddle-ocr-server # Custom Container Name
       image: paddle-ocr-server:lastest # Customized Image Name & Label in Step 2
       environment:
         - TZ=Asia/Shanghai
         - OCR_LANGUAGE=ch # support 80 languages. refer to https://github.com/Mushroomcat9998/PaddleOCR/blob/main/doc/doc_en/multi_languages_en.md#language_abbreviations
       ports:
         - "8000:8000" # Customize the service exposure port, 8000 is the default FastAPI port, do not modify
       restart: unless-stopped
   ```

4. Create the Docker container and run

   ```shell
   docker compose up -d
   ```

5. Swagger Page at `localhost:<port>/docs`

## Change language

1. Clone this repo to localhost.
2. Edit `routers/ocr.py`, modify the parameter "lang":

   ```python
   ocr = PaddleOCR(use_angle_cls=True, lang="ch")
   ```

   Before modify, read the [supported language list](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/multi_languages_en.md#5-support-languages-and-abbreviations).

3. Rebuild the docker image, or run the `main.py` directly.

## Screenshots

API Docs: `/docs`

![Swagger](https://raw.githubusercontent.com/cgcel/PaddleOCRFastAPI/dev/screenshots/Swagger.png)

## Todo

- [x] support ppocr v5
- [ ] GPU mode
- [x] Image url recognition

## License

**PaddleOCRFastAPI** is licensed under the MIT license. Refer to [LICENSE](https://github.com/cgcel/PaddleOCRFastAPI/blob/master/LICENSE) for more information.
