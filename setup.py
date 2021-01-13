from setuptools import setup

setup(
    name="cleanscan",
    version="0.1",
    description="Cleaner of photos and scans of documents",
    url="",
    author="Troels Frostholm Mogensen",
    author_email="troelsfrostholm@gmail.com",
    license="GNU GPLv3",
    packages=["cleanscan"],
    install_requires=["cv2", "imutils", "numpy", "scikit-image"],
    zip_safe=False,
    scripts=["bin/cleanscan"],
)
