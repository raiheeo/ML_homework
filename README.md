🧠 ML_homework
это учебный проект по машинному обучению, в котором реализована модель предсказания цен на жильё.

📁 Структура проекта
ML_homework/
├── hm_app/                   # Основное приложение
│   ├── __init__.py
│   ├── models.py             # Определение моделей
│   ├── routes.py             # Маршруты приложения
├── migrations/               # Миграции базы данных
├── house_price_model_job.pkl # Сериализованная модель
├── scaler.pkl                # Сериализованный скейлер
├── alembic.ini               # Конфигурация Alembic
├── req.txt                   # Зависимости проекта
└── .env                      # Переменные окружения

🚀 Быстрый старт
Клонируй репозиторий:
git clone https://github.com/raiheeo/ML_homework.git
cd ML_homework
Создай виртуальное окружение и активируй его:
python -m venv venv
source venv/bin/activate  # Для Unix или MacOS
venv\Scripts\activate     # Для Windows
Установи зависимости:
pip install -r req.txt

⚙️ Используемые технологии
Языки программирования: Python
Фреймворки и библиотеки:
Fastapi
SQLAlchemy
Alembic
scikit-learn
NumPy

📈 Описание модели
Модель машинного обучения обучена на датасете цен на жильё и способна предсказывать стоимость недвижимости на основе входных данных.


