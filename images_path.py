import os
import csv

from typing import List 

def get_full_paths(class_name: str)->List[str]:
    """
    Возвращает список абсолютных путей для изображений

    Данная функция возвращает список абсолютных путей для всех изображений определенного
    класса, переданного в функцию
    Parameters
        class_name : str
        Имя класса
    Returns
        list
        Список абсолютных путей к изображениям
    """
    dataset_dir = 'dataset'
    full_path = os.path.abspath(dataset_dir)
    class_path = os.path.join(full_path, class_name)
    image_names = os.listdir(class_path)
    image_full_paths = [os.path.join(class_path, name) for name in image_names]
    return image_full_paths

def get_relative_paths(class_name: str)->List[str]:
    # """
    # Возвращает список относительных путей путей для изображений

    # Данная функция возвращает список относительных путей относительно файла dataset для 
    # всех изображений определенного класса, переданного в функцию
    # Parameters
    #     class_name : str
    #     Имя класса
    # Returns
    #     list
    #     Список относительных путей к изображениям
    # """
    dataset_dir = 'dataset'
    rel_path = os.path.relpath(dataset_dir)
    class_path = os.path.join(rel_path, class_name)
    image_names = os.listdir(class_path)
    image_rel_paths = [os.path.join(class_path, name) for name in image_names]
    return image_rel_paths

def create_annotation():
    class_brown_bear="brown_bear"
    class_polar_bear="polar_bear"
    
    brown_bear_full_paths = get_full_paths(class_brown_bear)
    brown_bear_rel_paths = get_relative_paths(class_brown_bear)
    polar_bear_full_paths = get_full_paths(class_polar_bear)
    polar_bear_rel_paths = get_relative_paths(class_polar_bear)
    
    with open('paths.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
        for full_path, rel_path in zip(brown_bear_full_paths, brown_bear_rel_paths):
            writer.writerow([full_path, rel_path, class_brown_bear])
        for full_path, rel_path in zip(polar_bear_full_paths, polar_bear_rel_paths):
            writer.writerow([full_path, rel_path, class_polar_bear])

# if __name__ == "__main__":
#     main()