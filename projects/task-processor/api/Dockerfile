FROM python:3.11

WORKDIR /app

# зустановление ависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# весь код сервиса копирование
COPY . .

# запуск
CMD ["python", "app.py"]