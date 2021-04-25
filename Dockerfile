FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

EXPOSE 80

COPY ./backend /tagler/backend
COPY ./frontend /tagler/frontend
COPY ./models /tagler/models

ENTRYPOINT [ "python3" ]

CMD [ "tagler/backend/app.py" ]
#CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "80"]