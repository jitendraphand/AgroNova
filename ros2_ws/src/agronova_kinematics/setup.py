from setuptools import setup

pkg = "agronova_kinematics"
setup(
    name=pkg,
    version="0.1.0",
    packages=[pkg],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + pkg]),
        ("share/" + pkg, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    license="MIT",
    tests_require=["pytest"],
    entry_points={"console_scripts": ["diff_drive_node = agronova_kinematics.diff_drive_node:main"]},
)
