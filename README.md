# Multivariate Normal Distribution Visualizer

This project visualizes the progression from a 1D normal distribution to 2D and 3D multivariate normal distributions using the Manim animation library. It was created as a visualization tool for a class Mohamed Yossri attended at the Faculty of Computer and Data Science, Alexandria University.

## Purpose
The project aims to help students better understand the concepts of multivariate normal distributions by visually exploring the relationship between dimensions, correlation, and density functions.

### What is a Multivariate Normal Distribution?
A multivariate normal distribution is a generalization of the one-dimensional (univariate) normal distribution to higher dimensions. It is characterized by:

1. **Mean vector (\(\mu\))**: The central location of the distribution.
2. **Covariance matrix (\(\Sigma\))**: Represents the shape, spread, and correlation between variables.

The probability density function for a multivariate normal distribution is given as:
\[
    f(\mathbf{x}) = \frac{1}{(2\pi)^{n/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x} - \mu)^T \Sigma^{-1} (\mathbf{x} - \mu)\right)
\]

### Why is it Useful?
- **Data Analysis**: Used to model and understand relationships between multiple variables.
- **Machine Learning**: Forms the foundation for many probabilistic models.
- **Signal Processing**: Analyzes signals with multiple correlated variables.

---

## Features

### 1D Normal Distribution
- Visualizes the probability density function (PDF) for a normal distribution.
- Highlights mean (\(\mu\)) and standard deviation (\(\sigma\)).

### 2D Multivariate Normal Distribution
- Plots uncorrelated and correlated 2D distributions.
- Displays an evolving scatter plot and ellipse to represent the covariance structure.

### 3D Multivariate Normal Distribution
- Visualizes a 3D scatter plot of correlated data points.
- Includes a semi-transparent sphere to represent the contour of the distribution.

---

## Code Overview

### Requirements
This project uses the following libraries:
- **Manim**: For creating animations.
- **NumPy**: For numerical computations and data generation.
- **SciPy**: For probability density functions.

### Key Classes and Functions
1. **`NormalToMultivariate3D`**: The main class responsible for visualizing the progression from 1D to 3D distributions.
2. **`Axes`**: Sets up coordinate axes for 1D and 2D visualizations.
3. **`get_correlated_points(rho)`**: Generates correlated 2D data points based on a correlation coefficient \(\rho\).
4. **`set_camera_orientation()`**: Configures the 3D camera view.

---

## Running the Animation

To run the animation, use the following command:
```bash
manim -pql main.py NormalToMultivariate3D
```
### Explanation:
- **`-pql`**: Sets the preview and low-quality rendering mode. For production, replace with `-pqh` for high quality.
- **`main.py`**: The Python file containing the script.
- **`NormalToMultivariate3D`**: The class responsible for the visualization.

---

## Visualization Highlights
### 1D Distribution
- A standard normal distribution with a mean of 0 and a standard deviation of 1.
- Formula displayed alongside the graph for better understanding.

### 2D Distribution
- Showcases how correlation impacts data points.
- Smooth transitions between no correlation and high correlation (\(\rho = 0.9\)).

### 3D Distribution
- Demonstrates a 3D multivariate normal distribution with a specific covariance structure.
- Camera rotates for dynamic visualization.

---

## Future Improvements
- Add interactive controls for live demonstrations.
- Include detailed annotations explaining the math and statistics behind each step.

---

## Credits
This project was created by Mohamed Yossri as part of a class project at Alexandria University.
