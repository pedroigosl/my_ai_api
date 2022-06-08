import numpy as np
file = open('labelmap.txt')
category_index = {}
for i, val in enumerate(file):
    if i == 0:
        val = val[:-1]
        blank = np.copy(val)
        print(blank)
    else:
        val = val[:-1]
        if val != blank:
            category_index.update({(i-1): {'id': (i-1), 'name': val}})
    # print(i, val)

file.close()
print(category_index)


# =============================================================================
