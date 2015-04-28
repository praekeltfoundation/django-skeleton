django-skeleton
===============

A Sample Django application that illustrates what bits make up a
sane Django based web app deployment.

|Travis|_ |Coveralls|_

::

    $ virtualenv ve
    $ source ve/bin/activate
    (ve)$ pip install -r requirements.pip

You can use Git_ to merge this repository into your own code
if you would like to use it as a starting point::

    $ git remote add skeleton https://github.com/praekelt/django-skeleton.git
    $ git fetch skeleton
    $ git merge skeleton/develop

Tests
-----

We use Nose_ for running our tests. It's not fantastic but it does the job
well enough.

By adding ``django_nose`` to the installed apps, Django's existing testing
tools are replaced by Nose. Running tests is now the same with the difference
being that Nose gives you better tools to analyze your code base for things
like test coverage.

::

    (ve)$ ./manage.py test
    nosetests --verbosity 1
    Creating test database for alias 'default'...
    Raven is not configured (logging is disabled). Please see the documentation for more information.
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK
    Destroying test database for alias 'default'...

We use Travis_ and Coveralls_ for our open-source projects for
`Continuous Integration`_ and `Code Coverage`_. This project has a
``.travis.yml`` file which Travis_ uses to automatically run the full
test suite when new code is pushed to any of the repository's branches.


South
-----

South_ manages your schema and data migrations well enough.
As part of a deploy we expect any schema changes needed
to be part of your repository and handled by south.

For your initial schema::

    (ve)$ ./manage.py schemamigration --initial <app-name>

For subsequent schema changes::

    (ve)$ ./manage.py schemamigration --auto <app-name>

The schema changes can be applied manually with::

    (ve)$ ./manage.py migrate

Or generally what happens as part of a deploy is::

    (ve)$ ./manage.py syncdb --noinput --no-initial-data --migrate

As an example, the sample ``app1`` application's migrations were created
with the following commands after creating the ``app1/models.py`` file::

    (ve)$ ./manage.py schemamigration --initial app1
    Creating migrations directory at '.../django-skeleton/app1/migrations'...
    Creating __init__.py in '.../app1/migrations'...
     + Added model app1.App1Model
    Created 0001_initial.py. You can now apply this migration with: ./manage.py migrate app1

A later change to the model definition is detected by South_ and a new
schema migration is generated to reflect this change::

    (ve)$ ./manage.py schemamigration --auto app1
     + Added field gender on app1.App1Model
    Created 0002_auto__add_field_app1model_gender.py.
    You can now apply this migration with: ./manage.py migrate app1


Supervisord
-----------

Supervisord_ manages your processes and allows us to ensure that your
applications are a) running and b) come up at boot should the server
be restarted for whatever reason.

The folder ``etc/`` has ``supervisord.conf`` file that's read by ``supervisord``.
The application specific files are in ``etc/conf.d/*.conf``.

For each process that needs to be run by your application ensure that the
process is included in a ``.conf`` file::

    (ve)$ supervisord
    (ve)$ supervisorctl
    celery                           RUNNING    pid 24069, uptime 0:35:04
    django                           RUNNING    pid 24070, uptime 0:35:04
    supervisor> restart celery
    celery: stopped
    celery: started
    supervisor> tail -f celery
    ==> Press Ctrl-C to exit <==
    [2013-06-18 21:41:28,571: WARNING/MainProcess] celery@Simons-MacBook-Air.local ready.
    [2013-06-18 21:41:28,576: INFO/MainProcess] consumer: Connected to redis://localhost:6379/0.
    ...

Celery
------

Anything that requires moderate to heavy lifting, which could cause a
potentially slow response time, should be left for Celery to handle.

This includes sending emails, logging, database based cleanup tasks.

Celery allows you to define ``tasks`` that are scheduled from your Django
views but which are run by the Celery worker running in the background,
allowing your Django application to return the HTTP response to the user
as soon as possible.

How to use Celery from Django is documented at `celeryproject.org
<http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#defining-and-calling-tasks>`_

This skeleton application uses Redis_ as the broker for Celery,
in production this is going to be RabbitMQ_.

A sample application called ``celery_app`` is part of this skeleton as an
example. Visit http://localhost:8000/celery/ to see it in action if you've
got ``supervisord`` running.


Gunicorn
--------

Gunicorn_ is the application server we're using to servce our Django
applications with. Generally this sits behind Nginx_ and HAProxy_.

We are expecting your Django applications to be run with this, no exceptions.


Sentry
------

Sentry_ is a realtime error logging and aggregation platform.
We have a dedicated installation for our Django based projects.

Raven_ is the client that submits the errors to Sentry. We will
supply you with a key for you to configure your raven client with.


.. _South: http://south.aeracode.org/
.. _Redis: http://redis.io/
.. _RabbitMQ: http://rabbitmq.org/
.. _Supervisor: http://supervisord.org/
.. _Nginx: http://nginx.org/
.. _HAProxy: http://haproxy.1wt.eu/
.. _Gunicorn: http://gunicorn.org/
.. _Sentry: https://github.com/getsentry/sentry
.. _Raven: https://github.com/getsentry/raven-python
.. _Git: http://git-scm.com/
.. _Nose: https://nose.readthedocs.org/en/latest/
.. _Code Coverage: https://en.wikipedia.org/wiki/Code_coverage
.. _Continue Integration: https://en.wikipedia.org/wiki/Continuous_Integration

.. |Travis| image:: https://travis-ci.org/praekelt/django-skeleton.png?branch=develop
.. _Travis: https://travis-ci.org/praekelt/django-skeleton

.. |Coveralls| image:: https://coveralls.io/repos/praekelt/django-skeleton/badge.png?branch=develop
.. _Coveralls: https://coveralls.io/r/praekelt/django-skeleton
