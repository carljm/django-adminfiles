from setuptools import setup
import subprocess
import os.path

try:
    # don't get confused if our sdist is unzipped in a subdir of some 
    # other hg repo
    if os.path.isdir('.hg'):
        p = subprocess.Popen(['hg', 'parents', r'--template={rev}\n'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not p.returncode:
            fh = open('HGREV', 'w')
            fh.write(p.communicate()[0].splitlines()[0])
            fh.close()
except (OSError, IndexError):
    pass
    
try:
    hgrev = open('HGREV').read()
except IOError:
    hgrev = ''
    
long_description = (open('README.rst').read() + 
                    open('CHANGES.rst').read() +
                    open('TODO.rst').read())

setup(
    name='django-adminfiles',
    version='0.5.0',
    description='File upload manager and picker for Django admin',
    author='sgt.hulka',
    author_email='sgt.hulka@gmail.com',
    maintainer='Carl Meyer',
    maintainer_email='carl@dirtcircle.com',
    long_description=long_description,
    url='http://bitbucket.org/carljm/django-adminfiles/',
    packages=['adminfiles', 'adminfiles.templatetags', \
              'adminfiles.management', 'adminfiles.management.commands'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    test_suite='tests.runtests.runtests',
    package_data={'adminfiles': ['media/adminfiles/*.*',
                                 'media/adminfiles/mimetypes/*.png',
                                 'templates/adminfiles/render/*.html',
                                 'templates/adminfiles/render/image/*.html',
                                 'templates/adminfiles/uploader/*.html',
                                 'locale/*/LC_MESSAGES/*']}
)
