from setuptools import setup, find_packages

setup(
    name="document_to_audio",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'gTTS',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'PyPDF2',
        'python-docx',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to convert documents to audio and save them to Google Drive",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
