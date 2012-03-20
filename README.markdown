Description
--------------------
This is a basic people system, developed for adcloud with a view
to allowing the company to view photos and basic details of all people
working at adcloud


Installation
--------------------
`pip install requirements.txt`


Special Notes
--------------------
The system makes use of a specific fork of the django-socialregistration 
app. This fork has added a nuber of process hooks to allow the user
to specify particular user attributes from google (and other openid providers)


Deployment
--------------------
A fabric file has been included
`fab deploy_live`
