# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Install Gunicorn
RUN poetry add gunicorn

# Copy the rest of the application code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Run the application with Gunicorn
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
