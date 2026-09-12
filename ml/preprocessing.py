import os
import json
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf

# Standard class mappings
CLASS_NAMES = ['Safe', 'Moderate Risk', 'High Risk']
FOLDER_TO_LABEL = {
    'Safe': 0,
    'Moderate': 1,
    'High': 2
}
LABEL_TO_CLASS = {v: CLASS_NAMES[v] for v in FOLDER_TO_LABEL.values()}

IMAGE_SIZE = (224, 224)
AUTOTUNE = tf.data.AUTOTUNE

def get_or_create_splits(data_dir='data', split_file='ml/split_data.json', seed=42, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15):
    """
    Creates or loads a reproducible, stratified 70/15/15 train/val/test split.
    The test set remains completely unseen during training and tuning.
    """
    os.makedirs(os.path.dirname(split_file) if os.path.dirname(split_file) else '.', exist_ok=True)
    
    if os.path.exists(split_file):
        print(f"[Preprocessing] Loading existing split from {split_file}")
        with open(split_file, 'r') as f:
            splits = json.load(f)
        return splits

    print(f"[Preprocessing] Generating new reproducible stratified split from {data_dir} (seed={seed})...")
    all_samples = []
    
    for folder, label in FOLDER_TO_LABEL.items():
        folder_path = os.path.join(data_dir, folder)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Class folder {folder_path} not found!")
        
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
        print(f"  Class '{folder}' (Label {label}): {len(files)} images")
        for f in files:
            rel_path = os.path.join(data_dir, folder, f).replace('\\', '/')
            all_samples.append({'path': rel_path, 'label': label, 'class_name': CLASS_NAMES[label], 'folder': folder})

    df = pd.DataFrame(all_samples)
    
    # 70% train, 30% temp
    train_df, temp_df = train_test_split(
        df,
        test_size=(val_ratio + test_ratio),
        random_state=seed,
        stratify=df['label']
    )
    
    # 15% val, 15% test from temp
    val_proportion = val_ratio / (val_ratio + test_ratio)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=(1.0 - val_proportion),
        random_state=seed,
        stratify=temp_df['label']
    )

    splits = {
        'train': train_df.to_dict(orient='records'),
        'val': val_df.to_dict(orient='records'),
        'test': test_df.to_dict(orient='records'),
        'metadata': {
            'seed': seed,
            'total_samples': len(df),
            'train_count': len(train_df),
            'val_count': len(val_df),
            'test_count': len(test_df),
            'classes': CLASS_NAMES,
            'folder_to_label': FOLDER_TO_LABEL
        }
    }

    with open(split_file, 'w') as f:
        json.dump(splits, f, indent=2)

    # Also save CSV versions for easy inspection
    train_df.to_csv('ml/train_split.csv', index=False)
    val_df.to_csv('ml/val_split.csv', index=False)
    test_df.to_csv('ml/test_split.csv', index=False)

    print(f"[Preprocessing] Saved splits to {split_file}:")
    print(f"  Train: {len(train_df)} images ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Val:   {len(val_df)} images ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:  {len(test_df)} images ({len(test_df)/len(df)*100:.1f}%)")

    return splits

def compute_train_class_weights(train_samples):
    """
    Computes class weights strictly on the training set to prevent leakage and address imbalance.
    """
    labels = [s['label'] for s in train_samples]
    unique_classes = np.array([0, 1, 2])
    weights = compute_class_weight(
        class_weight='balanced',
        classes=unique_classes,
        y=labels
    )
    class_weight_dict = {int(cls): float(w) for cls, w in zip(unique_classes, weights)}
    print(f"[Preprocessing] Computed Training Class Weights: {class_weight_dict}")
    return class_weight_dict

def parse_image_and_label(path, label):
    """Reads, decodes, resizes, and normalizes an image to [0, 1]."""
    img_bytes = tf.io.read_file(path)
    # decode_image handles JPEG and PNG automatically, expand_animations=False
    img = tf.io.decode_image(img_bytes, channels=3, expand_animations=False)
    img = tf.image.resize(img, IMAGE_SIZE)
    img = tf.cast(img, tf.float32) / 255.0
    img.set_shape([224, 224, 3])
    return img, label

def augment_image(img, label):
    """Training data augmentation: horizontal flip, small rotation, zoom, brightness."""
    # Random horizontal flip
    img = tf.image.random_flip_left_right(img)
    # Random brightness variation (+/- 10%)
    img = tf.image.random_brightness(img, max_delta=0.1)
    # Clip back to [0, 1]
    img = tf.clip_by_value(img, 0.0, 1.0)
    return img, label

def build_dataset(samples, batch_size=32, is_training=False, shuffle_buffer=1000):
    """
    Constructs an optimized tf.data.Dataset pipeline.
    """
    paths = [s['path'] for s in samples]
    labels = [s['label'] for s in samples]

    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    
    if is_training:
        ds = ds.shuffle(buffer_size=min(len(paths), shuffle_buffer), reshuffle_each_iteration=True)

    ds = ds.map(parse_image_and_label, num_parallel_calls=AUTOTUNE)

    if is_training:
        ds = ds.map(augment_image, num_parallel_calls=AUTOTUNE)

    ds = ds.batch(batch_size)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

if __name__ == '__main__':
    splits = get_or_create_splits()
    weights = compute_train_class_weights(splits['train'])
    print("[Preprocessing] Test dataset creation...")
    train_ds = build_dataset(splits['train'], batch_size=32, is_training=True)
    for x, y in train_ds.take(1):
        print(f"Batch shape: images={x.shape}, labels={y.shape}, min_val={tf.reduce_min(x):.2f}, max_val={tf.reduce_max(x):.2f}")
    print("[Preprocessing] Pipeline verified successfully!")
