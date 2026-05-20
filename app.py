import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

from PIL import Image

from processing import (
    convert_to_gray,
    apply_sobel,
    apply_laplacian,
    apply_canny
)

from metrics import edge_density

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Edge Detection Playground",
    layout="wide"
)

st.title("Edge Detection Playground")

st.markdown("""
This interactive tool demonstrates classical edge detection algorithms and visualizes how parameter choices affect edge extraction behavior.

The app focuses on:
- parameter sensitivity
- algorithm trade-offs
- gradient behavior
- thresholding behavior
- noise sensitivity
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Controls")

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Sobel", "Laplacian", "Canny"]
)

# ---------------------------------------------------
# IMAGE INPUT
# ---------------------------------------------------

sample_choice = st.sidebar.selectbox(
    "Load Built-in Example",
    ["None", "Portrait"]
)

uploaded_file = st.file_uploader(
    "Or upload your own image"
)

image = None

# ---------------------------------------------------
# LOAD SAMPLE IMAGE
# ---------------------------------------------------

if sample_choice != "None":

    sample_path = os.path.join(
        "sample_images",
        "portrait.jpeg"
    )

    image = Image.open(sample_path).convert("RGB")
    image = np.array(image)

# ---------------------------------------------------
# LOAD UPLOADED IMAGE
# ---------------------------------------------------

elif uploaded_file is not None:

    valid_extensions = [
        "png",
        "jpg",
        "jpeg"
    ]

    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension not in valid_extensions:

        st.error(
            "Invalid input format. Please upload a PNG or JPG image."
        )

    else:

        image = Image.open(uploaded_file).convert("RGB")
        image = np.array(image)

# ---------------------------------------------------
# MAIN PROCESSING
# ---------------------------------------------------

if image is not None:

    # Resize large images for responsiveness
    max_width = 1200

    if image.shape[1] > max_width:

        scale = max_width / image.shape[1]

        new_height = int(image.shape[0] * scale)

        image = cv2.resize(
            image,
            (max_width, new_height)
        )

    gray = convert_to_gray(image)

    # ---------------------------------------------------
    # METRIC SETTINGS
    # ---------------------------------------------------

    st.sidebar.subheader("Evaluation Metric Settings")

    edge_metric_threshold = st.sidebar.slider(
        "Edge Density Threshold",
        0,
        255,
        50
    )

    # ---------------------------------------------------
    # ALGORITHM PARAMETERS
    # ---------------------------------------------------

    st.sidebar.subheader("Algorithm Parameters")

    # ---------------------------------------------------
    # SOBEL
    # ---------------------------------------------------

    if algorithm == "Sobel":

        ksize = st.sidebar.slider(
            "Kernel Size",
            1,
            7,
            3,
            step=2
        )

        sobelx = cv2.Sobel(
            gray,
            cv2.CV_64F,
            1,
            0,
            ksize=ksize
        )

        sobely = cv2.Sobel(
            gray,
            cv2.CV_64F,
            0,
            1,
            ksize=ksize
        )

        magnitude = np.sqrt(
            sobelx**2 + sobely**2
        )

        result = cv2.convertScaleAbs(magnitude)

        diagnostic_title = "Gradient Magnitude Heatmap"

    # ---------------------------------------------------
    # LAPLACIAN
    # ---------------------------------------------------

    elif algorithm == "Laplacian":

        ksize = st.sidebar.slider(
            "Kernel Size",
            1,
            7,
            3,
            step=2
        )

        sigma = st.sidebar.slider(
            "Gaussian Sigma",
            0.0,
            5.0,
            1.0,
            step=0.1
        )

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            sigma
        )

        laplacian = cv2.Laplacian(
            blurred,
            cv2.CV_64F,
            ksize=ksize
        )

        result = cv2.convertScaleAbs(laplacian)

        zero_crossing = np.zeros_like(laplacian)

        rows, cols = laplacian.shape

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):

                patch = laplacian[i-1:i+2, j-1:j+2]

                p = patch.max()
                n = patch.min()

                if p > 0 and n < 0:
                    zero_crossing[i, j] = 255

        diagnostic_title = "Zero-Crossing Map"

    # ---------------------------------------------------
    # CANNY
    # ---------------------------------------------------

    elif algorithm == "Canny":

        threshold1 = st.sidebar.slider(
            "Lower Threshold",
            0,
            255,
            100
        )

        threshold2 = st.sidebar.slider(
            "Upper Threshold",
            0,
            255,
            200
        )

        blur_size = st.sidebar.slider(
            "Gaussian Blur Size",
            1,
            11,
            5,
            step=2
        )

        blurred = cv2.GaussianBlur(
            gray,
            (blur_size, blur_size),
            0
        )

        # Gradient computation BEFORE hysteresis
        grad_x = cv2.Sobel(
            blurred,
            cv2.CV_64F,
            1,
            0,
            ksize=3
        )

        grad_y = cv2.Sobel(
            blurred,
            cv2.CV_64F,
            0,
            1,
            ksize=3
        )

        magnitude = np.sqrt(
            grad_x**2 + grad_y**2
        )

        magnitude = cv2.convertScaleAbs(magnitude)

        # Final Canny result
        result = cv2.Canny(
            blurred,
            threshold1,
            threshold2
        )

        # Educational edge classification
        strong_edges = magnitude >= threshold2

        weak_edges = (
            (magnitude >= threshold1) &
            (magnitude < threshold2)
        )

        classification = np.zeros(
            (result.shape[0], result.shape[1], 3),
            dtype=np.uint8
        )

        # Strong edges = green
        classification[strong_edges] = [0, 255, 0]

        # Weak edges = yellow
        classification[weak_edges] = [255, 255, 0]

        diagnostic_title = "Edge Classification Map"

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    density = edge_density(
        result,
        edge_metric_threshold
    )

    # ---------------------------------------------------
    # MAIN IMAGE DISPLAY
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Original Image")

        st.image(
            image,
            use_container_width=True
        )

    with col2:

        st.subheader("Edge Detection Result")

        st.image(
            result,
            use_container_width=True
        )

    # ---------------------------------------------------
    # METRICS DISPLAY
    # ---------------------------------------------------

    st.subheader("Evaluation Metric")

    st.metric(
        "Edge Density (%)",
        density
    )

    st.markdown("""
    ### Interpretation

    Edge density measures the percentage of pixels whose edge response exceeds the selected threshold.

    - Low thresholds classify more pixels as edges.
    - High thresholds focus on stronger image structures.
    - High edge density may indicate excessive sensitivity or noise amplification.
    - Low edge density may indicate under-detection of image structure.
    """)
    # ---------------------------------------------------
    # DIAGNOSTIC VISUALIZATION
    # ---------------------------------------------------

    st.subheader(diagnostic_title)

    fig, ax = plt.subplots()

    if algorithm == "Sobel":

        heatmap = ax.imshow(
            magnitude,
            cmap="inferno"
        )

        plt.colorbar(
            heatmap,
            ax=ax
        )

        st.markdown(
            "(Brighter colors indicate higher gradient magnitude and stronger intensity changes)"
            )

    elif algorithm == "Laplacian":

        ax.imshow(
            gray,
            cmap="gray"
        )

        ax.imshow(
            zero_crossing,
            cmap="Reds",
            alpha=0.7
        )
        
        st.markdown(
            "(Red overlay marks detected zero-crossings of the Laplacian response)"
            )

    elif algorithm == "Canny":

        ax.imshow(classification)
        
        st.markdown(
            "(Green = strong edges | Yellow = weak edges)"
            )

    ax.axis("off")

    st.pyplot(fig)

    # ---------------------------------------------------
    # DIAGNOSTIC INTERPRETATION
    # ---------------------------------------------------

    st.subheader("Diagnostic Interpretation")

    if algorithm == "Sobel":

        st.info("""
        The heatmap visualizes gradient magnitude, which measures how strongly image intensity changes at each pixel.

        - Dark regions correspond to weak intensity changes.
        - Bright regions correspond to strong edges and sharp transitions.
        - The colorbar shows relative gradient strength values computed from horizontal and vertical derivatives.

        Larger kernels smooth noise but can reduce sensitivity to fine image details.
        """)

    elif algorithm == "Laplacian":

        st.info("""
        The red overlay marks zero-crossings of the Laplacian response.

        A zero-crossing occurs where the second derivative changes sign,
        which often corresponds to an edge boundary in the image.

        Because second derivatives are highly sensitive to noise and fine texture,
        many small intensity fluctuations can also generate zero-crossings.

        Increasing Gaussian smoothing reduces this sensitivity and produces cleaner edge structures.
        """)

    elif algorithm == "Canny":

        st.info("""
        The classification map visualizes edge strength before hysteresis thresholding.

        Edge strength is determined from gradient magnitude, which measures how strongly image intensity changes at each pixel.

        The lower and upper thresholds define decision boundaries on these gradient values:

        - Pixels below the lower threshold are suppressed.
        - Pixels between the thresholds are classified as weak edges.
        - Pixels above the upper threshold are classified as strong edges.

        During hysteresis thresholding, weak edges connected to strong edges are more likely to survive in the final Canny result.
        """)

# ---------------------------------------------------
# NO IMAGE
# ---------------------------------------------------

else:

    st.warning(
        "Please upload an image or load the built-in example."
    )