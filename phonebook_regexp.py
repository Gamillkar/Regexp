from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

def conversion_name():
    fix_full_name = []
    pattern = re.compile(r"^([А-ЯЁ][\w]*)(\,|\s)([А-ЯЁ][\w]*)(\,|\s)([А-ЯЁ][\w]+)?(\,)")
    for contact in contacts_list[1:]:
        str_contact = ','.join(contact)
        full_name = pattern.sub(r"\1,\3,\5,", str_contact)
        fix_full_name.append(full_name)
    return fix_full_name

def fix_number():
    fix_number_name = []
    number_main = re.compile(r'\,(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})(\,*)')
    number_additional = re.compile(r'\,\s\(*\доб. (\d*)\)*')
    for basic_number in conversion_name():
        fix_number = number_main.sub(r',+7(\2)\3-\4-\5,', basic_number)
        if 'доб' in fix_number:
            fix_number = number_additional.sub(r' доб.\1', fix_number)
        fix_number_name.append(fix_number)
    return fix_number_name

def clear_data():
    clear_comma_list = []
    del_more_comma = re.compile(r'\,+')
    for item in fix_number():
        fix_comma = del_more_comma.sub(r',', item)
        clear_comma_list.append(fix_comma)
    return clear_comma_list

def transfer_data():
    name_surname_list = []
    transfer_data = []
    repeat_data = []
    for contact in clear_data():
        contact_name = contact.split(',')
        name_surname = f'{contact_name}'
        name_surname_control = (f'{contact_name[0]},{contact_name[1]}')
        # print(name_surname, name_surname_1)
        if name_surname_control not in name_surname_list:
            name_surname_list.append(name_surname_control) #добавление name и surname  в отд. лист
            transfer_data.append(contact_name) #добавление недублируемых данных в отд. лист
        else:
            repeat_data.append(contact.split(','))
    return transfer_data, repeat_data

def union_contact():
    list_contact, repeat_data = transfer_data()
    # перемещение пункта position и email
    for repeat_contact in repeat_data:
        rep_contact = (repeat_contact[0], repeat_contact[1])

        for contact in list_contact:
            contact_name = (contact[0], contact[1])
            # если из повторяющ. list name и sername совпадает с общим list,то извлекаеться инф. и вставляеться в общий лист
            if contact_name == rep_contact and len(repeat_contact)>=4:
                move_data = repeat_contact[4]
                contact.insert(4, move_data) #вставка position
            elif contact_name == rep_contact:
                if '@' in ','.join(repeat_contact):
                    email = [data_contact for data_contact in repeat_contact if '@' in data_contact]
                    email = email[0]
                    contact.insert(-1, email) #вставка email
    header = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    list_contact.insert(0, header)
    return list_contact

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(union_contact())





