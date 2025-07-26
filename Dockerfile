FROM python:3.10-slim

# Maak werkdirectory aan
WORKDIR /app

# Kopieer requirements + installeer packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer je hele project (bot.py, memory.py, etc.)
COPY . .

# Start de bot
CMD ["python", "bot.py"]
