import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import MobileNetV2
import json

DATASET_PATH = "data_merged"
MODEL_PATH = "model_phan_loai_bien_bao_1.h5"
LABEL_PATH = "label_mapping.json"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 30
LEARNING_RATE = 0.0002 

# Augmentation 
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2,
    rotation_range=25,          
    width_shift_range=0.2,      
    height_shift_range=0.2,
    shear_range=0.15,           
    zoom_range=0.25,            
    brightness_range=[0.7, 1.3],
    fill_mode='nearest',
    channel_shift_range=20.0    
)

val_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

# Mapping giữa label và index
label_mapping = train_generator.class_indices  
idx_to_label = {str(v): k for k, v in label_mapping.items()}  
with open(LABEL_PATH, "w", encoding="utf-8") as f:
    json.dump(idx_to_label, f, ensure_ascii=False, indent=4)

num_classes = train_generator.num_classes
print(f"\n Classes: {num_classes} | Train: {train_generator.samples} | Val: {val_generator.samples}")

# MobileNetV2 Model với Fine-tuning
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(*IMG_SIZE, 3))

for layer in base_model.layers[:-40]: 
    layer.trainable = False
for layer in base_model.layers[-40:]: # Fine-tune 40 lớp cuối
    layer.trainable = True

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.7),  
    layers.Dense(128, activation="relu"), 
    layers.Dropout(0.6),  
    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Dừng sớm
callbacks = [
    EarlyStopping(
        monitor="val_loss", 
        patience=8,  
        restore_best_weights=True, # khôi phục epochs có weights tốt nhất
        verbose=1
    ),
    ReduceLROnPlateau( # giảm learning rate khi val_loss không cải thiện
        monitor="val_loss", 
        factor=0.5, # giảm learning rate còn một nửa
        patience=4, 
        min_lr=1e-7, 
        verbose=1
    )
]

print("\n Bắt đầu training \n")

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

model.save(MODEL_PATH)
print(f"\n Đã lưu: {MODEL_PATH}")

# Result
print("\n" + "="*60)
val_loss, val_acc = model.evaluate(val_generator, verbose=0)
train_acc = history.history['accuracy'][-1]
gap = train_acc - val_acc

print(f"    KẾT QUẢ CUỐI:")
print(f"    Train Acc: {train_acc*100:.2f}%")
print(f"    Val Acc:   {val_acc*100:.2f}%")
print(f"    Gap:       {gap*100:.2f}%")

if gap < 0.08:
    print("TỐT - Gap nhẹ")
elif gap < 0.15:
    print("ỔN - Gap hơi cao")
else:
    print("OVERFITTING")

print("="*60)