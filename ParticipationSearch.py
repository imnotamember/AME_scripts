__author__ = 'Joshua Zosky'

import csv
import os


def get_file(type_of_file):
    """
    Will ask user to select file from a numbered list presented for using as whatever type_of_file specifies
    :param type_of_file: 1=Participant ID key file, 0=data file to swap info in
    :return: filename as a string
    """
    if type_of_file == 1:
        print "Enter the number of the file you want to get Participant Id's from:"
    else:
        print "Enter the number of the file you want to change data from:"
    cwdfiles = os.listdir(os.getcwd())
    for i in range(len(cwdfiles)):
        print "%d = %s" % (i, cwdfiles[i])
    selection = raw_input("File number:")
    try:
        selection = int(selection)
    except:
        return get_file(type_of_file)
    return cwdfiles[selection]


def get_files():
    """
    Will ask user to select files from a numbered list presented for using as files to check for participation activity
    :return: a list of filenames as strings
    """
    file_name_list = []
    print "Enter the number of the 3 files you want to check participation from:"
    cwdfiles = os.listdir(os.getcwd())
    for i in range(len(cwdfiles)):
        print "%d = %s" % (i, cwdfiles[i])
    for i in range(1, 4):
        selection = raw_input("File number %s:" % i)
        try:
            selection = int(selection)
            file_name_list.append(cwdfiles[selection])
        except:
            print "Not a number! Restarting..."
            return file_name_list
    return file_name_list

participant_id_file = get_file(1)
data_files = get_files()

with open(participant_id_file, 'rb') as csvfile:
    dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    participant_id = []
    for rows in dictreader:
        temp = (rows['User Id'], rows['ID'])
        if temp not in participant_id:
            participant_id.append(temp)

print "I found these participant ID's:"
for i in participant_id:
    print i[1]
participant_choice = raw_input("Which one would you like to check?\nEnter Participant ID:")
for i in participant_id:
    if participant_choice == i[1]:
        participant_choice_hash = i[0]

im_yn = 0
counter = 0

for data_file in data_files:
    with open(data_file, 'rb') as csvfile:
        dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for rows in dictreader:
            if rows['User Id'] == participant_choice_hash:
                counter += 1
                if rows['IM_yn'] == "Yes":
                    im_yn = 1

print "Participant %s completed %s diaries." % (participant_choice, counter)
if im_yn > 0:
    print "Participant also replied a Yes to IM_yn."
else:
    print "Participant replied No to IM_yn."