import pandas as pd
import os
import shutil
import cv2
import numpy as np
import itertools


def data():
    df = pd.read_csv("D:\\indirilenler\\h\\HAM10000_metadata.csv")

    for i, row in df.iterrows():
        img_id = row["image_id"]+ ".jpg"
        label = row["dx"]
        
        source = os.path.join("D:\\indirilenler\\h\\archive\\HAM10000_images_part_1",img_id)
        if not os.path.exists(source):
            source = os.path.join("D:\\indirilenler\\h\\archive\\HAM10000_images_part_2",img_id)
          
        print(source)
        
        target_dir = os.path.join("Dataset", label)
        os.makedirs(target_dir, exist_ok=True)

        data_set = os.path.join("Dataset",label,img_id) 
        shutil.copy(source, data_set)
        
        image_raw = cv2.imread(data_set)
        image_raw = cv2.resize(image_raw,(224,224))
        image_rgb = cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB)
        cv2.imwrite(data_set, image_rgb)
        
        
def data_increas(path, target_count=7000):
    imagelist = [f for f in os.listdir(path) if f.lower().endswith(".jpg")]
    image_count = len(imagelist)
    totalcount = (target_count - image_count) // 63
    count = 0

    while count < totalcount and image_count < target_count:
        img_path = os.path.join(path, imagelist[count % len(imagelist)])
        image = cv2.imread(img_path)

        variants = generate_unique_variants(image)

        for idx, variant in enumerate(variants):
            image_name = os.path.join(path, f"imageVariant_{image_count}_{idx}.jpg")
            #cv2.imwrite(image_name, cv2.cvtColor(variant, cv2.COLOR_BGR2RGB))
            cv2.imwrite(image_name, variant)
            image_count += 1

            if image_count >= target_count:
                break
            elif count >= totalcount:
                break
            
        count += 1
    return image_count
        
def augment_image(image, operations):
    img = image.copy()
    for op in operations:
        if op == "flip":
            img = cv2.flip(img, 1)
        elif op == "rotate":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif op == "brightness":
            img = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
        elif op == "gamma":
            gamma = 1.5
            lookUpTable = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)], dtype=np.uint8)
            img = cv2.LUT(img, lookUpTable)
        elif op == "blur":
            img = cv2.GaussianBlur(img, (5,5), 0)
        elif op == "skin":
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (0,0,0), (180,255,50))
            hsv[mask>0] = (10,150,200)
            img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def generate_unique_variants(image):
    operations = ["flip","rotate","brightness","gamma","blur","skin"]
    variants = []
    
    for r in range(1, len(operations)+1):
        combos = itertools.combinations(operations, r)
        for ops in combos:
            variants.append(augment_image(image, ops))
    return variants

if __name__ =="__main__":
    akiec = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\akiec")
    bcc = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\bcc")
    bkl = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\bkl")
    df = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\df")
    mel = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\mel")
    nv = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\nv")
    vasc = data_increas("D:\\final proje pyton\\DermaLens\\Dataset\\vasc")
    
    
    
    
    