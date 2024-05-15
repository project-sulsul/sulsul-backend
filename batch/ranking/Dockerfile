FROM python:slim-buster

RUN mkdir -p /lambda
COPY . /lambda
WORKDIR /batch/ranking

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD ["lambda_function.lambda_handler"]
