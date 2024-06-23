FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt  /app/
RUN pip install -r requirements.txt
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 1234
ENV POSTGRES_DB postgres
ENV POSTGRES_HOST localhost
COPY . /app/
COPY demo.py ./
COPY urls.py ./
CMD ["sh", "-c", "python /app/urls.py && python /app/demo.py"]