# Use an appropriate base image with necessary dependencies
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the source code and test files into the container
COPY . /app

# Install dependencies required for running tests
RUN pip install -r requirements.txt

# Run unit tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
