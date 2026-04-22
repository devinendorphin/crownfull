"""
CrownFull v2.1 - Core Mathematics
Implements k-Nearest Neighbors (k-NN) Jensen-Shannon Divergence and Regularized Polyphonic Disparity.
"""
import torch
import numpy as np
from typing import List

def knn_kl_divergence(X: torch.Tensor, Y: torch.Tensor, k: int = 5) -> float:
    """Estimates KL(P || Q) using a k-NN estimator for high-dimensional tensor clouds."""
    n, d = X.shape
    m = Y.shape[0]
    if n < k + 1 or m < k: 
        return 0.0 
        
    Z = torch.cat([X, Y], dim=0)
    
    dist_self = torch.cdist(X, X, p=2)
    dist_self.fill_diagonal_(float('inf'))
    kth_self, _ = torch.kthvalue(dist_self, k, dim=1)
    
    dist_mix = torch.cdist(X, Z, p=2)
    kth_mix, _ = torch.kthvalue(dist_mix, k, dim=1)
    
    kl = (d / n) * torch.sum(torch.log((kth_mix + 1e-8) / (kth_self + 1e-8))) + np.log(m / (n - 1))
    return float(kl.item())

def jensen_shannon_divergence(X: torch.Tensor, Y: torch.Tensor, k: int = 5) -> float:
    """Computes symmetric Jensen-Shannon divergence from k-NN KL estimates."""
    return 0.5 * knn_kl_divergence(X, Y, k) + 0.5 * knn_kl_divergence(Y, X, k)

def compute_phi_disparity(js_short: List[float], js_long: List[float], turn_index: int, t_min: int = 50, prior_var: float = 0.05) -> float:
    """Calculates regularized polyphonic disparity (variance ratio) to detect grooming trenches."""
    var_short = np.var(js_short) if len(js_short) > 1 else 0.0
    var_long_emp = np.var(js_long) if len(js_long) > 1 else 0.0
    
    alpha = max(0.0, 1.0 - turn_index / t_min)
    var_long_reg = alpha * prior_var + (1.0 - alpha) * var_long_emp
    
    if var_short < 1e-6: 
        return 0.0
        
    return var_short / (var_long_reg + 1e-8)
