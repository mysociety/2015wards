#!/bin/sh

# Stop script execution as soon as there are any errors
set -e

pwd
now=$(date +"%T")
echo "$now Running provision.sh"

if [ ! -f /vagrant/mapit_2015_ward_boundaries.sql.dump ]; then
    echo 'It looks like you forgot to prepare a MapIt Database dump.'
    echo 'Make sure you follow the setup step in README.md.'
    exit 1
fi

wget -O install-site.sh --no-verbose https://github.com/mysociety/commonlib/raw/master/bin/install-site.sh
sed -i -r -e "s,mapit,2015wards," install-site.sh
sudo DEBIAN_FRONTEND=noninteractive sh install-site.sh --dev 2015wards vagrant 127.0.0.1.xip.io

# Import boundary data from existing MapIt database dump
pg_restore --clean --no-owner --username=vagrant --dbname=mapit /vagrant/mapit_2015_ward_boundaries.sql.dump

# Set shell login message
echo "-------------------------------------------------
Welcome to your 2015wards vagrant machine

Run the web server with:
  cd 2015wards
  ./manage.py runserver 0.0.0.0:8000

Then visit http://127.0.0.1:8000 to use 2015wards
-------------------------------------------------
" | sudo tee /etc/motd.tail > /dev/null
