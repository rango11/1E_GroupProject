# 1E_GroupProject
WAD2 Group Project

CLEAN PROJECT NOTES:

**Commands**
    Activate conda - create:
        conda create -n WhiteMarket python=3.9

    Activate:
        conda activate WhiteMarket

    Django install:
        pip install django==2.2.28

    Pillow install:
        pip install pillow 

    Create a project:
        django-admin startproject White_Market_Project

    Run Server:
        python manage.py runserver

    Creating APP:
        python manage.py startapp WhiteMarket

    Migrate Databse changes:
        python manage.py migrate

    Create Super User:
        python manage.py createsuperuser

    Sync chaged to DB (ie. when tables have been added)
        python manage.py makemigrations WhiteMarket


State::::: 
got up to chapter 7. most exercises skipped, database and pop script un editted.
Issues::::
some stuff is case sensitve which is an issue because of the way I have named it, use PascalCase in the first instance and all lower if an error occours.
Couldn't for the life of me get media {{ MEDIA_URL }} working in the HTML, I will be having another bash on Monday and adding my CSS. 