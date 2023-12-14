import os
import pandas as pd
from PIL import Image


def create_dataframe(dataset_path):
    data = {'Absolute Path': [], 'Relative Path': [], 'Class': []}

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            class_name = root.split(os.path.sep)[-1]
            absolute_path = os.path.join(root, file)
            relative_path = os.path.relpath(absolute_path, dataset_path)
            data['Absolute Path'].append(absolute_path)
            data['Relative Path'].append(relative_path)
            data['Class'].append(class_name)

    df = pd.DataFrame(data)
    return df

def add_label_column(df):
    df['Label'] = df['Class'].astype('category').cat.codes
    return df

def add_image_size_columns(df):
    df['Height'] = [Image.open(path).height for path in df['Absolute Path']]
    df['Width'] = [Image.open(path).width for path in df['Absolute Path']]
    df['Depth'] = [Image.open(path).layers for path in df['Absolute Path']]
    return df

def compute_statistics(df):
    statistics = df.describe(include='all')
    return statistics

def filter_by_class(df, class_label):
    filtered_df = df[df['Class'] == class_label]
    return filtered_df

def filter_by_size(df, class_label, max_width, max_height):
    filtered_df = df[(df['Class'] == class_label) & (df['Width'] <= max_width) & (df['Height'] <= max_height)]
    return filtered_df

def group_by_class(df):
    df['Pixel Count'] = df['Height'] * df['Width'] * df['Depth']
    grouped_stats = df.groupby('Class')['Pixel Count'].agg(['min', 'max', 'mean'])
    return grouped_stats

def main():
    directory = os.getcwd()
    source_path = os.path.join(directory, 'dataset')
    df = create_dataframe(source_path)
    df = add_label_column(df)
    df = add_image_size_columns(df)

    df.to_csv('output_dataframe.csv', index=False)

    


if __name__ == "__main__":
    main()