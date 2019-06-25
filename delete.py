import sys
import os

latest = int(sys.argv[1])

for date in range(0, latest):
    for l in ('pos', 'neg'):
        path ='aclImdb/%s/%s' % (s, l)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r', encoding="utf8") as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]], ignore_index=True)
            pbar.update()