# folder structure
# my_special_package/
#     __init__.py
#     another_module.py
#     tests/
#         test_another_module.py





import setuptools

setuptools.setup(
    name='my_special_package',
    packages=setuptools.find_packages(include=["my_package∗"]),
)

