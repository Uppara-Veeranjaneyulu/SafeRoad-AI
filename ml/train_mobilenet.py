import os
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

try:
    from ml.preprocessing import get_or_create_splits, compute_train_class_weights, build_dataset, CLASS_NAMES
except ImportError:
    from preprocessing import get_or_create_splits, compute_train_class_weights, build_dataset, CLASS_NAMES

def build_mobilenetv2_model(input_shape=(224, 224, 3), num_classes=3, dropout_rate=0.3, dense_units=128):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Initially freeze backbone

    inputs = layers.Input(shape=input_shape)
    # Convert [0, 1] to [-1, 1] as expected by MobileNetV2
    x = (inputs * 2.0) - 1.0
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D(name='gap')(x)
    x = layers.Dense(dense_units, activation='relu', name='dense_feature')(x)
    x = layers.Dropout(dropout_rate, name='dropout')(x)
    outputs = layers.Dense(num_classes, activation='softmax', name='output')(x)

    model = models.Model(inputs, outputs, name='MobileNetV2_Classifier')
    return model, base_model

def train_and_evaluate_mobilenet(head_epochs=6, finetune_epochs=6, batch_size=32):
    os.makedirs('trained_models', exist_ok=True)
    os.makedirs('results/mobilenetv2', exist_ok=True)

    splits = get_or_create_splits()
    train_samples = splits['train']
    val_samples = splits['val']
    test_samples = splits['test']
    
    class_weights = compute_train_class_weights(train_samples)

    train_ds = build_dataset(train_samples, batch_size=batch_size, is_training=True)
    val_ds = build_dataset(val_samples, batch_size=batch_size, is_training=False)
    test_ds = build_dataset(test_samples, batch_size=batch_size, is_training=False)

    test_labels = [s['label'] for s in test_samples]

    model, base_model = build_mobilenetv2_model()
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model_path = 'trained_models/mobilenetv2_best.keras'
    cb_list = [
        callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True, verbose=1),
        callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=1),
        callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)
    ]

    print("\n[Training MobileNetV2] Phase 1: Training Classification Head...")
    start_time = time.time()
    hist_head = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=head_epochs,
        class_weight=class_weights,
        callbacks=cb_list,
        verbose=1
    )

    print("\n[Training MobileNetV2] Phase 2: Fine-tuning Upper Layers...")
    base_model.trainable = True
    # Freeze all layers except top 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    hist_fine = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=finetune_epochs,
        class_weight=class_weights,
        callbacks=cb_list,
        verbose=1
    )
    total_training_time = time.time() - start_time

    # Combine history
    combined_history = {
        'accuracy': hist_head.history['accuracy'] + hist_fine.history['accuracy'],
        'val_accuracy': hist_head.history['val_accuracy'] + hist_fine.history['val_accuracy'],
        'loss': hist_head.history['loss'] + hist_fine.history['loss'],
        'val_loss': hist_head.history['val_loss'] + hist_fine.history['val_loss'],
        'training_time_seconds': total_training_time,
        'epochs_trained': len(hist_head.history['loss']) + len(hist_fine.history['loss'])
    }

    with open('results/mobilenetv2/history.json', 'w') as f:
        json.dump(combined_history, f, indent=2)

    # Plot curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    epochs = range(1, len(combined_history['loss']) + 1)
    ax1.plot(epochs, [a * 100 for a in combined_history['accuracy']], 'b-', label='Train Accuracy')
    ax1.plot(epochs, [a * 100 for a in combined_history['val_accuracy']], 'r-', label='Val Accuracy')
    ax1.set_title('MobileNetV2 - Accuracy Curves')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(epochs, combined_history['loss'], 'b-', label='Train Loss')
    ax2.plot(epochs, combined_history['val_loss'], 'r-', label='Val Loss')
    ax2.set_title('MobileNetV2 - Loss Curves')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('results/mobilenetv2/training_curves.png', dpi=300)
    plt.close()

    # Unseen Test Set Evaluation
    best_model = tf.keras.models.load_model(model_path)
    print("\n[Evaluation] Evaluating MobileNetV2 on unseen test set...")
    t0 = time.time()
    test_preds_proba = best_model.predict(test_ds, verbose=1)
    avg_inference_ms = ((time.time() - t0) / len(test_samples)) * 1000.0

    test_preds = np.argmax(test_preds_proba, axis=1)

    prec, rec, f1, support = precision_recall_fscore_support(test_labels, test_preds, average=None, zero_division=0)
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(test_labels, test_preds, average='macro', zero_division=0)
    acc = np.mean(np.array(test_labels) == test_preds)
    cm = confusion_matrix(test_labels, test_preds)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title('MobileNetV2 - Confusion Matrix (Test Set)')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig('results/mobilenetv2/confusion_matrix.png', dpi=300)
    plt.close()

    report_str = classification_report(test_labels, test_preds, target_names=CLASS_NAMES, digits=4, zero_division=0)
    with open('results/mobilenetv2/classification_report.txt', 'w') as f:
        f.write(report_str)

    results = {
        'model': 'MobileNetV2',
        'accuracy': float(acc),
        'accuracy_percent': float(acc * 100.0),
        'precision': float(macro_p),
        'recall': float(macro_r),
        'f1_score': float(macro_f1),
        'macro_f1': float(macro_f1),
        'high_risk_recall': float(rec[2]),
        'per_class': {
            CLASS_NAMES[i]: {
                'precision': float(prec[i]),
                'recall': float(rec[i]),
                'f1_score': float(f1[i]),
                'support': int(support[i])
            } for i in range(len(CLASS_NAMES))
        },
        'confusion_matrix': cm.tolist(),
        'inference_time_ms': float(avg_inference_ms),
        'training_time_seconds': float(total_training_time),
        'total_parameters': int(best_model.count_params())
    }

    with open('results/mobilenetv2/test_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*50)
    print("MOBILENETV2 TEST RESULTS:")
    print(f"Accuracy:        {acc * 100:.2f}%")
    print(f"Macro-F1:        {macro_f1:.4f}")
    print(f"High-Risk Recall:{rec[2]:.4f}")
    print(f"Inference Time:  {avg_inference_ms:.2f} ms/image")
    print("="*50)
    return results

if __name__ == '__main__':
    train_and_evaluate_mobilenet()
