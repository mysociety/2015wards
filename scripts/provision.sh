#!/bin/sh

# Stop script execution as soon as there are any errors
set -e

pwd
now=$(date +"%T")
echo "$now Running provision.sh"

if [[ ! -f /vagrant/conf/general.yml ]] ; then
    echo 'It looks like you forgot to create a general.yml file.'
    echo 'Make sure you follow the two setup steps in README.md.'
    exit
fi

if [[ ! -f /vagrant/mapit_2015_ward_boundaries.sql.dump ]] ; then
    echo 'It looks like you forgot to prepare a MapIt Database dump.'
    echo 'Make sure you follow the two setup steps in README.md.'
    exit
fi

# Use the en_GB.utf8 locale
sudo update-locale LANG=en_GB.utf8

# Install the packages we need
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev python-pip postgresql postgresql-9.1-postgis postgresql-server-dev-9.1 libgdal1-1.7.0 ruby-sass python-psycopg2 python-shapely python-yaml python-gdal

cd /vagrant
sudo pip install --timeout=120 --use-mirrors -r requirements.txt

# Set up PostgreSQL database
sudo pg_dropcluster --stop 9.1 main
sudo pg_createcluster --locale=en_GB.utf8 --start 9.1 main
chmod +x scrips/postgis_template.sh
sudo -u postgres scrips/postgis_template.sh
echo "CREATE USER mapit WITH PASSWORD 'mapit' CREATEDB;" | sudo -u postgres psql
sudo -u postgres createdb --owner=mapit mapit

echo 'localhost:5432:mapit:mapit:mapit' > ~/.pgpass # Stops pg_restore asking for a password.
chmod 600 ~/.pgpass

# Import boundary data from existing MapIt database dump
cat mapit_2015_ward_boundaries.sql.dump | pg_restore --clean --no-owner --username=mapit --dbname=mapit --host=localhost

# Set shell login message
echo "-------------------------------------------------
Welcome to your 2015wards vagrant machine

Run the web server with:
  cd /vagrant
  ./manage.py runserver 0.0.0.0:8000

Then visit http://127.0.0.1:8000 to use 2015wards
-------------------------------------------------
" | sudo tee /etc/motd.tail > /dev/null
