# RentModel-RestAPI

REST API for simulate some model with Category/Product/User Object
with registrations and authorization functionality
based on [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server ONLY FOR UNIX sys

### Installing
1. __Run on localhost__
* 1.1. Make sure you have virtualenv and Python3 installed on your system 
```
pip3 install virtualenv
```
* 1.2. Clone the repo: 
```
git clone https://github.com/vbondyrev/RentModel-RestAPI
```
* 1.3. Install the virtualenv: virtualenv venv
* 1.4. Activate the virtual environment: 
```
source venv/bin/activate
```
* 1.5. Install Python Requirements: 
```
pip3 install -r requirements.txt 
```
* 1.6. Run this command in console: 
```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
* 1.7. Run app.py and check this endpoint:
			[http://0.0.0.0:5000/api/swagger](http://0.0.0.0:5000/api/swagger) 

* 1.8. Add user Admin
       In DB "Role" add admin aslo
       Only Admin user could add any categories
       Only registered and authorized users could get info 

### Endpoints
 All endpoints represented in Swagger:
 ![ScreenShot](https://raw.github.com/{username}/RentModel-RestAPI/screenshot/swagger.png)

 _Thanks for attention and have a nice day! :)_
