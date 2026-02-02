import os
import cv2
import numpy as np


def process_images(original_dir, result_dir, target_dir):
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    images = [os.path.join(original_dir, f) for f in os.listdir(original_dir) if f.endswith(('.jpg', '.png'))]

    for path in images:
        img = cv2.imread(path)
        if img is None:
            print(f"Error loading image: {path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (256, 256))

        name = os.path.splitext(os.path.basename(path))[0]
        result_path = os.path.join(result_dir, f"{name}.npy")
        data = small.reshape((1, 256, 256))
        np.save(result_path, data)

        target_small = cv2.resize(gray, (256, 256))
        target_data = target_small.reshape((1, 256, 256))
        target_path = os.path.join(target_dir, f"{name}.npy")
        np.save(target_path, target_data)

        print(f"Processed: {name}")


original_dir = r'F:\pywork119\pythonProject\segmentation\PART1/raw_train_photos'
result_dir = 'test1'
target_dir = 'label1'

process_images(original_dir, result_dir, target_dir)