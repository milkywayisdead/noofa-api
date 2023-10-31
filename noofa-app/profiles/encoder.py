import numpy as np

noofa_encoder = {
    np.int64: lambda x: x.item(),
    np.ndarray: lambda x: x.tolist(),
}