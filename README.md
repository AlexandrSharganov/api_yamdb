## YaMDb
# Educational project
YMDB project gathers users' reviews for different works of art

---

# List of required libraries and frameworks:
* requests==2.26.0
* django==2.2.16
* djangorestframework==3.12.4
* PyJWT==2.1.0
* pytest==6.2.4
* pytest-django==4.4.0
* pytest-pythonpath==0.7.3
* djangorestframework-simplejwt==4.7.2
* django-filter==21.1

# How to start the project:
1. Copy the project with SSH and establish a virtual environment:
```
'python -m .venv venv'
```
2. Activate the virtual environment and install the requirements:
```
.venv/scripts/activate

pip install -r requirements.txt
```
3. To load up the database:
```
python csvtodb.py
```
4. Change the directory and run server:
```
cd .\api_yamdb\

python manage.py runserver
```
---
# Developers:
- [fifififanfanfan](https://github.com/fifififanfanfan)
- [Alexandr Sharganov](https://github.com/AlexandrSharganov)
- [Stanislav Savitskiy](https://github.com/Stanislav-Sav)