from setuptools import setup


setup(
    packages=['justic'],
    include_package_data=True,
    use_scm_version=True,
    install_requires=[
        'jinja2',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points={
        'console_scripts': [
            'justic=justic.__main__:main',
        ],
    },
)
