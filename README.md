# EU_HFR_NODE_accessCleanSynchedData
Python3 scripts for periodically removing old data synchronized by data providers towards the EU HFR Node. Tools to be run at the EU HFR Node.

This application is written in Python3 language and it is designed for High Frequency Radar (HFR) data management according to the European HFR node processing workflow.

This application periodically removes data older than 30 days from the providers' home folders on the access virtual machine. It runs on the access virtual machine, that is part of the European HFR Node (EU HFR NODE) workflow for the production of HFR NRT datasets. Data providers connected to the EU HFR NODE automatically synchronize their NRT radial and total files towards the access virtual machine.

The application EU_HFR_NODE_accessCleanSynchedData.py has to be run on daily basis and it is launched via the cron.daily scheduler. When calling the application it is possible to specify the number of days in the past beyond which files are removed. If no input is specified, 30 days are used as time limit.

The application EU_HFR_NODE_accessCleanSynchedData.py takes as input the number of days in the past beyond which files are removed, lists all the files in the data providers' home folders older than the input time limit and removes them from the file system.

Usage: EU_HFR_NODE_accessCleanSynchedData.py -m <number of days in the past beyond which files are removed (default to 30)>

The required packages are:
- os
- sys
- getopt
- glob
- logging
- datetime as dt
- dateutil.relativedelta.relativedelta

Cite as:
Lorenzo Corgnati. (2024). EU_HFR_NODE_accessCleanSynchedData. DOI: 10.5281/zenodo.11475569


Author: Lorenzo Corgnati

Date: June 03, 2024

E-mail: lorenzo.corgnati@sp.ismar.cnr.it
