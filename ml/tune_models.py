import os
import json
import time
import numpy as np
import optuna
from sklearn.metrics import f1_score
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

try:
    from ml.preprocessing import get_or_create_splits, compute_train_class_weights, build_dataset
except ImportError:
    from preprocessing import get_or_create_splits, compute_train_class_weights, build_dataset

optuna.logging.set_verbosity(optuna.logging.WARNING)

def objective_cnn(trial):
    splits = get_or_create_splits()
    train_samples = splits['train']
    val_samples = splits['val']
    class_weights = compute_train_class_weights(train_samples)

    # Hyperparameters to tune
    lr = trial.suggest_float('learning_rate', 1e-4, 2e-3, log=True)
    dropout_rate = trial.suggest_float('dropout_rate', 0.2, 0.5, step=0.1)
    dense_units = trial.suggest_categorical('dense_units', [64, 128, 256])
    batch_size = trial.suggest_categorical('batch_size', [16, 32])

    train_ds = build_dataset(train_samples, batch_size=batch_size, is_training=True)
    val_ds = build_dataset(val_samples, batch_size=batch_size, is_training=False)
    val_labels = [s['label'] for s in val_samples]

    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.GlobalAveragePooling2D(),
        layers.Dense(dense_units, activation='relu'),
        layers.Dropout(dropout_rate),
        layers.Dense(3, activation='softmax')
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    epochs_to_run = 2
    start_t = time.time()
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs_to_run,
        class_weight=class_weights,
        verbose=0
    )
    duration = time.time() - start_t

    preds = model.predict(val_ds, verbose=0)
    pred_classes = np.argmax(preds, axis=1)
    val_macro_f1 = f1_score(val_labels, pred_classes, average='macro', zero_division=0)

    trial.set_user_attr('training_time', duration)
    trial.set_user_attr('epochs', epochs_to_run)
    print(f"  Trial {trial.number}: Val Macro-F1={val_macro_f1:.4f} (lr={lr:.5f}, dropout={dropout_rate}, units={dense_units}, batch={batch_size}, time={duration:.1f}s)")
    return val_macro_f1

def run_optuna_tuning(n_trials=3):
    os.makedirs('results', exist_ok=True)
    print(f"\n[Optuna] Starting Optuna hyperparameter study ({n_trials} trials, objective=Validation Macro-F1)...")
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective_cnn, n_trials=n_trials)

    best = study.best_trial
    print("\n[Optuna] Best Trial:")
    print(f"  Validation Macro-F1: {best.value:.4f}")
    print(f"  Params: {best.params}")

    tuning_results = {
        'best_trial_number': best.number,
        'best_val_macro_f1': float(best.value),
        'best_params': best.params,
        'all_trials': [
            {
                'number': t.number,
                'value_macro_f1': float(t.value) if t.value is not None else None,
                'params': t.params,
                'epochs': int(t.user_attrs.get('epochs', 2)),
                'training_time': float(t.user_attrs.get('training_time', 0.0))
            } for t in study.trials
        ]
    }

    with open('results/optuna_tuning.json', 'w') as f:
        json.dump(tuning_results, f, indent=2)

    print(f"[Optuna] Saved tuning results to results/optuna_tuning.json")
    return tuning_results

if __name__ == '__main__':
    run_optuna_tuning(n_trials=3)
