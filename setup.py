from setuptools import setup

setup(
    name='Tackling Cancer',
    packages=['tackling_cancer'],
    include_package_data=True,
    install_requires=[
        'flask',
        'watson_developer_cloud',
        'setuptools',
        'opencv_python',
        'numpy',
        'Werkzeug',
        'matplotlib',
        'mpld3',
        'Pillow',
        'scikit_learn',
    ],
)