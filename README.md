# E-commerce-Website

# Creating virtual environment Linux

```
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
```

# Creating virtual environment Windows

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Do migration

```
python manage.py migrate
```

Load data into database

To run

```
python manage.py runserver
```

To delete all migrations

```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```