FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /social_network

# Set the working directory to /rest_project
WORKDIR /social_network

COPY ./requirements.txt /social_network
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . /social_network

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]