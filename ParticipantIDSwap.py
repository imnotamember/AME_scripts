__author__ = 'Joshua Zosky'

import csv
import os


def get_file(type_of_file):
    """
    Will ask user to select file from a numbered list presented for using as whatever type_of_file specifies
    :param type_of_file: 1=Participant ID key file, 0=data file to swap info in
    :return: filename as a string
    """
    if type_of_file:
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
        get_file(type_of_file)
    return cwdfiles[selection]


def name_file(cwdfiles=[]):
    """
    Prompts user for a filename to save updated file to
    :param cwdfiles: if passed, use this list to check against for filename to prevent overwriting
    :return: a non-overwriting filename, with .csv appended to the end
    """
    new_file_name = raw_input("New File Name:")
    if '.csv' not in new_file_name[-4:-1]:
        new_file_name += '.csv'
    if cwdfiles == []:
        os.chdir("Processed")
        cwdfiles = os.listdir(os.getcwd())
    if new_file_name in cwdfiles:
        print "File name in use, try a new one."
        name_file(cwdfiles)
    os.chdir(os.pardir)
    return new_file_name


def hash_to_participant(hash_name, user_list):
    for user_id in user_list:
        if user_id[0] == hash_name:
            return user_id[1]
    return "."

participant_id_file = get_file(1)
data_file = get_file(0)
file_name = name_file()


with open(participant_id_file, 'rb') as csvfile:
    dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    participant_id = []
    for rows in dictreader:
        temp = (rows['User Id'], rows['ID'])
        if temp not in participant_id:
            participant_id.append(temp)

with open(data_file, 'rb') as csvfile:
    dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    dict_list = []
    new_dict = {'Participant Id': []}
    for rows in dictreader:
        print rows
        rows['Participant Id'] = (hash_to_participant(rows['User Id'], participant_id))
        dict_list.append(rows)

os.chdir('Processed')  # Go down into Processed folder to save to
with open(file_name, 'w') as csvfile:
    fieldnames = sorted(dict_list[0])
    dictwriter = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
    dictwriter.writeheader()
    dictwriter.writerows(sorted(dict_list))
