# Первичная настройка работы проекта, основанного на фреймворке Django

## Описание проекта
Проект предназначен для маркетплейса Megano с целью размещения товаров для продажи.
Данный проект разработан на основе Django REST Framework. API контракт может использоваться для работы сторонних приложений

## Контракт для API
Названия роутов и ожидаемую структуру ответа от API endpoints можно найти в спецификации по адресу ниже (проект при этом должен быть запущен):
```http request
    /api/swagger/
```

## Установка виртуального окружения и библиотек/пакетов

Установка всех необходимых библиотек производится с использованием файла с зависимостями requirements.txt

Перед установкой пакетов и библиотек, необходимо удостовериться, что все действия происходят внутри виртуального
окружения. Поэтому сначала необходимо его создать (если этого еще не было сделано)

```text
python3 -m venv venv (python3 - unix / python - windows)
```

Данная команда создаст папку venv в папке, откуда была выполнена команда, и в терминале появится запись *(venv)*
Теперь можно выполнить установку всех требуемых для работы библиотек и пакетов.
Для этого необходимо в терминале (находясь в папке, в которой расположен файл requirements.txt) выполнить следующую
команду:

```text
pip install -r requirements.txt
```

## Подготовка базы данных PostgreSQL и создание виртуального окружения переменных

Подключаемся к консоли Postgres, выполнив следующий код

```text
sudo -u postgres psql
```

Создаем базу данных, создаем пользователя, меняем некоторые настройки по рекомендации из документации Django
(кодировка, чтение транзакций и часовой пояс), открываем для нового пользователя все возможности работы с новой БД

```postgresql
CREATE DATABASE db_name;
CREATE USER username WITH PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE db_name TO username;
```

В директории вместе с текущим файлом расположен файл ".env.template". Нужно переименовать его в ".env" и переместить
в одну директорию вместе с файлом settings.py, а потом заполнить по принципу:

```dotenv
SECRET_KEY=secret_key_from_django_settings.py
DEBUG=True_or_False
ALLOWED_HOSTS=some_hosts

#в соответствии с созданными пользователем и БД
DB_NAME=db_name
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
```

В файле settings.py необходимо сделать следующее:

```python
# вверху файла добавить два импорта
import os
import environ

env = environ.Env()
environ.Env.read_env()

# В соответствии с названиями переменных (выше) нужно внести правки в указанные ниже строчки
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': ''
    }
}
```


Теперь необходимо провести миграции (создание таблиц в базе данных), создать суперпользователя, запустить сервер и
проект готов к работе:

```text
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```
