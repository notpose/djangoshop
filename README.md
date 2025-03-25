# djangoshop
git clone https://github.com/notpose/djangoshop.git

cd djangoshop

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
