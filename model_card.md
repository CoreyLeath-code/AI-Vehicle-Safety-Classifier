# 📄 Model Card — AI Vehicle Safety Classifier

## 1. Model Summary
A convolutional neural network (CNN) trained to classify vehicle driving conditions into *Safe* and *Unsafe*. Intended for use in driver assistance systems and intelligent vehicle monitoring.

---

## 2. Intended Use
- Dashcam monitoring  
- Insurance claim validation  
- Fleet vehicle safety analysis  
- Autonomous vehicle pre-processing  

Not intended for *real-time* emergency intervention without human oversight.

---

## 3. Architecture Overview
- Convolutional layers (3 blocks)  
- Batch normalization  
- Dropout (0.3)  
- Dense classifier with softmax  
- Adam optimizer  

---

## 4. Dataset
- 1,260 total labeled images  
- Balanced classes  
- Train/val/test split = 70/15/15  
- Augmentations: rotation, blur, brightness, motion distortion  

---

## 5. Performance Metrics
See **metrics.md** for full details.

Best F1 Score = **0.907**

ROC-AUC = **0.958**

---

## 6. Ethical Considerations

### Potential Risks
- Bias if trained only on certain environments (e.g., daytime, clear weather)  
- May misclassify rare driving scenarios  
- Cannot replace human judgment in insurance or legal cases  

### Mitigation Steps
- Expand dataset to include diverse lighting + weather  
- Add uncertainty estimation  
- Continuous monitoring of false positives  

---

## 7. Limitations
- Not trained on video sequences — single-frame only  
- Not robust to night conditions unless supplemented  
- Limited by dataset size  

---

## 8. Reproducibility
Environment and seeds stored in `reproducibility.md`.

---

## 9. Maintainer
Corey Leath (CoreyLeath-code)  
GitHub: https://github.com/CoreyLeath-code