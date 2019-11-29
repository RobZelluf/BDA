import pandas as pd
from time import sleep

cols_to_keep = ["lrscale", "cntry", "cntry", "aesfdrk", "sclmeet", "sclact", "imwbcnt", "lknemny", "yrbrn"]

filename = "data/variables.csv"
metadata = pd.read_csv(filename, index_col="Name")
filename = "data/ESS8e02.1_F1.csv"
data = pd.read_csv(filename)

num_cols = len(list(data))
num_entries = len(data)

columns_to_delete = []
binary_columns = []

scale_types = list(set(metadata["Scale_type"]))
print(scale_types)

formats = list(set(metadata["Format"]))
print(formats)

non_values = [55, 66, 77, 88, 99, 666, 777, 888, 999, 14, 16, 18]
yn_non = [6, 7, 8, 9]
yn_non = [((x + -1) * 4) + 3 for x in yn_non]
non_values.extend(yn_non)


def check_none_answer(data):
    for val in non_values:
        if val in data.values:
            return True


def count_none_answer(data):
    count = 0
    for val in non_values:
        count += len(data[data.values == val])

    return count


def remove_sparse_columns(df):
    print("Filtering sparse columns")

    columns = list(df)
    num_entries = len(df)

    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue
        num_none = count_none_answer(df[i])
        if num_none / num_entries > 0.1:
            count += 1
            del df[i]

    print("Removed", count, "columns")
    return df


def remove_none_answers_rows(df):
    print("Removing none-answers")
    to_remove = []
    count = 0
    for i, j in df.iterrows():
        if check_none_answer(j):
            count += 1
            to_remove.append(i)

    print("Removed", count, "rows")
    return df.drop(df.index[to_remove])


def delete_column(row):
    if row["Scale_type"] == "nominal":
        return True
    if row["Invalid"] > 0.1 * num_entries:
        return True
    if "character" in row["Format"]:
        return True
    if row["Country_specific"] == "yes":
        return True

    return False


def filter_binary(df):
    print("Filtering binary columns")

    columns = list(df)
    count = 0
    del_count = 0
    for i in columns:
        if metadata.loc[i]["Scale_type"] == "binary":
            if len([x for x in df[i] if x == 0]) > 0:
                del df[i]
                del_count += 1
            else:
                df[i] -= 1
                df[i] *= 4
                df[i] += 3
                count += 1

    print("Altered", count, "columns. Deleted", del_count, "columns.")
    return df


def remove_above_ten_columns(df):
    print("Filtering >10 columns")

    columns = list(df)

    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue
        if max(df[i]) > 10:
            count += 1
            del df[i]

    print("Removed", count, "columns")
    return df


for index, row in metadata.iterrows():
    if delete_column(row):
        columns_to_delete.append(index)


for col in columns_to_delete:
    if col in cols_to_keep:
        continue

    del data[col]

data = remove_sparse_columns(data)
data = remove_above_ten_columns(data)
data = filter_binary(data)
data = remove_none_answers_rows(data)


print("Reduced from", num_cols, "to", len(list(data)), "columns and", num_entries, "to", len(data), "rows")

data = data.reindex(sorted(data.columns), axis=1)
data.to_csv("data/filtered_data2.csv", index=False)