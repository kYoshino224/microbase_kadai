def split_region(word_list, line_list):
    for i in range(word_list.shape[0]):
        for j, line in enumerate(line_list):
            x = word_list.loc[i, "x"]
            y = word_list.loc[i, "y"]
            if y >= line.y(x):
                word_list.loc[i, "region"] = word_list.loc[i, "region"] + 2**j
    return word_list
