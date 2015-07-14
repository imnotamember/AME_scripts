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


def swap_date_format(dict_list, column):
    for i in dict_list:
        temp_date_time = i[column]
        if temp_date_time.isspace() is False and temp_date_time != '':
            temp_date_time = temp_date_time.replace('/', '-')
        else:
            temp_date_time = '.'
        i[column] = temp_date_time
    return dict_list



def swap_values_numerals(dict_list, key, translator):
    for i in dict_list:
        temp = i[key]
        if temp in translator:
            temp = translator[temp]
        else:
            temp = '-999'
        i[key] = temp
    return dict_list


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
        rows['Participant Id'] = (hash_to_participant(rows['User Id'], participant_id))
        dict_list.append(rows)

correct_dates = ['IM_time1',
                 'IM_time2',
                 'IM_time3',
                 'Alc_start1',
                 'Alc_stop1',
                 'Alc_start2',
                 'Alc_stop2',
                 'SexActivities2']

y_n = {'Yes': 1, 'No': 0}
y_n_skip = {'Yes': 1, 'No': 0, 'Skipped': -888.00}
v1_3 = {'1': 1, '2': 2, '3 or more': 3}
alc_0_1 = {'Yes- I find I cannot remember things I did or said when drinking': 1,
           'No- I do not have difficulty remembering things I did or said when drinking': 0
           }
IM_type = {'A thought': 1, 'An image': 2, 'A combination of a thought and image': 3}
v0_4_skip = {'Skipped': -888.00,
             'Not at all': 0,
             'Slightly': 1,
             'Moderately': 2,
             'Very': 3,
             'Extremely': 4
             }
vivid_1_7_skip = {'Skipped': -888.00,
                  '1- No image at all': 1,
                  '2': 2,
                  '3': 3,
                  '4': 4,
                  '5': 5,
                  '6': 6,
                  '7- As clear as normal vision': 7
                  }
intox_0_11 = {'0- Not at all': 0,
              '1': 1,
              '2': 2,
              '3': 3,
              '4': 4,
              '5': 5,
              '6': 6,
              '7': 7,
              '8- Drunk as I have ever been': 8,
              '9': 9,
              '10': 10,
              '11- More drunk than I have ever been': 11
              }

values_to_numerals = {'Dreams': y_n,
                      'IM_yn': y_n,
                      'Alc_yn': y_n,
                      'Alc_2nd': y_n,
                      'IM_num': v1_3,
                      'IM_Distress1': v0_4_skip,
                      'IM_Distress2': v0_4_skip,
                      'IM_Distress3': v0_4_skip,
                      'NoAlc_5': v0_4_skip,
                      'IM_type1': IM_type,
                      'IM_type2': IM_type,
                      'IM_type3': IM_type,
                      'IM_vivid1': vivid_1_7_skip,
                      'IM_vivid2': vivid_1_7_skip,
                      'IM_vivid3': vivid_1_7_skip,
                      'NoAlc_1': y_n_skip,
                      'NoAlc_2': y_n_skip,
                      'NoAlc_3': y_n_skip,
                      'SexActivities1': y_n_skip,
                      'SexActivities3': y_n_skip,
                      'Alc_intox1': intox_0_11,
                      'Alc_intox2': intox_0_11,
                      'Alc_intoxNow': intox_0_11,
                      'Alc_black1': alc_0_1,
                      'Alc_black2': alc_0_1,
                      }

for key in values_to_numerals.keys():
    if key in dict_list[0].keys():
        dict_list = swap_values_numerals(dict_list, key, values_to_numerals[key])

for column in correct_dates:
    if column in dict_list[0].keys():
        dict_list = swap_date_format(dict_list, column)

os.chdir('Processed')  # Go down into Processed folder to save to
with open(file_name, 'w') as csvfile:
    fieldnames = sorted(dict_list[0])
    dictwriter = csv.DictWriter(csvfile, fieldnames, lineterminator='\n')
    dictwriter.writeheader()
    dictwriter.writerows(sorted(dict_list))
