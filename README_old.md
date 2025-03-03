Requirements: Python ul instalat si repository ul clonat

1) Create virtual environment with python (vezi care merge la tine)
```
python -m venv venv
```
sau 
```
py -m venv venv
```

2) Activate environment
```
.\venv\Scripts\activate
```

3) Install python packages
```
pip install -r requirements.txt
```
4) MakeMigration
```
python manage.py makemigrations
```
5) Migrate
```
python manage.py migrate
```
6) .env text:
```
DB_ENGINE = django.db.backends.postgresql
DB_NAME = polihack24
DB_USER = postgres
DB_PASSWORD = <parola ta>
DB_HOST=localhost
DB_PORT=5432

OPENAI_API_KEY = <on whatsapp>
```
7) Run server
```
python manage.py runserver
``` 
