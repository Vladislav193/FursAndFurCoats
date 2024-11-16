---

# Интернет-магазин "Меха и шубы"

Этот проект представляет собой backend-часть интернет-магазина, где пользователи могут авторизоваться, просматривать каталог товаров, добавлять товары в корзину и оформлять заказы.

## Стек технологий

- Python 3.x
- Django & Django REST Framework
- PostgreSQL
- JWT для авторизации
- Swagger для документации API
- Внешние интеграции:
  - Авторизация через соц.сети Яндекс и ВК
  - SMTP клиент для отправки уведомлений о заказе
  - Платежные системы Юкасса — для обработки платежей.
  - Dadata API — для валидации и авто-заполнения данных пользователей при регистрации.

## Установка

1. Клонируйте репозиторий:

     git clone https://github.com/Vladislav193/FursAndFurCoats.git
2. 
   cd ваш_репозиторий
   
2. Создайте виртуальное окружение и установите зависимости:

   python -m venv venv && . venv/Scripts/activate

   pip install -r requirements.txt
   
3. Создайте и настройте базу данных PostgreSQL:

   - Создайте базу данных и пользователя.
   - В файле settings.py укажите данные для подключения к базе данных:

         DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     
4. Выполните миграции:

     python manage.py makemigrations

   python manage.py migrate
   
5. Создайте суперпользователя для доступа к админке:

     python manage.py createsuperuser
   
6. Запустите сервер разработки:

     python manage.py runserver
   
## Документация API

API документация доступна по адресу http://127.0.0.1:8000/api/docs/ (Swagger UI).

### Основные эндпоинты

- Товары
  - POST /products/ — Получение товаров по категории.
  - GET /product/<id>/ — Получение данных о конкретном товаре, включая описание, изображение, цену, характеристики и возможность фильтрации по цене.

- Категории
  - GET /categories/ — Список категорий с поддержкой вложенности.

- Корзина
  - GET, POST, PUT, DELETE /cart/ — Работа с корзиной пользователя: получение, добавление, изменение и удаление товаров.

- Заказы
  - POST /order/ — Создание заказа. После создания заказа корзина очищается.

- Авторизация
  - Поддерживается авторизация через социальные сети (Яндекс, ВК).

## Интеграции

1. SMTP клиент — для отправки email-уведомлений после успешного создания заказа.
2. Платежные системы Юкасса — для обработки платежей.
3. Dadata API — для валидации и авто-заполнения данных пользователей при регистрации.

## Тестирование

Запустите тесты для проверки работы всех эндпоинтов:
pytest

## Docker

Для запуска проекта в контейнере Docker используйте Dockerfile и docker-compose:

1. Соберите контейнер:

     docker-compose build
   
2. Запустите контейнер:

     docker-compose up
   

## Особенности

- Поддержка JWT авторизации.
- Поддержка вложенных категорий.
- Автоматическая очистка корзины после создания заказа.
- Swagger-документация.

