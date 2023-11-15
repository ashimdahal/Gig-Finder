FROM python:3.8-slim

WORKDIR /app

COPY .env /app
COPY main.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt


# Make port 80 available to the world outside this container
EXPOSE 80

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

# Run the application using flask run
CMD ["flask", "run", "--host=0.0.0.0"]
