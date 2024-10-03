from setuptools import setup, find_packages

setup(
    name='project-DreamTeam15',
    version='0.1.0',
    packages=find_packages(include=['project-DreamTeam15', 'project-DreamTeam15.*']),
    install_requires=[
        'prompt_toolkit==3.0.47',
        'setuptools==72.2.0',
        'wcwidth==0.2.13'
    ]
)
