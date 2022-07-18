FROM python:3
ENV PYTHONUNBUFFERED 1
# RUN git clone -b dev https://github.com/bervr/DRF_test_task.git ./drftt
WORKDIR /drftt
COPY ./drftt /drftt
RUN ls .
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py makemigrations && python manage.py migrate  && python manage.py migrate  --run-syncdb && python manage.py runserver 0.0.0.0:8000