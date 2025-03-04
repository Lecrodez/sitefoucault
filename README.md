# 📝 Sitefoucault 
Django-приложение для создания и прохождения опросов.

## 📜 Описание  
Этот проект позволяет:  
✅ Создавать опросы с различными типами вопросов (текст, одиночный выбор, множественный выбор, численный).  
✅ Отправлять опросы пользователям.  
✅ Сохранять ответы.  

---

## 📊 Структура базы данных  
Вот схема БД (ER-диаграмма):  

![ER Diagram](https://github.com/Lecrodez/sitefoucault/blob/main/docs/db_schema.png)

## 🚀 Установка и запуск  

### 1️⃣ Клонирование репозитория  

git clone https://github.com/Lecrodez/sitefoucault.git

cd sitefoucault

2️⃣ Установка зависимостей

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

3️⃣ Применение миграций

python manage.py migrate

4️⃣ Создание суперпользователя (если нужно)
python manage.py createsuperuser

5️⃣ Запуск сервера
python manage.py runserver
