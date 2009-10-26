from setuptools import setup, find_packages
 
setup(
    name='django-admin-uploads',
    version='0.2.0',
    description='file upload manager and picker for Django admin',
    author='sgt.hulka',
    author_email='sgt.hulka@gmail.com',
    url='http://code.google.com/p/django-admin-uploads/',
    packages=find_packages(),
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
    package_data={'upload': ['media/upload/*.*',
                             'media/upload/mimetypes/*.png',
                             'templates/upload/*.html']}
)
