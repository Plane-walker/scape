from setuptools import setup, find_packages

setup(
    name="scape",
    version="0.8.8",
    keywords=["pip", "raspberry pi"],
    description="a framework for raspberry pi developing",
    long_description=open('README.rst').read(),
    license="MIT Licence",

    url="https://github.com/Plane-walker/scape",
    author="Plane-walker",
    author_email="a990990@163.com",

    packages=find_packages(exclude=['*test']),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
