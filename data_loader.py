import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

from tensorflow.keras.layers import Rescaling

def data_pre():
    dataset_dir = "Dataset"
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(224, 224),
        batch_size=16
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(224, 224),
        batch_size=16
    )
    
    class_names = train_ds.class_names
    
    normalization_layer = Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
    val_ds = val_ds.map(lambda x, y: (preprocess_input(x), y))

    # Daha hızlı eğitim
    train_ds = train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_ds, val_ds, class_names
