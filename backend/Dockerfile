FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Hugging Face Spaces runs on port 7860
ENV PORT=7860
EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "run:app"]
