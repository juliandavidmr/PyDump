# PyDump
Dump Mysql with Python

## Features
- [x] Generate DDL Tables, Procedures, Inserts, Functions
- [x] Messages log
- [x] Tested with large amounts of data _(>2Gb)_
- [ ] Commit & push changes into gitlab

## Install
- [Install packages](https://pythonspot.com/en/mysql-with-python/)
- Install [python-gitlab](http://python-gitlab.readthedocs.io/en/stable/install.html) _[**Optional**]_
`$ pip install --upgrade python-gitlab`


### Run
```bash
git clone https://github.com/juliandavidmr/PyDump
cd PyDump
python main.py
```

> Configure `credentials` db into [credentials.py](./credentials.py)

_Testing with **Python 2.7.13**_