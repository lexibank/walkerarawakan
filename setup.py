from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_walkerarawakan',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_walkerarawakan'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'walkerarawakan=lexibank_walkerarawakan:Dataset',
        ]
    },
    extras_require={"test": ["pytest-cldf"]},
    install_requires=[
        'pylexibank>=2.0',
    ]
)
