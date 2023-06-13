from setuptools import setup, find_packages

setup(
    name='Analyst_Bi',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'altair==4.2.2',
        'numpy==1.24.2',
        'pandas==1.5.3',
        'streamlit==1.22.0',
        'streamlit-echarts==0.4.0'
        
    ],
    entry_points={
        'console_scripts': [
            'Analyst_Bi = Analyst_Bi.main:main'
        ]
    },
)