FROM python as base

# Add curl for healthcheck
RUN apt-get update && \
    apt-get install -

# Set the application working directory
WORKDIR /usr/local/app

# Install our requirements.txt
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the app
CMD ["python", "app.py"]

# Copy our code from the current folder to the working directory inside the container
COPY . .