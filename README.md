# Automated Inventory Reporting System

[![GitHub Super-Linter](https://github.com/cfarrell987/AIRS/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Purpose

Currently, Reports provided from SnipeIT need to be manually configured each time. AIRS intends to make it easier by configuring once and running it on a regular schedule. This will assist in Auditing and reduce man hours taken on configuring and cleaning reports.

## Usage 
1. Run `pip install -r requirements.txt` To install Depenedencies(See Below)
2. Run `setup.py install`
3. Create _resources folder_ and create _api_key.txt_
4. Inside _api_key.txt_ add `Bearer $APIKEY`
5. Run main.py

## Dependencies
1. [Numpy](https://pypi.org/project/numpy/)
2. [Pandas](https://pypi.org/project/pandas/)
3. [Requests](https://pypi.org/project/requests/)
