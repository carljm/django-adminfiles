#!/bin/bash

./manage.py syncdb --noinput
pushd media
ln -s ../../adminfiles/media/adminfiles .
popd
./manage.py runserver
rm adminfiles-test.db
rm media/adminfiles
