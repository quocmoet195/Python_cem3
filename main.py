
import shutil
from bs4 import BeautifulSoup
import requests
import os
import csv


URL = "https://yandex.ru/images/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

def get_image(image_url, name, index):
    if not os.path.isdir(name):
        os.mkdir(name)
    picture = requests.get(f"https:{image_url}", HEADERS)
    saver = open(os.path.join(f"{name}/{str(index).zfill(4)}.jpg"), "wb")
    saver.write(picture.content)
    saver.close()

def download_img(path, key):
    os.chdir(path)
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
    os.chdir("dataset")
    
    count = 0
    page = 0
    
    while count < 1000:
        key1=key.replace(" ", "%20")
        url = f'{URL}search?p={page}&text={key}'
        print(f"Fetching URL: {url}")
        
        response = requests.get(url, headers=HEADERS)
        response =response.text
        soup = BeautifulSoup(response, "lxml")
        images = soup.findAll('img', class_='serp-item__thumb justifier__thumb')
        if not images:
            print("No images found on this page.")
            break

        for image in images:
            if count == 1020:
                return
            image_url = image.get("src")
            if image_url and not image_url.startswith("data:"):
                get_image(image_url, key, count)
                count += 1
        print(count)
        page += 1



def create_annotation_file(dataset_path, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([f"      Absolute Path                 Relative Path      Class"])

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                class_name = root.split(os.path.sep)[-1]
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, dataset_path)
                csv_row = [f"{absolute_path}    {relative_path}    {class_name}"]
                csv_writer.writerow(csv_row)



def copy_dataset_with_modified_filenames(dataset_path):
    output_path = 'modified_dataset'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            class_name = root.split(os.path.sep)[-1]
            new_filename = f"{class_name}_{file}"
            source_file = os.path.join(root, file)
            destination_file = os.path.join(output_path, new_filename)
            shutil.copy(source_file, destination_file)





def main():
    directory = os.getcwd()
    #download_img(directory, 'brown bear')
    #download_img(directory, 'polar bear')
    create_annotation_file('dataset', 'annotation.csv')
    copy_dataset_with_modified_filenames('dataset')


if __name__ == "__main__":
    main()