import pandas as pd
from time import sleep


cols_to_keep = ["lrscale", "cntry", "cntry", "aesfdrk", "sclmeet", "sclact", "imwbcnt", "lknemny", "yrbrn"]
five_scale_columns = []

non_values = [55, 66, 77, 88, 99, 666, 777, 888, 999, 14, 16, 18]

yn_non = [6, 7, 8, 9]
yn_non = [((x + -1) * 4) + 3 for x in yn_non]
non_values.extend(yn_non)


def check_if_nominal(data):
    nom_values = [6666, 7777, 8888, 9999, 66666, 77777, 88888, 99999, 555555, 11010, 55]
    for val in nom_values:
        if val in data.values:
            return True

    return False


def check_none_answer(data):
    for val in non_values:
        if val in data.values:
            return True


def count_none_answer(data):
    count = 0
    for val in non_values:
        count += len(data[data.values == val])

    return count


def remove_text_columns(df):
    print("Filtering text columns")

    columns = list(df)

    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue
        if not pd.to_numeric(df[i], errors='coerce').notnull().all():
            count += 1
            del df[i]

    print("Removed", count, "columns")
    return df


def remove_nominal_columns(df):
    print("Filtering nominal columns")

    columns = list(df)

    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue

        if check_if_nominal(df[i]):
            count += 1
            del df[i]
            continue

        if max(df[i]) <= 2:
            count += 1
            del df[i]

    print("Removed", count, "columns")
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


def filter_five_scale(df):
    print("Filtering 5-scale columns")

    columns = list(df)
    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue

        if len([x for x in df[i] if x == 6]) == 0 and max(df[i]) < 10:
            df[i] *= 2
            five_scale_columns.append(i)
            count += 1

    print("Altered", count, "columns")
    return df


def filter_yes_no(df):
    print("Filtering yes-no columns")

    columns = list(df)
    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue

        if len([x for x in df[i] if x in [3, 4, 5]]) == 0:
            df[i] -= 1
            df[i] *= 4
            df[i] += 3
            count += 1

    print("Altered", count, "columns")
    return df


def remove_nonfull_columns(df):
    print("Filtering non-full columns")

    columns = list(df)
    num_entries = len(df)

    count = 0
    for i in columns:
        if i in cols_to_keep:
            continue
        num_empty = df[i].isna().sum()
        if num_empty / num_entries > 0:
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


filename = "data/ESS8e02.1_F1.csv"
df = pd.read_csv(filename)

num_cols = len(list(df))
num_entries = len(df)


print("Number of columns", len(list(df)), "and rows", len(df))
df = remove_text_columns(df)
print("---")
df = remove_nonfull_columns(df)
print("---")
df = remove_nominal_columns(df)
print("---")
df = remove_above_ten_columns(df)
print("---")
df = filter_yes_no(df)
print("---")
df = filter_five_scale(df)
print("---")
df = remove_sparse_columns(df)
print("---")
df = remove_none_answers_rows(df)
print("---")

print("Number of columns", len(list(df)), "and rows", len(df))
print("Reduced from", num_cols, "to", len(list(df)), "columns and", num_entries, "to", len(df), "rows")

df = df.reindex(sorted(df.columns), axis=1)
df.to_csv("data/filtered_data.csv", index=False)