# Use an official Python runtime as a parent image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container with the new name
COPY main.py .

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "main.py"]
