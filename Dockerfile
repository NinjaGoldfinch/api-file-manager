FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y virtualenv

# Create virtual environment
RUN virtualenv env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
RUN /env/bin/pip install --upgrade pip

# Make sure that python knows it's in a docker container
ENV DOCKER_CONTAINER true

# Create file manager structure
RUN mkdir /files

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Start the application
RUN chmod +x app.py
CMD ["python3", "-u", "app.py"]