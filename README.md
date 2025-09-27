# Dermalens

Dermalens is a desktop application built with Python, TensorFlow, and PyQt5 for classifying skin lesions. The model uses **EfficientNetB0** and has been trained on the **HAM10000** dataset. The application provides a user-friendly PyQt5 GUI for image upload and real-time predictions. Training is supported with checkpointing and data augmentation.

Features:
- Classifies skin lesions into 7 classes: akiec, bcc, bkl, df, mel, nv, vasc
- Real-time predictions via PyQt5 GUI
- Training with data augmentation
- Checkpointing and model backup
- User-friendly file upload and table display

Setup:
1. Clone the repository:
```
git clone https://github.com/username/dermalens.git
cd dermalens
```
2. Create a virtual environment (optional but recommended):
```
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```
3. Install required libraries:
```
pip install -r requirements.txt
```

Usage:
- Run the GUI:
```
python gui.py
```
- Click the "Upload File" button to select an image.
- Model predictions will appear in the table and class probabilities will be shown in the terminal.

Project Structure:
- Dataset/             # HAM10000 training data
- checkpoints/         # Model checkpoints
- flow.py              # Model class (EfficientNetB0)
- data_loader.py       # Dataset loading and preprocessing
- data_prepare.py       # Data augmentation
- results.py           # Prediction and result handling
- main.py              # For model training, does not launch the GUI
- gui.py               # Main GUI application, launched by the user
- Base.png             # Temporary preprocessed image created during prediction
- requirements.txt     # Required libraries
- README.md            # Project description

Model Training:
- Epochs: 20
- Batch size: 16
- Optimizer: Adam (lr=0.001)
- Loss: Sparse Categorical Crossentropy
- Early stopping and checkpoints used

License:
MIT License. This project is released under the MIT License; it can be freely used, modified, and distributed.
