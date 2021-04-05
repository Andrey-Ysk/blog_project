# Blog
Simple blog written on Flask

# Demo:
You can try it [HERE](https://ksps.space/)

Login: `Test_1`

Password: `12345678`

# Technology
Python

Flask

jQuery

SQLite

SQLAlchemy

alembic

pytest

# Set up
Clone this repo:

`git clone https://github.com/Andrey-Ysk/blog_project.git`

Create and activate a virtual environment inside your project directory:

`python -m venv venv`

`source env/bin/activate`

Install the requirements:

`pip install -r requirements.txt`

Set up the database:

`python run.py shell`

`db.create_all()`

Set "Environment variable" to send email:

`export MAIL_USERNAME='youmail@mail.com'`

`export MAIL_PASSWORD='mailpassword'`

Run the app:

`python run.py runserver`


Navigate to localhost:5000/

Tests:

`pytest`
