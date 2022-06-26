# Yamdb
## Пет-прект
YaMDb Собирает отзывы и рецензии пользователей на различные произведения

---

## Список используемых библиотек и фреймворков:
* requests==2.26.0
* django==2.2.16
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* djangorestframework-simplejwt==4.7.2
* django-filter==21.1
## Как запустить проект:
1. Скопируйте проект с помощью SSH и установите виртуальное окружение:
```
'python -m .venv venv'
```
2. Активируйте виртуальное окружение и установите все зависимости:
```
.venv/scripts/activate
pip install -r requirements.txt
```
3. Чтобы загрузить данные из базы данных в проект:
```
python csvtodb.py
```
4. Поменяйте директорию и запустите сервер:
```
cd .\api_yamdb\
python manage.py runserver
```
---
## Разработчики:
-[Александр Шарганов](https://github.com/AlexandrSharganov)
-[Станислав Савицкий](https://github.com/fifififanfanfan)
-[иван Чугунов](https://github.com/fifififanfanfan)