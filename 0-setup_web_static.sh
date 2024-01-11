@@ -0,0 +1,37 @@
#!/usr/bin/env bash
#Bash script that sets up web servers for the deployment of web_static

#Install nginx.
sudo apt update
sudo apt install -y nginx

#Create default nginx folder for the pages.
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

#Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
sudo touch /data/web_static/releases/test/index.html

#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo rm /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

#Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist).
# This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

#Overwite file content.
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

#Create an endpoint to index.html.
sudo sed -i "s/server_name _;/&\n\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t\tindex index.html;\n\t}\n/" /etc/nginx/sites-enabled/default

#Restart nginx server.
sudo service nginx restart
