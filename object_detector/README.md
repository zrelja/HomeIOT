## Requirements

1. Git
2. Docker engine
3. Docker compose

## Set Up

1. Use git clone to pull this branch onto the server.
2. If you are going to dev, go to docker/web/web-entrypoint.sh and change npm run build to npm run start
3. Change to directory in which ``docker-compose.yml`` is located.
4. run ``docker-compose build``
5. run ``docker-compose up``

## Update project on server

1. Git pull the new code.
2. If you changed only one container, build just that container without downtime with this:
    docker-compose up -d --no-deps --build <service_name>


## Notes

* Make sure you access everything with sudo. 
* Syntax for creating super user from shell is ``python manage.py createsuperuser``
* https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
* https://github.com/Seedstars/django-react-redux-base
