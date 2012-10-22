Description
--------------------
This is a basic people system, developed for adcloud with a view
to allowing the company to view photos and basic details of all people
working at adcloud


Installation
--------------------
`easy_install pip` 
`pip install virtualenv virtualenvwrapper` 
`pip install -r requirements.txt` 

`python manage.py syncdb` 
`python manage.py migrate` 
`python manage.py loadfixtures` 
`python manage.py validate` 
`python manage.py runserver_plus` 

Special Notes
--------------------
The system makes use of a specific fork of the django-socialregistration 
app. This fork has added a nuber of process hooks to allow the user
to specify particular user attributes from google (and other openid providers)


Deployment
--------------------
A fabric file has been included
`fab deploy_live`
