#!/bin/sh

install_website_packages
install_postgis
add_postgresql_user
pip install --requirement "$REPOSITORY/requirements.txt"
su -l -c "$REPOSITORY/bin/install-as-user '$REPOSITORY' '$UNIX_USER'" "$UNIX_USER"
