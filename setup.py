from setuptools import setup, find_packages

setup(
    name="dbzpy",
    version="0.0.1",
    author="Bader AlAttar",
    description="Cyborg DBZ YAML spec ingestion",
    python_requires=">=3.8",
    packages=find_packages(),
    package_data = {
        "": ["*"],
    },
    requires=[
        "jinja2",
        "jsonschema",
        "pyyaml"
    ]
)