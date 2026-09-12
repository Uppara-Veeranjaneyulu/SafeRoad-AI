import os
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, f1_score
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers

from preprocessing import get_or_create_splits, compute_train_class_weights, build_dataset, CLASS_NAMES

def build_custom_cnn(input_shape=(224, 224, 3), num_classes=3, dropout_rate=0.4, dense_units=128):
    """
    Constructs the exact Custom CNN specified in requirements:
    Conv2D 32 -> MaxPool -> Conv2D 64 -> MaxPool -> Conv2D 128 -> MaxPool -> Conv2D 256 -> GAP -> Dense 128 + ReLU -> Dropout -> Dense 3 + Softmax
    """
    model = models.Sequential([
        layers.Input(shape=input_shape),
        
        layers.Conv2D(32, (3, 3), padding='same', activation='relu', name='conv1'),
        layers.MaxPooling2D((2, 2), name='pool1'),
        
        layers.Conv2D(64, (3, 3), padding='same', activation='relu', name='conv2'),
        layers.MaxPooling2D((2, 2), name='pool2'),
        
        layers.Conv2D(128, (3, 3), padding='same', activation='relu', name='conv3'),
        layers.MaxPooling2D((2, 2), name='pool3'),
        
        layers.Conv2D(256, (3, 3), padding='same', activation='relu', name='conv4'),
        
        layers.GlobalAveragePooling2D(name='gap'),
        
        layers.Dense(dense_units, activation='relu', name='dense_feature'),
        layers.Dropout(dropout_rate, name='dropout'),
        layers.Dense(num_classes, activation='softmax', name='output')
    ], name='Custom_CNN')
    
    return model

class MacroF1ValCallback(callbacks.Callback):
    """Computes and logs validation Macro-F1 at the end of each epoch."""
    def __init__(self, val_dataset, val_labels):
        super().__init__()
        self.val_dataset = val_dataset
        self.val_labels = np.array(val_labels)
        self.macro_f1_history = []

    def on_epoch_end(self, epoch, logs=None):
        preds = self.model.predict(self.val_dataset, verbose=0)
        pred_classes = np.argmax(preds, axis=1)
        macro_f1 = f1_score(self.val_labels, pred_classes, average='macro', zero_division=0)
        self.macro_f1_history.append(float(macro_f1))
        if logs is not None:
            logs['val_macro_f1'] = macro_f1
        print(f" - val_macro_f1: {macro_f1:.4f}")

def plot_and_save_curves(history, out_path, model_name='Custom CNN'):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    epochs = range(1, len(history['loss']) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Accuracy
    ax1.plot(epochs, [a * 100 for a in history.get('accuracy', [])], 'b-', label='Train Accuracy')
    ax1.plot(epochs, [a * 100 for a in history.get('val_accuracy', [])], 'r-', label='Val Accuracy')
    ax1.set_title(f'{model_name} - Accuracy Curves')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Loss
    ax2.plot(epochs, history.get('loss', []), 'b-', label='Train Loss')
    ax2.plot(epochs, history.get('val_loss', []), 'r-', label='Val Loss')
    ax2.set_title(f'{model_name} - Loss Curves')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Training] Saved curves to {out_path}")

def plot_confusion_matrix(cm, out_path, model_name='Custom CNN'):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title(f'{model_name} - Confusion Matrix (Test Set)')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Evaluation] Saved confusion matrix to {out_path}")

def train_and_evaluate_cnn(epochs=30, batch_size=32, lr=0.001):
    os.makedirs('trained_models', exist_ok=True)
    os.makedirs('results/cnn', exist_ok=True)

    splits = get_or_create_splits()
    train_samples = splits['train']
    val_samples = splits['val']
    test_samples = splits['test']
    
    class_weights = compute_train_class_weights(train_samples)

    train_ds = build_dataset(train_samples, batch_size=batch_size, is_training=True)
    val_ds = build_dataset(val_samples, batch_size=batch_size, is_training=False)
    test_ds = build_dataset(test_samples, batch_size=batch_size, is_training=False)

    val_labels = [s['label'] for s in val_samples]
    test_labels = [s['label'] for s in test_samples]

    model = build_custom_cnn()
    model.summary()

    model.compile(
        optimizer=optimizers.Adam(learning_rate=lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model_path = 'trained_models/cnn_best.keras'
    f1_cb = MacroF1ValCallback(val_ds, val_labels)

    cb_list = [
        callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
        callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=1),
        callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1),
        f1_cb
    ]

    print(f"\n[Training] Starting Custom CNN training for up to {epochs} epochs...")
    start_time = time.time()
    hist = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        class_weight=class_weights,
        callbacks=cb_list,
        verbose=1
    )
    total_training_time = time.time() - start_time
    print(f"[Training] Custom CNN finished in {total_training_time:.1f}s")

    # Save training history
    history_dict = hist.history
    history_dict['val_macro_f1'] = f1_cb.macro_f1_history
    history_dict['training_time_seconds'] = total_training_time
    history_dict['epochs_trained'] = len(hist.history['loss'])
    
    with open('results/cnn/history.json', 'w') as f:
        json.dump(history_dict, f, indent=2)

    plot_and_save_curves(history_dict, 'results/cnn/training_curves.png', model_name='Custom CNN Baseline')

    # Load best model for evaluation on unseen test set
    best_model = tf.keras.models.load_model(model_path)

    print("\n[Evaluation] Evaluating Custom CNN on unseen test set...")
    t0 = time.time()
    test_preds_proba = best_model.predict(test_ds, verbose=1)
    inference_duration = (time.time() - t0)
    avg_inference_ms = (inference_duration / len(test_samples)) * 1000.0

    test_preds = np.argmax(test_preds_proba, axis=1)

    # Metrics
    prec, rec, f1, support = precision_recall_fscore_support(test_labels, test_preds, average=None, zero_division=0)
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(test_labels, test_preds, average='macro', zero_division=0)
    acc = np.mean(np.array(test_labels) == test_preds)
    cm = confusion_matrix(test_labels, test_preds)

    plot_confusion_matrix(cm, 'results/cnn/confusion_matrix.png', model_name='Custom CNN Baseline')

    report_str = classification_report(test_labels, test_preds, target_names=CLASS_NAMES, digits=4, zero_division=0)
    with open('results/cnn/classification_report.txt', 'w') as f:
        f.write(report_str)

    results = {
        'model': 'CNN',
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

    with open('results/cnn/test_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*50)
    print("CUSTOM CNN TEST RESULTS:")
    print(f"Accuracy:        {acc * 100:.2f}%")
    print(f"Macro-F1:        {macro_f1:.4f}")
    print(f"High-Risk Recall:{rec[2]:.4f}")
    print(f"Inference Time:  {avg_inference_ms:.2f} ms/image")
    print("="*50)
    print(report_str)

    return results

if __name__ == '__main__':
    train_and_evaluate_cnn(epochs=20, batch_size=32, lr=0.001)
