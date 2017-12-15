FROM python:3.6.3

WORKDIR /consumer

ADD requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY consumer /consumer

CMD ["python", "/timeout_script.py", "psql -h \"postgres\" -U postgres -c \\l", "--timeout=600", "--wait_interval=5", "--on_success='python manage.py runserver'"]