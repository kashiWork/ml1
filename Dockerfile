FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the FastAPI default port
EXPOSE 7860

# Run FastAPI using Uvicorn
CMD ["uvicorn", "Fastapi_Model_Api:app", "--host", "0.0.0.0", "--port", "7860"]
