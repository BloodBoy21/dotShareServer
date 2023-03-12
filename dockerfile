FROM python:3.10
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 80 for the container
EXPOSE 80

# Run the FastAPI server when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
