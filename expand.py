#!/usr/bin/python3
import os
import csv
from pathlib import Path
import re

dir_in = "X:\\xxx\\steamapps\\common\\Stellaris" #Stellaris' path
dir_out = "X:\\Users\\xxx\\Documents\\Paradox Interactive\\Stellaris\\mod\\xxx" #output path
list_csv = ".\\list.csv" #scv file path
p_txt_paths = [dir_in + '\\common', dir_in + '\\events']
### ↑ These is windows' path, if linux pls replacement as appropriate ###

mapping = {}
with open(list_csv, mode='r', newline='') as csvfile:
    expand_list = csv.reader(csvfile)
    for row in expand_list:
        mapping[row[0] + ' = yes'] = row[1]
        mapping[row[0] + ' = no'] = 'NOT = { ' + row[1] + ' }'

for i in p_txt_paths:
    for f_name in list(Path(i).rglob('*.txt')):
        expanded = 0
        with open(f_name, 'r', encoding='utf-8', newline='\n') as infile:
            newline = []
            for oldline in infile.readlines():
                tmpline = oldline
                for key,value in mapping.items():
                    if key in tmpline:
                        #tmpline = tmpline.replace(key, value)
                        tmpline = re.sub(rf'\b{key}\b', value, tmpline)
                        expanded = 1
                newline.append(tmpline)
        if expanded:
            outpath = str(f_name).replace(dir_in, dir_out)
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            with open(outpath, 'w', encoding='utf-8', newline='\n') as outfile:
                outfile.writelines(newline)
            print("expanded: " + str(f_name))