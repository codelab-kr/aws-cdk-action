FastAPI docs: https://fastapi.tiangolo.com/

## Local Installation
```shell
pipenv install fastapi==0.99.0 mangum uvicorn
pipenv shell
> python 인터프리터 선택
uvicorn main:app --reload # chack if it works
pipenv run pip freeze > requirements.txt
```


## Propare to Deploy FastAPI to AWS Lambda
```shell
0. cd lambda
1. pipenv run pip install -t dependencies -r requirements.txt
1. pipenv run pip install -t dependencies  fastapi==0.99.0 mangu


2. (cd dependencies; zip ../aws_lambda_artifact.zip -r .)
3. zip aws_lambda_artifact.zip -u main.py
zip aws_lambda_artifact.zip -u books.json
```


https://youtu.be/7-CvGFJNE_o?si=6vDNWKTp2ZtmNWp8
