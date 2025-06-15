import os
import numpy as np
import pandas as pd
import torch
import shap
import matplotlib.pyplot as plt

def run_shap_analysis():
    """Perform SHAP analysis for all models (fixing data type issues)"""

    feature_names = ['致癌性', '致畸性', '致突变性', '急性毒性', '刺激与腐蚀性', '内分泌干扰',
                     '中国严管', '优先控制', '危化品名录', '易制爆', 'EPA', '重点环境管控', '重点监管', '高毒']

    model_names = ["MLP", "MLP_Attention", "CNN", "CNN_Attention", "Attention"]

    for model_name in model_names:
        try:
            print(f"\n{'='*100}\nLoading model: {model_name}")

            model_path = f'FINAL_{model_name}.pth'
            checkpoint = torch.load(model_path)

            if model_name == "MLP":
                model = MLP(X_test.shape[1])
            elif model_name == "MLP_Attention":
                model = MLP_Attention(X_test.shape[1])
            elif model_name == "CNN":
                model = CNNModel(X_test.shape[1])
            elif model_name == "CNN_Attention":
                model = CNN_Attention(X_test.shape[1])
            elif model_name == "Attention":
                model = AttentionModel(X_test.shape[1])
            else:
                raise ValueError(f"Unknown model: {model_name}")

            model.load_state_dict(checkpoint['model_state'])
            model = model.to(device)
            model.eval()

            shap_analysis(model, X_test, feature_names, model_name, device)

        except Exception as e:
            print(f"Error processing model {model_name}: {e}")

    print("\n✅ SHAP analysis completed for all models.")

def shap_analysis(model, X_test, feature_names, model_name, device):
    """SHAP analysis function with data type fixes"""
    print(f"\n{'='*80}\nRunning SHAP analysis: {model_name}\n{'='*80}")

    os.makedirs("results/shap_analysis/plots", exist_ok=True)
    os.makedirs("results/shap_analysis/values", exist_ok=True)

    mapped_feature_names = map_feature_names(feature_names)
    X_test_df = pd.DataFrame(X_test, columns=feature_names)
    X_test_df.to_csv(f"results/shap_analysis/values/X_test.csv", index=False)

    def model_wrapper(x_df):
        x_tensor = torch.tensor(x_df.values, dtype=torch.float32).to(device)
        if x_tensor.ndim == 1:
            x_tensor = x_tensor.unsqueeze(0)
        with torch.no_grad():
            return model(x_tensor).cpu().numpy()

    masker = shap.maskers.Independent(data=X_test_df)
    explainer = shap.Explainer(model_wrapper, masker=masker)

    shap_values = explainer(X_test_df)

    shap_df = pd.DataFrame(shap_values.values, columns=feature_names)
    shap_df.to_csv(f"results/shap_analysis/values/{model_name}_shap_values.csv", index=False)

    shap_mapped_df = pd.DataFrame(shap_values.values, columns=mapped_feature_names)
    shap_mapped_df.to_csv(f"results/shap_analysis/values/{model_name}_shap_values_mapped.csv", index=False)

    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_test_df, feature_names=mapped_feature_names, show=False)
    plt.title(f'SHAP Summary Plot for {model_name}')
    plt.savefig(f"results/shap_analysis/plots/{model_name}_shap_summary.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_test_df, feature_names=mapped_feature_names, plot_type="bar", show=False)
    plt.title(f'SHAP Bar Plot for {model_name}')
    plt.savefig(f"results/shap_analysis/plots/{model_name}_shap_bar.png", dpi=300, bbox_inches='tight')
    plt.close()

    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    top_indices = np.argsort(mean_abs_shap)[-3:]
    for idx in top_indices:
        original_name = feature_names[idx]
        mapped_name = mapped_feature_names[idx]
        plt.figure(figsize=(10, 7))
        shap.dependence_plot(
            idx, shap_values.values, X_test_df,
            feature_names=mapped_feature_names, show=False
        )
        plt.title(f"SHAP Dependence Plot - {mapped_name}")
        plt.savefig(f"results/shap_analysis/plots/{model_name}_shap_dependence_{original_name}.png", dpi=300, bbox_inches='tight')
        plt.close()

    print("SHAP analysis complete.")
    return shap_values