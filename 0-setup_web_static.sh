#!/usr/bin/env bash
# update package lists
# check if nginx not installed and install it
if [ ! -x /usr/sbin/nginx ]
then
	sudo apt-get -y update
        sudo apt-get -y install nginx
fi

# create directories if not exists
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# create a html file
touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create new sympolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change owner to ubuntu and group recursively
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data/

# Check if alias already exists, replace it; otherwise, add the alias
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" | sudo tee /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
