# carbon

# create_report.py
## The create_report.py script takes two input parameters: Beginning Date and End Date (YYYMMDD)
## The dates will be used to query the DB transaction information
## create_report.py formats the input dates to match the format of the DB dates
## If no transactions are available within the specified date range the program will exit with a 2
## Sends a report of the found results via FTP


# run_report.sh
## The run_report.sh script calls the create_report.py script and gathers the input dates
## An email address is requested to send messages to the user about the file transfer
## A username and password are also requested for a FTP account to transfer the file
## run_report.sh will check the exit codes and will send an appropriate message to the user depending on the exit code
