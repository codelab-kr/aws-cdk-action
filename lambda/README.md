FastAPI docs: https://fastapi.tiangolo.com/

## Local Installation
```shell
pipenv install fastapi uvicorn
pipenv shell
> python 인터프리터 선택
uvicorn main:app --reload # chack if it works
pip freeze > requirements.txt
```

## Deploying FastAPI to AWS EC2

```shell
# Launch an EC2 instance
# Choose Amazon Linux 2 AMI
# Choose t2.micro
# Configure Security Group
# Add Rule: HTTP, Port 80, Source Anywhere
# Connect to the EC2 instance

sudo yum update -y
sudo yum install -y python3-pip nginx git vim
git clone https://github.com/pixegami/fastapi-tutorial.git
cd fastapi-tutorial
python3 -m pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

ll /etc/nginx/conf.d/
sudo vim /etc/nginx/conf.d/default.conf

server {
    listen 80;
    server_name 3.35.209.50;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

sudo service nginx restart

```
## Check it works
http://3.35.209.50/docs

<br>

# FastAPI Tutorial for Lambda
```shell
cd lambda
pip install -t lib -r requirements.txt
cd lib && zip -r ../lambda.zip .
cd ..
zip lambda.zip -u main.py
zip lambda.zip -u books.json
```