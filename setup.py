from setuptools import find_packages, setup

setup(
    name='ptdk',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    setup_requires=['libsass'],
    sass_manifests={
        'ptdk': ('static/sass', 'static/css', '/static/css')
    },
)