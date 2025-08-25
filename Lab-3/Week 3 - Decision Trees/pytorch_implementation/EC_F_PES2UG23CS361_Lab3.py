"""
SRN: PES2UG23CS361
Campus: EC
Section: F
"""
# lab.py
import torch

def get_entropy_of_dataset(tensor: torch.Tensor):
    """
    Calculate the entropy of the entire dataset.
    Formula: Entropy = -Σ(p_i * log2(p_i)) where p_i is the probability of class i

    Args:
        tensor (torch.Tensor): Input dataset as a tensor, where the last column is the target.

    Returns:
        float: Entropy of the dataset.
    """
    target_col = tensor[:, -1]
    values, counts = torch.unique(target_col, return_counts=True)
    probabilities = counts.float() / counts.sum()
    entropy = -torch.sum(probabilities * torch.log2(probabilities + 1e-10))
    return float(entropy)


def get_avg_info_of_attribute(tensor: torch.Tensor, attribute: int):
    """
    Calculate the average information (weighted entropy) of an attribute.
    Formula: Avg_Info = Σ((|S_v|/|S|) * Entropy(S_v)) where S_v is subset with attribute value v.

    Args:
        tensor (torch.Tensor): Input dataset as a tensor.
        attribute (int): Index of the attribute column.

    Returns:
        float: Average information of the attribute.
    """
    total = tensor.shape[0]
    avg_info = 0.0
    attr_col = tensor[:, attribute]
    values, counts = torch.unique(attr_col, return_counts=True)
    for v, count in zip(values, counts):
        subset = tensor[attr_col == v]
        entropy = get_entropy_of_dataset(subset)
        avg_info += (count.item() / total) * entropy
    return float(avg_info)


def get_information_gain(tensor: torch.Tensor, attribute: int):
    """
    Calculate Information Gain for an attribute.
    Formula: Information_Gain = Entropy(S) - Avg_Info(attribute)

    Args:
        tensor (torch.Tensor): Input dataset as a tensor.
        attribute (int): Index of the attribute column.

    Returns:
        float: Information gain for the attribute (rounded to 4 decimals).
    """
    entropy = get_entropy_of_dataset(tensor)
    avg_info = get_avg_info_of_attribute(tensor, attribute)
    info_gain = entropy - avg_info
    return round(info_gain, 4)


def get_selected_attribute(tensor: torch.Tensor):
    """
    Select the best attribute based on highest information gain.

    Returns a tuple with:
    1. Dictionary mapping attribute indices to their information gains
    2. Index of the attribute with highest information gain
    
    Example: ({0: 0.123, 1: 0.768, 2: 1.23}, 2)

    Args:
        tensor (torch.Tensor): Input dataset as a tensor.

    Returns:
        tuple: (dict of attribute:index -> information gain, index of best attribute)
    """
    n_attributes = tensor.shape[1] - 1
    gains = {}
    for attr in range(n_attributes):
        gains[attr] = get_information_gain(tensor, attr)
    selected = max(gains, key=gains.get)
    return gains, selected
