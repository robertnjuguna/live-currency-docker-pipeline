# specifying the python package
FROM python:3.10-slim

# setting up the working directory
WORKDIR /app

COPY requirements.txt .

#installing the packages in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline.py .

CMD ["python", "pipeline.py"]


