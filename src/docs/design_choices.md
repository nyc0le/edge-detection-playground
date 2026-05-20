# Design Choices

## Educational Focus

The application was designed primarily as an interactive educational tool rather than a production image processing pipeline.

The main goal was to help users understand:
- how edge detection algorithms work
- how parameter choices affect results
- how different algorithms behave under noise and smoothing

The interface emphasizes interpretability and visualization clarity.

---

# Algorithm Selection

The project focuses on three classical edge detection algorithms:
- Sobel
- Laplacian
- Canny

These algorithms were selected because they represent different edge detection philosophies:

| Algorithm | Main Idea |
|---|---|
| Sobel | First-order gradients |
| Laplacian | Second-order derivatives |
| Canny | Multi-stage robust edge detection |

This allows direct comparison of:
- sensitivity
- noise robustness
- edge continuity
- threshold behavior

---

# Diagnostic Visualizations

Instead of only showing final edge outputs, the app includes algorithm-specific diagnostic views.

## Sobel

Uses a gradient magnitude heatmap to visualize edge strength.

Purpose:
- show spatial gradient intensity
- connect derivatives to edge detection

---

## Laplacian

Uses a zero-crossing overlay.

Purpose:
- visualize sign changes of the second derivative
- demonstrate why Laplacian is sensitive to noise

Gaussian smoothing was added to allow exploration of noise suppression.

---

## Canny

Uses a strong/weak edge classification map based on gradient magnitude thresholds.

Purpose:
- visualize hysteresis thresholding concepts
- demonstrate how thresholds classify edge responses

The visualization is intentionally educational rather than a direct extraction of OpenCV internal intermediate states.

---

# Evaluation Metric

The app uses edge density as a simple quantitative metric.

Edge density measures:
- percentage of pixels exceeding a selected edge-response threshold

A user-adjustable threshold was chosen because:
- different algorithms produce different response distributions
- edge interpretation depends on threshold selection

This also reinforces the concept of parameter sensitivity.

---

# Reliability and Usability

Several design choices were made to improve usability:

- invalid file handling
- automatic image resizing
- simple parameter controls
- clear labels and interpretation text
- side-by-side visualization layout

The interface was intentionally kept minimal to support non-expert users.

---

# Deployment

The app was deployed using:
- Hugging Face Spaces
- Docker-based deployment
- Streamlit frontend

The repository structure was kept modular for readability and reproducibility.

---

# Future Improvements

Potential future extensions include:
- non-maximum suppression visualization
- interactive edge tracing
- additional edge detectors
- image noise simulation
- quantitative edge quality metrics
- real-time webcam input