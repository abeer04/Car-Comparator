# CarCompare
Prototype for a car comparator that scrapes car seller information from major car dealing platforms (olx pakistan, pakwheels, gari) and then displays them based on best offers w.r.t. their price, mileage and model.

Documentation at https://docs.google.com/document/d/1GyWChvCrnx9HEMiFE5fz0sjyLQ1rGh_w9VoNmFf1CiQ/edit?usp=sharing

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Create a virtual environment, activate it and install the required packages:
#### Conda:
```
conda create -n CarCompareVenv python=3.7
conda activate CarCompareVenv
pip install -r requirements.txt
```
#### Python:
On Windows, run:
```
python3 -m venv CarCompareVenv
CarCompareVenv\Scripts\activate.bat
pip install -r requirements.txt
```
On Unix or MacOS, run:
```
python3 -m venv CarCompareVenv
source CarCompareVenv/bin/activate
pip install -r requirements.txt
```

## Built With
* Django
* Scrapy
* Scrapyd
* MongoDB

## Authors
* [**Abeer Butt**](https://github.com/abeer04)
* [**Mohammad Usman**](https://github.com/mohammadusman666)
* [**Muhammad Omer**](https://github.com/skydowx)