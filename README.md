# ml-api-fastapi
Machine learning API implementation using fastapi

# Demo
![](./pic/demo.png)

# Environment
- Mac OS X Mojave
- Python3.7.1 (for anaconda3.5)


# Requirement
- tensorflow==1.15.2
- fastapi
- uvicorn
- Jinja
- aiofiles
- python-multipart
- opencv-python

All of these are listed in [requirements.txt](./requirements.txt).

You can download the model [here](https://drive.google.com/drive/folders/1zsvSqqsmQpBW7wQQRJpiHNHpLD5mGwrB?usp=sharing) and store in ./static/model/ .


# Usage
```
$git clone https://github.com/T-Sumida/ml-api-fastapi.git
$cd ml-api-fastapi
$pip install -r requirements.txt
$uvicorn server:app
```
Go to [http://localhost:8000](http://localhost:8000)


# Author
T-Sumida

