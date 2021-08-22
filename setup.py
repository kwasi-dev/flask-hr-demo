from setuptools import find_packages, setup

setup(
    name='HR Software',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'psycopg2-binary',
        'flask-sqlalchemy',
        'pyjwt',
        'flask-jwt-extended',
        'python-dotenv',
        'flask-bcrypt',
        'flask-login',
        'nfcpy'
    ],
)