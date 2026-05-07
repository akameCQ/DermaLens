from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models
import tensorflow as tf

class EfficientNetB0Model:
    def __init__(self, classes, dropout=0.3, dense_units=128):
        self.classes = int(classes)
        self.dropout = float(dropout)
        self.dense_units = int(dense_units)
        self.model = self.build_model()
    
    def build_model(self):
        base_model = EfficientNetB0(
            include_top=False,
            weights="imagenet",
            input_shape=(224, 224, 3),
            pooling=None
        )
        base_model.trainable = False
        
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(self.dense_units, activation="relu"),
            layers.Dropout(self.dropout),
            layers.Dense(self.classes, activation="softmax")
        ])
        return model
    
    def compile(self):
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),#0.001  0.0005
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )
    
    def summary(self):
        return self.model.summary()
