FROM python:3.12-alpine

WORKDIR /crawler

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]