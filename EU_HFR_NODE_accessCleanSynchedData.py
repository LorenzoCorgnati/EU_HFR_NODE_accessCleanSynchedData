#!/usr/bin/python3


# Created on Mon Jun 03 14:12:26 2024

# @author: Lorenzo Corgnati
# e-mail: lorenzo.corgnati@sp.ismar.cnr.it


# This application periodically removes data older than 30 days from the providers'
# home folders on the access virtual machine. This application runs on the access 
# virtual machine, that is part of the European HFR Node (EU HFR NODE) workflow 
# for the production of HFR NRT datasets.
# Data providers connected to the EU HFR NODE automatically synchronize their NRT radial and
# total files towards the access virtual machine.

import os
import sys
import getopt
import glob
import logging
import datetime as dt
from dateutil.relativedelta import relativedelta

####################
# MAIN DEFINITION
####################

def main(argv):
    
#####
# Setup
#####
       
    # Set the argument structure
    try:
        opts, args = getopt.getopt(argv,"m:h",["memory=","help"])
    except getopt.GetoptError:
        print('Usage: EU_HFR_NODE_accessCleanSynchedData.py -m <number of days in the past beyond which files are removed (default to 15)>')
        sys.exit(2)
        
    if not argv:
        memory = 15       # number of days in the past beyond which files are removed (default to 15)
        
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: EU_HFR_NODE_accessCleanSynchedData.py -m <number of days in the past beyond which files are removed (default to 15)>')
            sys.exit()
        elif opt in ("-m", "--memory"):
            memory = int(arg)
            
    # Create logger
    logger = logging.getLogger('EU_HFR_NODE_accessCleanSynchedData')
    logger.setLevel(logging.INFO)
    # Create logfile handler
    logFilename = '/var/log/EU_HFR_NODE_NRT/EU_HFR_NODE_accessCleanSynchedData.log'
    lfh = logging.FileHandler(logFilename)
    lfh.setLevel(logging.INFO)
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] -- %(levelname)s -- %(module)s - %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
    # Add formatter to lfh and ch
    lfh.setFormatter(formatter)
    # Add lfh and ch to logger
    logger.addHandler(lfh)
    
    # Initialize error flag
    cPDerr = False
    
    logger.info('Cleaning started.')
    
    try:
        
#####
# Set the earliest date for data cleaning
#####        
        
        # Set datetime of the earliest date for data cleaning
        startDate = (dt.datetime.utcnow()- relativedelta(days=memory)).strftime("%Y-%m-%d")
        
        # Convert starting date from string to timestamp
        mTime = dt.datetime.strptime(startDate,"%Y-%m-%d").timestamp()
        
#####
# Set the folder path patterns for the folders to be cleaned
#####
        
        # Set the providers' home base folder pattern
        provBasePattern = '/home/hfr_*'
        
        # Set the path pattern for the folders to be cleaned
        srcFolderPattern = os.path.join(provBasePattern, 'NRT_HFR_DATA', 'HFR-*')
    
####
# Clean old data
#####        
        
        # List the files to be removed
        filesToBeRemoved = [file for file in glob.glob(os.path.join(srcFolderPattern,'**/*'), recursive = True) if os.path.getmtime(file) < mTime]   
        # Keep only files (not folders)
        filesToBeRemoved = [item for item in filesToBeRemoved if not os.path.isdir(item)]

        # Remove files
        for file in filesToBeRemoved:
            os.remove(file)
            logger.info('File ' + file + ' removed.')

    except Exception as err:
        cPDerr = True
        logger.error(err.args[0])    
    
    
####################
    
    if(not cPDerr):
        logger.info('Successfully executed.')
    else:
        logger.error('Exited with errors.')
            
####################


#####################################
# SCRIPT LAUNCHER
#####################################    
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
