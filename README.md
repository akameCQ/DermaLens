<div align="center">
  <img src="https://via.placeholder.com/150" width="150" alt="DermaLens Logo">
  <h1>DermaLens</h1>
  <p><b>AI-Powered Skin Cancer Detection System</b></p>
</div>

---

DermaLens is a state-of-the-art desktop application designed to assist in predicting skin cancer classes from dermoscopic images. Powered by Deep Learning, it offers a real-time, interactive, and visually stunning interface for analyzing skin lesions.

## ✨ Features

- 🧠 **Deep Learning Core**: Utilizes an EfficientNet-based TensorFlow model to accurately classify skin lesions into 7 distinct categories.
- 🎨 **Modern User Interface**: A sleek, dark-themed GUI built entirely in Tkinter, offering a premium user experience.
- 📊 **Real-Time Analytics**: Instantly view detailed probability breakdowns, interactive pie charts, and top diagnoses.
- 🕒 **History Tracking**: Seamlessly keeps track of your recent scans directly within the interface.

---

## 📷 Screenshots

> *(Replace the placeholder image below with an actual screenshot of the DermaLens interface)*

<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=DermaLens+Interface+Screenshot" alt="DermaLens Interface">
</div>

---

## 🔬 Supported Classes

The AI model is trained to recognize the following skin conditions:

| Code   | Class Name                     |
| :---   | :---                           |
| **akiec** | Actinic Keratoses / Bowen's Disease |
| **bcc**   | Basal Cell Carcinoma           |
| **bkl**   | Benign Keratosis-like Lesions  |
| **df**    | Dermatofibroma                 |
| **mel**   | Melanoma                       |
| **nv**    | Melanocytic Nevi               |
| **vasc**  | Vascular Lesions               |

---

## 🚀 Installation & Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/yourusername/dermalens.git
   cd dermalens
   ```

2. **Install the required dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Model Weights**:
   Make sure the pre-trained weights (`dermalens_best_2.h5`) are located in the `checkpoints` directory.

---

## 💻 Usage

Start the graphical interface by running the following command in your terminal:

```bash
python new_gui.py
```

Simply click **"Upload Image"**, select a dermoscopic image (PNG, JPG, JPEG), and let the AI perform its analysis!

---

<div align="center">
  <p><i>Developed for advanced dermatological analysis.</i></p>
</div>
