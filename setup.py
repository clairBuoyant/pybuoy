from setuptools import find_packages, setup

setup(
    name="buoy-py",
    version="0.1.0",
    author="Kyle J. Burda",
    description="Python wrapper for NDBC buoy data.",
    url="https://github.com/clairBuoyant/buoy-py",
    project_urls={
        "Bug Tracker": "https://github.com/clairBuoyant/buoy-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">3.9",
)
