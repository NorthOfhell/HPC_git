import os
import numpy as np
data_sets =["global", "shared", "shared_comm"]
data_list = []
for outer_index, data_set in enumerate(data_sets):
    num_lines = sum(1 for _ in os.listdir(data_set))
    data_list.append([np.zeros((num_lines, 3))])
    data_list[outer_index].append([])
    inner_index = 0
    for name in os.listdir(data_set):
        settings = name.strip(data_set).strip(".dat")
        data_list[outer_index][1].append(settings)
        with open(data_set + "//" + name) as f:
            count = 0
            for line in f:
                count +=1

                splitted = line[:-1].split("|-|")
                if len(splitted) > 1:
                    data_list[outer_index][0][inner_index][0] += float(splitted[0])
                    data_list[outer_index][0][inner_index][1] += float(splitted[1])
                    if len(splitted) == 5:
                        data_list[outer_index][0][inner_index][2] += float(splitted[2])

            data_list[outer_index][0][inner_index][0] /= count
            data_list[outer_index][0][inner_index][1] /= count
            if len(splitted) == 5:
                data_list[outer_index][0][inner_index][2] /= count
                

            inner_index += 1
            
for index in range(len(data_list[0][0])):
    if data_list[0][1][index] == data_list[1][1][index]: 
        speedup1 = data_list[0][0][index][0] / data_list[0][0][index][1]
        speedup2 = data_list[1][0][index][0] / data_list[1][0][index][1]
        print(f"{data_list[0][1][index]:<10}: speedup global: {speedup1:<10.3} - speedup shared: {speedup2:<10.3}")
    else:
        print("ERROR")

for index in range(len(data_list[0][0])):
    if data_list[1][1][index] == data_list[2][1][index]: 
        speedup1 = data_list[1][0][index][0] / data_list[1][0][index][1]
        speedup2 = data_list[1][0][index][0]  / (data_list[1][0][index][1] - data_list[2][0][index][2])
        print(f"{data_list[0][1][index]:<10}: speedup with comm: {speedup1:<10.3} - speedup without comm: {speedup2:<10.3}")
    else:
        print("ERROR")