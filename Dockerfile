# Візьми готовий Python → поклади всередину список залежностей → встанови ці залежності
FROM python:3.14-slim
#Docker бере готове середовище з Python 3.14 як основу.
WORKDIR /app
#Задає робочу папку контейнера.
COPY requirements.txt .
#Копіюємо твій requirements.txt з Mac у майбутнє середовище Docker.
RUN pip install --no-cache-dir -r requirements.txt
#Docker запускає команду встановлення залежностей.
COPY . .
#Копіюємо весь твій Todo API всередину Docker:
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
#Коли запустиш те, що ми зараз створюємо, запусти FastAPI через Uvicorn на порту 8000
