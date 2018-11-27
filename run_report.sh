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
exit 0
