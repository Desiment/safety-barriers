import csv

file = open('precedents.csv', 'r')
objs = file.read().replace('\n', '').lower().split('#')
with open('fixed_precedents.csv', 'w') as out:
    out.write("subsidiary,contractor,worktype,place,description\n")
    i = 4
    while i < len(objs):
        if len(objs[i]) == 0:
            i += 1
            continue
        open = False
        res = []
        ic = 0
        while ic < len(objs[i]):
            if objs[i][ic] == '\'':
                open = not open
                if open:
                    res.append('')
            elif objs[i][ic] == '\\':
                ic += 1
            elif open:
                res[-1] += objs[i][ic]
            ic += 1
        i += 2
        res.append("")
        ic = 0
        while ic < len(objs[i]):
            if objs[i][ic] == '\\':
                ic += 1
            else:
                res[-1] += objs[i][ic]
            ic += 1
        for j in range(len(res)):
            out.write(res[j])
            if j != len(res) - 1:
                out.write(',')
            else:
                out.write('\n')
        i += 1

file.close()
