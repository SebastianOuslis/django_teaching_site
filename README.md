# django_teaching_site

- sudo systemctl start docker
- docker-compose up -d 
- -d runs it in the background as daemon

- if you want to remake the image
- docker image prune -a
- docker system prune -a
- docker container rm -f to kill and remove running containers


Steps to re-run site
- SSH into ec2 instance
- go to the working directory for the site code
- pull the newest git with command "git pull origin master" this will update the code
- run "docker container ls" to see currently running dock containers
- run "docker container rm -f (IDs)" with the (IDs) being the names of the running containers (should be one for django and one for nginx)
- run "docker image prune -a" and "docker system prune -a" to remove images
- run "docker-compose up -d" to run the container as a daemon (so that it runs in the background even if you log off)
