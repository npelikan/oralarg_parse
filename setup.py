from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='oralarg_parse',
    version='0.0.0.900',
    description='Parses Supreme Court Oral Arguments',
    long_description=readme,
    author='Nick Pelikan',
    author_email='nick.pelikan@gmail.com',
    url='https://github.com/npelikan/oralarg_parse',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "extract_interruption = oralarg_parse:main"
        ]
    }
)