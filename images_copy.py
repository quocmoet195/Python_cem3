import os
import csv
import shutil

def get_full_paths2(class_name: str) -> list:
    # """
    # Возвращает список измененных абсолютных путей для изображений

    # Данная функция возвращает список абсолютных путей для всех изображений определенного
    # класса, переданного в функцию, после перемещения изображений в другую директорию
    # Parameters
    #     class_name : str
    #     Имя класса
    # Returns
    #     list
    #     Список абсолютных путей к изображениям
    # """
    full_path = os.path.abspath('dataset2')
    image_names = os.listdir(full_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_full_paths = list(
        map(lambda name: os.path.join(full_path, name), image_class_names))
    return image_full_paths

def get_relative_paths2(class_name: str) -> list:
    # """
    # Возвращает список измененных относительных путей для изображений

    # Данная функция возвращает список относительных путей для всех изображений определенного класса, 
    # переданного в функцию, после перемещения изображений в другую директорию
    # Parameters
    #     class_name : str
    #     Имя класса
    # Returns
    #     list
    #     Список относительных путей к изображениям
    # """
    rel_path = os.path.abspath('dataset2')
    image_names = os.listdir(rel_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_rel_paths = list(
        map(lambda name: os.path.join(rel_path, name), image_class_names))
    return image_rel_paths

def replace_images(class_name: str) -> list:
    # """
    # Изменяет имена изображений и переносит их в другую директорию

    # Данная функция изменяет имена изображений, объединяя номер изображения и класс в формате class_number.jpg, 
    # переносит изображения в директорию dataset и удаляет папку, где хранились изображения класса

    # Parameters
    #     class_name : str
    #     Имя класса
    # Returns
    #     None
    # """
    rel_path = os.path.relpath('dataset2')
    class_path = os.path.join(rel_path, class_name)
    image_names = os.listdir(class_path)
    image_rel_paths = list(
        map(lambda name: os.path.join(class_path, name), image_names))
    new_rel_paths = list(
        map(lambda name: os.path.join(rel_path, f'{class_name}_{name}'), image_names))
    for old_name, new_name in zip(image_rel_paths, new_rel_paths):
        os.replace(old_name, new_name)

    os.chdir('dataset2')

    if os.path.isdir(class_name):
        os.rmdir(class_name)

    os.chdir('..')


def create_dataset2():
    class_brown_bear="cat"
    class_polar_bear="dog"
    
    if os.path.isdir('dataset2'):
        shutil.rmtree('dataset2')

    old = os.path.relpath('dataset')
    new = os.path.relpath('dataset2')
    shutil.copytree(old, new)
    
    replace_images(class_brown_bear)
    replace_images(class_polar_bear)
    
def create_annotation2():
    class_brown_bear="cat"
    class_polar_bear="dog"
    
    cat_full_paths = get_full_paths2(class_brown_bear)
    cat_rel_paths = get_relative_paths2(class_brown_bear)
    dog_full_paths = get_full_paths2(class_polar_bear)
    dog_rel_paths = get_relative_paths2(class_polar_bear)
    
    with open('paths2.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
        for full_path, rel_path in zip(cat_full_paths, cat_rel_paths):
            writer.writerow([full_path, rel_path, class_brown_bear])
        for full_path, rel_path in zip(dog_full_paths, dog_rel_paths):
            writer.writerow([full_path, rel_path, class_polar_bear])

# if __name__ == "__main__":
#     main()