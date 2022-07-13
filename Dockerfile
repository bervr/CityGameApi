FROM python:3
ENV PYTHONUNBUFFERED 1
# ADD ./drftt
RUN git clone -b dev https://github.com/bervr/DRF_test_task.git ./drftt
WORKDIR /drftt/drftt
RUN ls .
RUN pip install --upgrade pip && pip install -r requirementes.txt
VOLUME /drftt/drftt
EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000