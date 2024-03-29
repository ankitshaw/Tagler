FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN apt update
RUN apt-get install -y unixodbc unixodbc-dev

RUN pip3 install -r requirements.txt


EXPOSE 5000 8501

COPY ./backend /backend
COPY ./frontend /frontend
COPY ./models /models

WORKDIR /backend

#CMD ["cd /frontend/tagler"]
#CMD ["streamlit", "run", "web_app.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]