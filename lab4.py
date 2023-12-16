import os
import pandas as pd
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np


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

def plot_histogram(image, class_label, save_path=None):
        # Считаем изображение с использованием OpenCV
    img = cv2.imread(image)

    # Разделим изображение на каналы B, G, R
    b, g, r = cv2.split(img)

    # Вычислим гистограммы для каждого канала
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])

    # Отрисовываем гистограммы
    plt.figure(figsize=(10, 6))
    plt.title(f'Histogram for Class: {class_label}')
    plt.subplot(3, 1, 1)
    plt.plot(hist_b, color='blue')
    plt.title('Blue Channel Histogram')
    plt.subplot(3, 1, 2)
    plt.plot(hist_g, color='green')
    plt.title('Green Channel Histogram')
    plt.subplot(3, 1, 3)
    plt.plot(hist_r, color='red')
    plt.title('Red Channel Histogram')

    #plt.tight_layout()
    #plt.show()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        # Если путь не указан, отображаем изображение в интерфейсе
        plt.show()

def main():
    directory = os.getcwd()
    source_path = os.path.join(directory, 'dataset')
    df = create_dataframe(source_path)
    df = add_label_column(df)
    df = add_image_size_columns(df)

    # Выбираем случайное изображение
    random_image_row = df.sample(1).iloc[0]
    random_image_path = random_image_row['Absolute Path']
    random_image_class = random_image_row['Class']

    save_path = 'histogram_image.png'
    plot_histogram(random_image_path, random_image_class, save_path)

    # Строим и отрисовываем гистограмму
    save_path_plot = 'output_plot.png'
    df.to_csv('output_dataframe.csv', index=False)
    plt.savefig(save_path_plot)

if __name__ == "__main__":
    main()
    
