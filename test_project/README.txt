A bare-bones Django project for live-testing django-adminfiles; particularly
Javascript functionality that can't easily be unit-tested.

Run ``pip install -r requirements.txt`` to install all the dependencies you
need into a virtualenv; then run ``./run_test_project.sh`` to set up a test
database and run the test server on ``http://localhost:8000``.

Use admin/admin to log into the admin of the test server.

Ideally we'd have Selenium tests for this stuff.
