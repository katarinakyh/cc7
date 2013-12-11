cc7
===

Deploying with mysql, nginx and guni_corn
========================================
* : install virtual env
=======================
$ sudo apt-get update
$ sudo apt-get install python-pip
$ sudo pip install virtualenv
$ virtualenv env
$ source env/bin/activate

* : install git and clone project
=================================
$ sudo apt-get install git 
$ git clone https://github.com/katarinakyh/cc7.git


* : Install: python-mysqldb
========================================================
$ sudo apt-get install python-mysqldb

* : login into mysql: 
====================
$ mysql -u root -p
mysql> create database cc7;
mysql> quit 


* : Install: gcc need for pillow
========================================================
$ sudo apt-get install python-dev
$ sudo apt-get install libevent-dev

Install requirement
===================
$ cd ccc7
$ pip install -r requirements

* : Nginx conf:
================
$ sudo apt-get install nginx
$ cd /etc/nginx/sites-available/
$ sudo nano cc7.org 
--- copy/past this -----------------
server {
        listen 80; ## listen for ipv4; this line is default and implied

        root /home/adminuser/vb/vb/vamlingbolaget;
        index index.html index.htm;

        # Make site accessible from http://localhost/
        server_name localhost;

        location /theme/static/  { # STATIC URL
                alias /home/adminuser/cc7/cc7/theme/static/;
        }

        location /media/ { # MEDIA URL
                alias /home/adminuser/cc7/cc7/media/;
        }

        location / {
                proxy_pass_header Server;
                proxy_redirect off;
                client_max_body_size 100M;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Scheme $scheme;
                proxy_connect_timeout 20;
                proxy_read_timeout 20;
                proxy_pass http://127.0.0.1:8000;
        }
        error_page 500 502 503 504 /media/50x.html;
}
----- end ---------------------------
Ctrl X and Y to save 
$ sudo ln -s cc7.org ../sites-enabled/cc7.org
$ mkdir backup 
$ mv default backup/default
$ sudo /etc/init.d/nginx reload
$ pip install MySQL-python 

$ nano local_settings.py
--- copy/past this -----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name_of_your_database',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'OPTIONS': { 'init_command': 'SET storage_engine=MyISAM; SET names "utf8"' },
        }
}

MEDIA_ROOT = '/home/palle/Project/django/cc7/cc7/media/'
----- end ---------------------------
move default from 
$ cd 
$ cd cc7 
$ > implied :pip install gunicorn
$ python manage.py run_gunicorn 

4 installed apps:
=================
    'imagekit',
    'south',
    'userena',
    'guardian',
    'easy_thumbnails',
    'gunicorn',


