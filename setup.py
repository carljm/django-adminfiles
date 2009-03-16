from setuptools import setup, find_packages
 
setup(
    name='django-admin-uploads',
    version='0.1.0',
    description='file upload manager and picker for Django admin',
    author='sgt.hulka',
    author_email='sgt.hulka@gmail.com',
    url='http://code.google.com/p/django-admin-uploads/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
