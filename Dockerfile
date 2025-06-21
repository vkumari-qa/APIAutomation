# Dockerfile: runs FastAPI tests with pytest-html

# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy project files into container
COPY . .

# 4. Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 5. Default command: run tests and generate report
CMD ["pytest", "--html=reports/report.html", "--self-contained-html"]
