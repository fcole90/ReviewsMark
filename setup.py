from setuptools import setup
setup(
    name="tldr",
    packages=["tldr"],
    version="0.0.1.dev1",
    description="Amazon reviews summarisation engine and user interface.",
    author="Hackaton Team",
    author_email="chose_an@email.com",
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
                      'numpy',
                      'gensim',
                      'nltk',
                      'pandas',
                      'sklearn'],
    python_requires='>=3.4'
)
