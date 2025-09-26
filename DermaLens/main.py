from data_loader import data_pre
from flow import EfficientNetB0Model
import tensorflow as tf


def main():
    train_ds, val_ds, class_names = data_pre()

    my_model = EfficientNetB0Model(classes=len(class_names))
    my_model.compile()
    my_model.summary()
    
    
    early_stop_cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",        
        patience=10,                
        restore_best_weights=True  
    )
    
    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
        filepath="checkpoints/dermalens_best_2.h5",   
        save_best_only=True,                       
        monitor="val_loss",                       
        mode="min",                                
        
    )
    #my_model.model.load_weights("checkpoints/dermalens_best.h5")

    history = my_model.model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20,   
        #initial_epoch=2,                
        class_weight=classes(class_names),
        callbacks=[checkpoint_cb, early_stop_cb],
        verbose=1
    )
    
    try:
        my_model.model.save_weights("backup_weights2.h5")   
    except:
        print("backup_weights2.h5 kaydetme başarısız")
    
    try:
        my_model.model.save("dermalens_model.keras")
    except:
        print("dermalens_model.keras kaydetme başarısız")
        
    
    #my_model.model.load_weights("backup_weights.h5")
    #print("Ağırlıklar yüklendi!")
    #preds = my_model.model.predict(val_ds.take(1))
    #print(preds)
    #my_model.model.save("dermalens_model2.keras")
    #print("Model kaydedildi: dermalens_model2")
    

def classes(class_names):
    counts = {
        "akiec": 6942,
        "bcc": 6940,
        "bkl": 6958,
        "df": 6982,
        "mel": 6972,
        "nv": 6957,
        "vasc": 6946
    }
    class_weight = {}
    total = float(sum(counts.values()))    
    num_classes = float(len(counts))       
    
    for idx, clss in enumerate(class_names):
        c = float(counts[clss])          
        weight = total / (num_classes * c)
        class_weight[int(idx)] = float(weight)   
    
    return class_weight

if __name__ == "__main__":
    main()
