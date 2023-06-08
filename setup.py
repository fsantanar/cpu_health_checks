from setuptools import find_packages, setup

setup(
    name='cpu_health_checks',
    version='1.0.0',
    author='Felipe Santana Rojas',
    description='Package to make a series of CPU health checks',
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.3',
        'psutil==5.9.0',
        'PyYAML==6.0',
        'tqdm==4.62.3',
    ],
    python_requires='>=3.5',
)
