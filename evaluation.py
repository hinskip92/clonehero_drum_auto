
import numpy as np
from utils.logger import logger

def f1_score(pred, ref, tol=0.05):
    """Compute F1 for onset detection within tol seconds."""
    pred = np.asarray(pred)
    ref = np.asarray(ref)
    matched = np.zeros(len(ref), dtype=bool)
    tp = 0
    for p in pred:
        idx = np.where(np.abs(ref - p) <= tol)[0]
        if idx.size:
            i = idx[0]
            if not matched[i]:
                matched[i] = True
                tp += 1
    fp = len(pred) - tp
    fn = len(ref) - matched.sum()
    prec = tp / (tp + fp + 1e-9)
    rec = tp / (tp + fn + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    logger.info("Precision %.2f Recall %.2f F1 %.2f", prec, rec, f1)
    return f1
