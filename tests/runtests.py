#!/usr/bin/env python

import os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

def runtests():
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(
        verbosity=1, interactive=True, failfast=False)
    failures = runner.run_tests(['tests'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
