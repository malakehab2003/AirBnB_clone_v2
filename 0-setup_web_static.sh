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
</html>" > "/data/web_static/releases/test/index.html"

# remove sympolic link if exists
if [ -L "/data/web_static/current" ]
then
        sudo rm /data/web_static/current
fi

# create new sympolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change owner to ubuntu and group recursively
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 777 /data/

# Check if alias already exists, replace it; otherwise, add the alias
sudo sed -i '48 i \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
