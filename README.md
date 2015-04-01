Which ward am I in?
===================

A small project that uses [mapit](http://mapit.mysociety.org) to query ward
boundaries and show users whether their local government ward will change in
2015.

Quick install: Vagrant
----------------------

This project has a Vagrantfile, but before you can run it, you need to make sure the following things have been set up:

1. Copy `conf/general.yml-example` to `conf/general.yml`, set `DJANGO_SECRET_KEY` to some random string of characters, and set `2015WARDS_DB_USER`, `2015WARDS_DB_NAME`, and `2015WARDS_DB_PASS` all to `'mapit'`.
2. Place a database dump from an existing MapIt Wards 2015 install, named `mapit_2015_ward_boundaries.sql.dump` into the root level of the project.

Once these two requirements are satisfied, you can run `vagrant up`.

If you run `vagrant up` without having created `conf/general.yml` and `mapit_2015_ward_boundaries.sql.dump`, it will warn you and exit, so you can create them.

Install
-------
This is a fairly standard Django project, but because it uses Mapit, you need
to set up a GeoDjango database and have the associated GIS dependencies on
your system. The best resource for this is [the Django docs](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/). You can also take a look at [the MapIt install docs](http://mapit.poplus.org/docs/self-hosted/install/)

Once you have the necessary dependencies in place, you just need to copy
`conf/general.yml-example` to `conf/general.yml` and adjust the appropriate
settings to point it to your database

Getting data
------------
This project was designed to run off the data made available from the Ordnance
Survey in the UK, as per MapIt GB. Again, see [the MapIt docs](http://mapit.poplus.org/docs/self-hosted/import/)
for a better explanation about how to get those into your database. After you
have the standard boundaries in, the code also expects you to load some "new"
ward boundaries in, with the type code `15W`. We got these from: http://www.ordnancesurvey.co.uk/business-and-government/help-and-support/products/boundary-line.html.

Note: these latter boundaries are a bit different than the usual Boundary Line
data. We used the basic `mapit_import` management command to load them in,
rather than the UK-specific ones. See: https://github.com/mysociety/mapit/issues/152#issuecomment-76703854
for some of the issues we had with them and the work-arounds we used.
