import setuptools

with open("README.md", encoding="utf-8") as f:
	long_description = f.read()

setuptools.setup(
	name="pintool",
	version="0.1",
	descripton="Program for playing with Pin",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	license="MIT",
	author="SuperStormer",
	author_email="larry.p.xue@gmail.com",
	url="https://github.com/SuperStormer/pintool2",
	project_urls={"Source Code": "https://github.com/SuperStormer/pintool2"},
	entry_points={"console_scripts": ["pintool=pintool.pintool:main"]},
)
