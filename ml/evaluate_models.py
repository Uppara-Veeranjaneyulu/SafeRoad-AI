import os
import json
import pandas as pd
import numpy as np

def generate_model_comparison():
    models = ['cnn', 'mobilenetv2', 'efficientnetb0', 'resnet50']
    model_display = {
        'cnn': 'Custom CNN',
        'mobilenetv2': 'MobileNetV2',
        'efficientnetb0': 'EfficientNetB0',
        'resnet50': 'ResNet50'
    }

    all_metrics = []
    
    for m in models:
        metric_file = f'results/{m}/test_metrics.json'
        if os.path.exists(metric_file):
            with open(metric_file, 'r') as f:
                data = json.load(f)
                all_metrics.append({
                    'model_key': m,
                    'Model': model_display.get(m, m),
                    'Accuracy': f"{data['accuracy'] * 100:.2f}%",
                    'Precision': f"{data['precision'] * 100:.2f}%",
                    'Recall': f"{data['recall'] * 100:.2f}%",
                    'F1': f"{data['f1_score'] * 100:.2f}%",
                    'Macro-F1': f"{data['macro_f1'] * 100:.2f}%",
                    'High-Risk Recall': f"{data['high_risk_recall'] * 100:.2f}%",
                    'Inference Time': f"{data['inference_time_ms']:.1f} ms",
                    '_raw_acc': data['accuracy'],
                    '_raw_macro_f1': data['macro_f1'],
                    '_raw_f1': data['f1_score'],
                    '_raw_hr_recall': data['high_risk_recall'],
                    '_raw_inf_time': data['inference_time_ms'],
                    'Parameters': f"{data['total_parameters']:,}"
                })
        else:
            print(f"[Comparison] Warning: {metric_file} not found yet.")

    if not all_metrics:
        print("[Comparison] No trained model metrics found yet.")
        return None

    # Sorting / Ranking logic:
    # 1. Macro-F1 (primary)
    # 2. High-Risk Recall
    # 3. Overall F1
    # 4. Accuracy
    # 5. Inference time (faster is better)
    sorted_models = sorted(
        all_metrics,
        key=lambda x: (x['_raw_macro_f1'], x['_raw_hr_recall'], x['_raw_f1'], x['_raw_acc'], -x['_raw_inf_time']),
        reverse=True
    )

    best_model_entry = sorted_models[0]
    best_model_name = best_model_entry['Model']
    best_model_key = best_model_entry['model_key']

    df = pd.DataFrame(all_metrics)
    display_cols = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1', 'Macro-F1', 'High-Risk Recall', 'Inference Time', 'Parameters']
    clean_df = df[display_cols]
    
    os.makedirs('results', exist_ok=True)
    clean_df.to_csv('results/model_comparison.csv', index=False)
    
    with open('results/model_comparison.json', 'w') as f:
        json.dump({
            'comparison': all_metrics,
            'best_model': best_model_entry,
            'best_model_name': best_model_name,
            'best_model_key': best_model_key
        }, f, indent=2)

    with open('trained_models/best_model_meta.json', 'w') as f:
        json.dump({
            'best_model_name': best_model_name,
            'best_model_key': best_model_key,
            'weights_file': f"trained_models/{best_model_key}_best.keras",
            'accuracy': best_model_entry['Accuracy'],
            'macro_f1': best_model_entry['Macro-F1'],
            'high_risk_recall': best_model_entry['High-Risk Recall'],
            'inference_time': best_model_entry['Inference Time'],
            'selection_criteria': 'Ranked by Macro-F1, High-Risk Recall, Overall F1, Accuracy, and Inference Time'
        }, f, indent=2)

    print("\n" + "="*80)
    print("FINAL MODEL COMPARISON TABLE (UNSEEN TEST SET)")
    print("="*80)
    print(clean_df.to_string(index=False))
    print("="*80)
    print(f"BEST MODEL = {best_model_name.upper()}")
    print(f"  Accuracy:         {best_model_entry['Accuracy']}")
    print(f"  Macro-F1:         {best_model_entry['Macro-F1']}")
    print(f"  High-Risk Recall: {best_model_entry['High-Risk Recall']}")
    print(f"  Inference Time:   {best_model_entry['Inference Time']}")
    print("="*80 + "\n")

    return best_model_entry

if __name__ == '__main__':
    generate_model_comparison()
