import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def histplot_feature(df, subset, column_name, save_path=None):
    
    if column_name not in df.columns: 
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    all_values = df[column_name]
    subset_values = subset[column_name]
    
    mean_all = all_values.mean()
    std_all = all_values.std()
    all_values = all_values[np.abs(all_values - np.mean(all_values)) <= 3*np.std(all_values)]
    
    plt.hist(all_values, bins=30, alpha=0.5, label='All ICs', color='blue')
    plt.hist(subset_values, bins=30, alpha=0.8, label='EZ Candidates', color='red')
    
    plt.axvline(mean_all, color='black', linestyle='dashed', linewidth=1, label=f'Mean: {mean_all:.2f}')
    plt.axvline(mean_all + std_all, color='grey', linestyle='dotted', linewidth=1, label=f'+1 STD: {mean_all + std_all:.2f}')
    plt.axvline(mean_all - std_all, color='grey', linestyle='dotted', linewidth=1, label=f'-1 STD: {mean_all - std_all:.2f}')
    
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column_name}')
    plt.legend(prop={'size': 7})
    
    if save_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, format='svg')
        
    plt.show()

def boxplot_features(df, subset_df, column_names, norm=True, save_path=None):
    
    if norm:
        means = df.mean()
        stds = df.std()
        df = (df - means) / stds
        subset_df = (subset_df - means) / stds
    
    df.columns = df.columns.str.strip() 
    subset_df.columns = subset_df.columns.str.strip()
    
    invalid_columns = [col for col in column_names if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid column names: {', '.join(invalid_columns)}")
    
    missing_subset_columns = [col for col in column_names if col not in subset_df.columns]
    if missing_subset_columns:
        raise ValueError(f"Subset DataFrame is missing columns: {', '.join(missing_subset_columns)}")

    plt.figure(figsize=(8, 6))

    data_to_plot = []
    highlighted_data = []

    for column in column_names:
        all_data = df[column].dropna()
        data_to_plot.append(all_data)

        subset_data = subset_df[column].dropna()
        highlighted_data.append(subset_data)

    plt.boxplot(data_to_plot, positions=np.arange(1, len(column_names) + 1), widths=0.5, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='black'), medianprops=dict(color='black'),
                showfliers=False, showcaps=False, whiskerprops=dict(color='black'))

    plt.boxplot(highlighted_data, positions=np.arange(1, len(column_names) + 1), widths=0.3, patch_artist=True,
                boxprops=dict(facecolor='salmon', color='red', alpha=0.6), medianprops=dict(color='red'),
                showfliers=False, showcaps=False, whiskerprops=dict(color='red'))

    plt.xticks(np.arange(1, len(column_names) + 1), column_names, rotation=45, ha='right')

    plt.ylabel('Normalized Distributions')
    plt.title('IC Features with Epileptic ICs Highlighted')

    plt.tight_layout()
    
    if save_path:
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, format='svg')
    
    plt.show()
