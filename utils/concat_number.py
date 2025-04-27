import pandas as pd

def concat_number(ocred_list):
    input_list = ocred_list
    try_to_float_stack = []
    remove_stack = []
    for i in range(input_list.shape[0]):
        try:
            float(input_list.loc[i, "word"])
            try_to_float_stack.append(i)
            remove_stack.append(input_list.loc[i, "word"])
        except (TypeError, ValueError):
            if try_to_float_stack != []:
                figure = ""
                x, y = 0, 0
                for index in try_to_float_stack:
                    figure = figure + input_list.loc[index, "word"]
                    x += input_list.loc[index, "x"]
                    y += input_list.loc[index, "y"]
                x = int(x / len(try_to_float_stack))
                y = int(y / len(try_to_float_stack))
                input_list.loc[i-1, :] = pd.Series({"word":figure, "x":x, "y":y, "region":0})
                if figure in remove_stack:
                    remove_stack.remove(figure)
                try_to_float_stack = []
    input_list = input_list[~input_list["word"].isin(remove_stack)]
    input_list = input_list.reset_index(drop=True)
    return input_list