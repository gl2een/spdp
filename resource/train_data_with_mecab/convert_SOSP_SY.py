#-*- coding:utf-8 -*-

import glob

file_list = glob.glob('../origin_data/*.conll')

for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as f:
        print(file_name)
        out = open(file_name+'.converted', 'w')

        for line in f:
            line = line.strip()
            if line == '':
                out.write('\n')
                continue
            if line[0] == '#':
                out.write(line)
                out.write('\n')
                continue
                
            line = line.split('\t')
            line[4] = line[4].replace('SO', 'SY')
            line[4] = line[4].replace('SW', 'SY')

            out.write('\t'.join(line))
            out.write('\n')
        out.write('\n')
        
        out.close()

