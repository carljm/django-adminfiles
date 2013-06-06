#!/bin/bash

./manage.py syncdb --noinput
pushd static
ln -s ../../adminfiles/static/adminfiles .
popd
./manage.py runserver
rm adminfiles-test.db
rm static/adminfiles
rm -rf media/*
