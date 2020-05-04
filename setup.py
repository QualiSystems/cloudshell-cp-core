from setuptools import find_packages, setup


def get_file_content(file_name):
    with open(file_name) as f:
        return f.read()


setup(
    name="cloudshell-cp-core",
    url="http://www.qualisystems.com",
    author="Quali",
    author_email="support@qualisystems.com",
    description=(
        "A repository for projects providing out of the box capabilities within CloudShell to parse and "
        "convert cloushell driver request to well defined python objects."
        "One cloudshell-cp-core For All cloudshell cloud provider shells."
    ),
    long_description=get_file_content("README.md"),
    tests_require=get_file_content("test_requirements.txt"),
    test_suite="nose.collector",
    packages=find_packages(),
    include_package_data=True,
    python_requires="~=3.7",
    install_requires=get_file_content("requirements.txt"),
    version=get_file_content("version.txt"),
    keywords="sandbox cloudshell json request",
)
