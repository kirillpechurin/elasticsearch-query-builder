import setuptools

VERSION = '0.2'

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="elasticsearch-query-builder",
    version=VERSION,
    python_requires=">=3.8",
    author="kirillpechurin",
    author_email="k.pechurin04@gmail.com",
    description="A tool for forming a single query body for further search in Elasticsearch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kirillpechurin/elasticsearch-query-builder",
    project_urls={
        "Repository": "https://github.com/kirillpechurin/elasticsearch-query-builder"
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "License :: OSI Approved :: Apache Software License",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=[
        "elasticsearch_query_builder",
        "elasticsearch_query_builder.fields",
    ],
)
