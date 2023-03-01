# White Market Project ReadMe
Project following the book Tango with Django - Web app development using python. Then adapted for use in a team project.

**:::Commands:::**

>Activate Conda
conda activate White_Market_Env

>try these if the above doesn't work
conda create -n White_Market_Env python=3.9
conda activate White_Market_Env
pip install django==2.2.28
pip install pillow

>Migrate the data
python manage.py migrate

>Transfer migration to live site
python manage.py makemigrations rango

>update sql
python manage.py sqlmigrate rango 0001

>runserver - start the server
python manage.py runserver

>url address of home
http://127.0.0.1:8000/