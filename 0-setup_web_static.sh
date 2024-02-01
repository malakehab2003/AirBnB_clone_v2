#!/usr/bin/env bash
# sets up web servers for the deployment of web_static
# Create directories recursively if they don't exist
if [ ! -x /usr/sbin/nginx ]
then
apt-get -y update
apt-get -y install nginx
fi
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/
sed -i -e "0,/    }/ s#    }# }\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n#" /etc/nginx/sites-available/default
nginx -t
nginx -s reload
