from tensorflow import keras
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
import cv2

class Get_Result():
    def __init__(self):
        self.model = None
        self.pred = None
        self.class_names = None
        
    def model_load(self):
        self.model = keras.models.load_model("checkpoints/dermalens_best_2.h5")
        self.class_names = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]
        
    def get_image_pre(self, image_dir):
        img = cv2.imread(image_dir)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        
        cv2.imwrite("Base.png", img)
        
        return self.get_image("Base.png")
        
    def get_image(self, image_dir):
        img = cv2.imread(image_dir)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        
        cv2.imwrite(image_dir, img)
        img_array = np.expand_dims(img, axis=0).astype(np.float32)

        img_array = preprocess_input(img_array)

        self.pred = self.model.predict(img_array)
        return self.get_results()
    
    def get_results(self):
        probs = self.pred[0]
        print("\n... Tahmin Olasılıkları ...")
        for i, cls in enumerate(self.class_names):
            print(f"{cls}: {probs[i]*100:.2f}%")
        
        predicted_class = np.argmax(self.pred, axis=1)[0]
        print(f"\nTahmin edilen sınıf: {self.class_names[predicted_class]} "
        f"({probs[predicted_class]*100:.2f}%)")
        return self.class_names[predicted_class]
        
"""
if __name__ == "__main__":
    gr = Get_Result()
    gr.model_load()
    gr.get_image_pre("test/azra.png")
    gr.get_results()
"""