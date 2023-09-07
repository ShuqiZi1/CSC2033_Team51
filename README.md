Gather - Team 51 Global Partnership Project
===========================
[![license](https://img.shields.io/github/license/:user/:repo.svg)](LICENSE.md)

## Table of Contents
- [Background](#background)
- [Introduction](#introduction)
- [Install](#install)
- [Usage](#usage)
- [Collaboration](#collaboration)
- [License](#license)

***
## Background
The Global Partnership for Sustainable Development Data is a multi-stakeholder network of more than 300 data 
champions working to galvanize political commitments, align strategic priorities, foster collaboration, spur 
innovations, build capacity and enhance trust in the booming data ecosystems of the 21st century.
(cite from: [linked-in](https://www.linkedin.com/company/global-partnership-for-sustainable-development-data))
***
## Introduction
This website is a platform for multi-stakeholder exchanges. They can communicate and cooperate on this website from the 
fields of finance, science, technology and trade, leading to a win-win situation.

The website offers different functions such as Chat, Charitable actions, Posts, Location, Search and Quiz. Various 
functions can be accessed by different user groups (individual users, companies and charities).
***
## Requirements
Gather(Global Partnership Project) supports at a minimum the currently supported versions of Python and MySQL:

* Python 3.8 +
* MySQL 8.0.21 +
***
## Install
This project uses [Python 3.8](https://www.python.org/downloads/) and [MySQL](https://dev.mysql.com/downloads/).
Go check them out if you don't have them locally installed.

To install the latest `Python`, there are two methods:  
Method 1: Download the Python 3.8 installer from the official [Python website](https://www.python.org/downloads/), 
and double-click to run and install it;  
Method 2: If `Homebrew` is installed, install it directly through the command brew install python3.

To install the latest `MySQL`, use following command:  
``` 
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm 
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
yum install mysql-server
```

To run the project a valid Newcastle University login is required to be put into config.py
Details for the admin account can be found in login.py, including the Authy key.
***
## Usage
To get started, Creation of virtual environments is done by executing the command `venv`:
```python
python3 -m venv /path/to/new/virtual/environment
```
Then, use following lines to install dependencies:
``` python
# install related library
pip install -r requirements.txt
```
Import database settings in Python console:
```python
from models import init_db
init_db()
```
Please edit the Configuration in the top right corner of `PyCharm` and set the Script path to `app.py` in the root directory. 
Run it after clicking `Apply`.

Admin Actions:

* View all basic user information.
* Ban or not ban basic user.
* View all post information.
* Delete post.
* Make push message for users who want to receive email.
* All user's action.


User Actions:
* View all posts.
* Add new post.
* Update delete their own posts.
* Like posts.
* View info page.
* Test with a quiz.
* Edit personal information.
* View own profile.
* Contact with website developer.
***
## Collaboration
If you wish to work with us please contact us: [gblparnershipncl@ncl.ac.uk.](gblparnershipncl@ncl.ac.uk.)
***
## LICENSE
[Newcastle © CSC2033 Team 51](LICENSE.md)

## Link to repository
https://github.com/newcastleuniversity-computing/CSC2033_Team51
