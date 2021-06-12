FROM python:3.7

WORKDIR /

RUN pip install streamlit==0.72.0

RUN export API_ENDPOINT=http://api:8000

EXPOSE 8000 8501

COPY ./tagler /tagler

WORKDIR /tagler

CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]