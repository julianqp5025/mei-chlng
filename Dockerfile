FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD [ "python", "main.py" ]