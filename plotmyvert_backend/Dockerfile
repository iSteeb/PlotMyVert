# Use an official Python runtime as a parent image
FROM python:3.12-alpine3.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

RUN apk add --no-cache build-base

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

EXPOSE 8001
# Run the application
CMD ["gunicorn", "plotmyvert_backend.wsgi:application", "--bind", "0.0.0.0:8001", "--access-logfile", "-", "--error-logfile", "-"]