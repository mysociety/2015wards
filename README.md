Which ward am I in?
===================

A small project that uses [MapIt](https://mapit.mysociety.org) to query ward
boundaries and show users whether their local government ward will change in
the coming election.

Install
-------
This is a fairly standard Django project, but because it uses MapIt, you need
to set up a GeoDjango database and have the associated GIS dependencies on
your system. The best resource for this is [the Django docs](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/).
You can also take a look at [the MapIt install docs](http://mapit.poplus.org/docs/self-hosted/install/).

Once you have the necessary dependencies in place, you just need to copy
`conf/general.yml-example` to `conf/general.yml` and adjust the appropriate
settings to point it to your database.

Getting data
------------
This project was designed to run off the data made available from the Ordnance
Survey in the UK, as per MapIt GB. Again, see [the MapIt docs](http://mapit.poplus.org/docs/self-hosted/import/)
for a better explanation about how to get those into your database. After you
have the standard boundaries in, the code also expects you to load some "new"
ward boundaries in, with the type code `16W`. We got these from: http://www.ordnancesurvey.co.uk/business-and-government/help-and-support/products/boundary-line.html.

Note: these latter boundaries are a bit different than the usual Boundary Line
data. We used the basic `mapit_import` management command to load them in,
rather than the UK-specific ones. We then manually added their ONS codes
using a script.
