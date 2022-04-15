# Самоделкин

## Описание

Сервис для предпринимателей, предоставляющий набор инструментов для продвижения своего дела и поиска клиентов.

## Стек технологий

#### Backend

- python3.7
- Django REST framework

#### [Frontend](https://github.com/Volokhov-mda/sitodel)

- React
- HTML5 + CSS3 + JS

## Инструкция по запуску

1. Установите [python3](https://www.python.org/)

2. Склонируйте репозиторий и перейдите в директорию с проектом
   ```bash
   $ git clone https://github.com/PPnP/Samodelkin.git && cd Samodelkin
   ```

3. Создайте и активируйте виртуальное окружение
   ```bash
   $ virtualenv --python=python3 venv
   $ source venv/bin/activate
   ```

4. Установите зависимости
   ```bash
   $ pip3 install -r requirements.txt
   ```

5. Добавьте файл ```Samodelkin/.env``` c переменными, заданными согласно формату файла ```Samodelkin/.env.example```.

6. Выполните миграцию базы данных
   ```bash
   $ ./manage.py migrate --run-syncdb
   ```

7. Запустите сервер
   ```bash
   $ ./manage.py runserver
   ```

Просмотр Swagger UI будет доступен по адресу ```/swagger```.

## Справка

- Создание суперпользователя (username == email)
  ```bash
  $ ./manage.py createsuperuser
  ```

- Сброс содержимого базы данных
  ```bash
  $ ./manage.py flush
  ```
