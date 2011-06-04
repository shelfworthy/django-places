from setuptools import setup, find_packages
 
setup(
    name='django-places',
    version='0.1',
    description='Place or Location management app for django',
    author='Chris Drackett',
    author_email='chris@shelfworthy.com',
    url='http://github.com/shelfworthy/django-places',
    packages = [
        "places",
    ],
    install_requires = [
        'geopy',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        # 'Intended Audience :: Designers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Utilities',
    ],
)