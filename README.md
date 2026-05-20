---
title: Edge Detection Playground
emoji: 🖼️
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# Edge Detection Playground

An interactive educational app for exploring classical edge detection algorithms in image analysis.

Built with Streamlit and OpenCV.

---

# Project Summary

This app demonstrates how different edge detection algorithms respond to image structure, noise, smoothing, and threshold selection.

Implemented algorithms:
- Sobel
- Laplacian
- Canny

The application was designed as an educational visualization tool for students learning introductory computer vision and image analysis concepts.

Users can:
- upload their own images
- explore parameter sensitivity interactively
- compare edge detection outputs side-by-side
- inspect diagnostic visualizations
- observe algorithm trade-offs

---

# Features

## Interactive Controls
- Upload custom images
- Built-in sample image
- Adjustable edge detection parameters
- Adjustable edge density evaluation threshold

## Visualization
- Side-by-side input/output comparison
- Sobel gradient magnitude heatmap
- Laplacian zero-crossing overlay
- Canny edge classification map

## Evaluation Metric
- Edge density metric with adjustable threshold interpretation

## Reliability
- Invalid file handling
- Automatic image resizing for responsiveness
- Stable operation on standard image sizes

---

# Algorithms Included

## Sobel

Computes first-order image gradients in horizontal and vertical directions.

Diagnostic view:
- Gradient magnitude heatmap

Demonstrates:
- edge strength
- directional gradients
- smoothing trade-offs

---

## Laplacian

Computes second-order image derivatives.

Diagnostic view:
- Zero-crossing overlay

Demonstrates:
- second-derivative edge detection
- sensitivity to noise
- effect of Gaussian smoothing

---

## Canny

Multi-stage edge detector using:
- Gaussian smoothing
- gradient computation
- non-maximum suppression
- hysteresis thresholding

Diagnostic view:
- Strong vs weak edge classification map

Demonstrates:
- threshold sensitivity
- edge tracking behavior
- noise robustness

---

# Local Run Instructions

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd edge-detection-playground
```

## 2. Create and activate virtual environment

### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the app

```bash
streamlit run app.py
```

---

# Hugging Face Space URL

```text
https://huggingface.co/spaces/nyc0le/edge-detection-playground
```

---

# Screenshots

## Main Interface

[Screenshot here of side-by-side image comparison and controls]

---

## Sobel Diagnostic View

[Screenshot here of gradient magnitude heatmap]

---

## Laplacian Diagnostic View

[Screenshot here of zero-crossing overlay]

---

## Canny Diagnostic View

[Screenshot here of strong/weak edge classification map]

---

# Repository Structure

```text
edge-detection-playground/
│
├── app.py
├── processing.py
├── metrics.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── sample_images/
│   └── portrait.jpeg
│
└── docs/
    └── design_choices.md
```

---

# Known Limitations

- The app is designed for educational visualization rather than production computer vision pipelines.
- The Canny classification map visualizes gradient magnitude thresholds before hysteresis thresholding rather than OpenCV internal intermediate states.
- Laplacian zero-crossing detection is intentionally simplified for interpretability.
- Extremely large images may still increase processing time.

---

# Technologies Used

- Python
- Streamlit
- OpenCV
- NumPy
- Matplotlib
- Pillow

---

# Educational Goals

This project was designed to help students:
- understand classical edge detection methods
- explore parameter sensitivity
- compare algorithm behavior
- interpret diagnostic visualizations
- connect mathematical concepts to image analysis results