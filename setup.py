from setuptools import setup
setup(
    name="reviewsmark",
    packages=["reviewsmark"],
    version="0.0.1.dev1",
    description="Amazon reviews summarisation engine and user interface.",
    author="Carles Balsellis Rodas <balsells96@gmail.com>, "
           "Fabio Colella <fabio.colella@aalto.fi>, "
           "Pau Batlle Franch <paubatlle11@outlook.com>, "
           "Saihan Li <saihan.li@aalto.fi>, "
           "Vytautas Mikalainis <vmikalainis@gmail.com>",
    author_email="balsells96@gmail.com,"
                 "fabio.colella@aalto.fi,"
                 "paubatlle11@outlook.com,"
                 "saihan.li@aalto.fi,"
                 "vmikalainis@gmail.com",
    url="https://github.com/MVytautas/tldr",
    download_url="https://github.com/MVytautas/tldr",
    keywords=["amazon", "reviews", "summary", "hackaton"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        "Topic :: Text Processing :: Linguistic"
        ],
    long_description="""\
Amazon reviews summarisation engine and user interface.
""",
    install_requires=['bs4',
                      'flask',
                      'gensim',
                      'nltk',
                      'numpy',
                      'pandas',
                      'requests',
                      'sklearn'],
    python_requires='>=3.4'
)
