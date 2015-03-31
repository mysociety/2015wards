#!/bin/sh

# Stop script execution as soon as there are any errors
set -e

pwd
now=$(date +"%T")
echo "$now Running provision.sh"

# Use the en_GB.utf8 locale
sudo update-locale LANG=en_GB.utf8

# Install the packages we need
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev python-pip postgresql postgresql-9.1-postgis postgresql-server-dev-9.1 libgdal1-1.7.0 ruby-sass python-psycopg2 python-shapely python-yaml python-gdal

cd /vagrant
sudo pip install --timeout=120 --use-mirrors -r requirements.txt

# Set up the Django database
./manage.py syncdb --noinput
./manage.py migrate

# Set shell login message
echo "-------------------------------------------------
Welcome to your 2015wards vagrant machine

Run the web server with:
  cd /vagrant
  ./manage.py runserver 0.0.0.0:8000

Then visit http://localhost:8000 to use 2015wards
-------------------------------------------------
" | sudo tee /etc/motd.tail > /dev/null
