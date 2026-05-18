#Visualization & Analytics Dashboard : 
#This file handles: loading dataset , preprocessing ,helper methods

# utils.py

"""
Utility functions for loading and preprocessing
Aadhaar enrollment anomaly detection datasets.
"""

import pandas as pd


def load_data(path):
    """
    Load dataset from CSV file.

    Args:
        path (str): Path to CSV dataset.

    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    
    df = pd.read_csv(path)
    
    return df