#!/bin/bash -
#===============================================================================
#
#          FILE: run_report.sh
#
#         USAGE: ./run_report.sh
#
#   DESCRIPTION: 
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Carbon team
#  ORGANIZATION: WSU
#       CREATED: 11/27/2018 02:43:38 AM
#      REVISION:  ---
#===============================================================================

set -o nounset                                  # Treat unset variables as an error

#Usage function
UsageFunction()
{
    echo "Usage: $0 [-f <BegDate>] [-t <EndDate>] [-e <email>] [-u <user>] [-p <passwd>]"
    exit 1
}

#variable to check if correct items were entered
have_f=0
have_t=0
have_e=0
user=""
passwd=""

#gets the input
while getopts ":f:t:e:u:p:" opt
do
    case $opt in
        f)
            begDate=$OPTARG
            have_f=1
            #echo "The beginning date is $OPTARG"
            ;;
        t)
            endDate=$OPTARG
            have_t=1
            #echo "The end date is $OPTARG"
            ;;
        e)
            email=$OPTARG
            have_e=1
            #echo "The email is $OPTARG"
            ;;
        u)
            user=$OPTARG
            #echo "The user name is $OPTARG"
            ;;
        p)
            passwd=$OPTARG
            #echo "The password is $OPTARG"
            ;;
        *)
            UsageFunction
            ;;
    esac
done


#check to see if the beginning date, end date, and email were entered
if [[ $have_f -eq 1 && $have_t -eq 1 && $have_e -eq 1 ]]
then
    echo "Have required info"
fi

#pass begDate and endDate
#exec python3 create_report.py "$begDate" "$endDate"

HOST="137.190.19.85"
#Check exit code
#Send email
if [[ $? -eq 0 ]]
then
    tar -czvf company_trans_$begDate\_$endDate.tar company_trans_$begDate\_$endDate.dat
    `ftp -np $HOST <<END_SCRIPT
        user $user $passwd
        cd files/
        binary
        put company_trans_$begDate\_$endDate.dat
        bye
    END_SCRIPT`
    `mail -s "Sucessfully transfer file $HOST" $email <<< "Successfully created a
    transaction report from $begDate to $endDate"`
elif [[ $? -eq -1 ]]
then
    `mail -s "The create_report program exit with code -1" $email <<< "Bad Input parameters $begDate $endDate"`
else
    #for -2 exit code
    `mail -s "The create_report program exit with code -2" $email <<< "No transactions available from $begDate to $endDate"`
fi
exit 0
