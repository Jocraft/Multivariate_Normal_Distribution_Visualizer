from manim import *
import numpy as np
from scipy.stats import norm, multivariate_normal

# # Preview Settings
# config.pixel_height = 360       
# config.pixel_width = 640        
# config.frame_rate = 15          

# Production Settings
config.pixel_height = 720
config.pixel_width = 1280
config.frame_rate = 30

class NormalToMultivariate3D(ThreeDScene):
    def construct(self):
        # Create streamlines as background
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1.5)
        
        # Step 0: Add intro text fixed to the screen
        intro_text = Text("Exploring Multivariate Normal Distributions: From 1D to 3D", font_size=28)
        self.add_fixed_in_frame_mobjects(intro_text)
        self.play(Write(intro_text))
        self.wait(2)
        
        # Replace intro text with a fixed name label
        my_name = Text("Made by Mohamed Yossri", font_size=24)
        self.play(Transform(intro_text, my_name))
        self.wait(1)
        self.play(intro_text.animate.to_corner(DL).scale(0.677))
        self.play(FadeOut(stream_lines))
        stream_lines.end_animation()

        # Step 1: Set up the axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"color": WHITE},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="Density")
        
        # Generate the 1D normal distribution data points
        mean_1d = 0
        std_1d = 1
        x_vals = np.linspace(-3, 3, 100)
        y_vals = norm.pdf(x_vals, mean_1d, std_1d)
        
        # Create the graph of the normal distribution curve
        one_d_graph = axes.plot_line_graph(x_values=x_vals, y_values=y_vals, line_color=BLUE)
        
        # Label for 1D distribution
        label_1d = Text("1D Normal Distribution", font_size=24).to_edge(UP)
        formula_1D = MathTex(
            r"f(x) = \frac{1}{\sqrt{2 \pi \sigma^2}}",
            r"\exp\left(-\frac{(x - \mu)^2}{2 \sigma^2}\right)"
        )
        formula_1D.set_color_by_tex_to_color_map({"\\mu": YELLOW,"\\sigma": GREEN})


          
        # Adjust the position of the formula on screen
        formula_1D.scale(0.5).to_edge(LEFT)
        
        # Display the 1D distribution with axes and label
        self.play(Create(axes), Write(label_1d), Create(labels),Write(formula_1D))
        self.play(Create(one_d_graph),run_time=2.5)

        # Add mean and std dev in 1D
        mean_line = DashedLine(axes.c2p(0, 0), axes.c2p(0, norm.pdf(0, mean_1d, std_1d)), color=YELLOW)
        std_dev_line1 = DashedLine(axes.c2p(-1, 0), axes.c2p(-1, norm.pdf(-1, mean_1d, std_1d)), color=GREEN)
        std_dev_line2 = DashedLine(axes.c2p(1, 0), axes.c2p(1, norm.pdf(1, mean_1d, std_1d)), color=GREEN)

        self.play(Create(mean_line), Create(std_dev_line1), Create(std_dev_line2))
        self.wait(1.5)
        self.play(FadeOut(mean_line), FadeOut(std_dev_line1), FadeOut(std_dev_line2))
        self.play(FadeOut(one_d_graph), FadeOut(label_1d), FadeOut(axes), FadeOut(labels), FadeOut(formula_1D))



        # Step 2: Transition to 2D Multivariate Normal Distribution
        # Axes for clarity
        axes = Axes(
            x_range=[-4,4,1],
            y_range=[-4,4,1],
            x_length=6,
            y_length=4.5,
            axis_config={"stroke_color": GREY_B},
        )
        # Add arrows to both ends of the x-axis and y-axis
        axes.x_axis.add_tip(tip_length=0.2, at_start=True)
        axes.y_axis.add_tip(tip_length=0.2, at_start=True)
        self.play(Create(axes))
        
        mean_2d = np.array([0,0,0])
        cov_initial_2d = np.array([[1,0],[0,1]])
        
        # Points with no correlation
        points_uncorrelated_data = np.random.multivariate_normal(mean_2d[:2], cov_initial_2d, 300)
        scatter_uncorrelated = VGroup(*[
            Dot(point=axes.coords_to_point(*p), radius=0.03, color=BLUE) for p in points_uncorrelated_data
        ])
        
        formula_2D = MathTex(
            r"f(x, y) = \frac{1}{2 \pi \sigma_X \sigma_Y \sqrt{1 - \rho^2}}",
            r"\exp \left( -\frac{1}{2(1 - \rho^2)}",
            r"\left( \frac{(x - \mu_X)^2}{\sigma_X^2}",
            r"- 2 \rho \frac{(x - \mu_X)(y - \mu_Y)}{\sigma_X \sigma_Y}",
            r"+ \frac{(y - \mu_Y)^2}{\sigma_Y^2} \right) \right)",
            tex_to_color_map={"\\rho": RED}
        )
        formula_2D.scale(0.5).to_edge(UP)
        
        label_2d = Text("2D Multivariate Normal Distribution", font_size=24).to_edge(UP)
        legend = Text("No Correlation", font_size=16).next_to(axes, RIGHT, buff=0.5)
        
        self.play(Write(formula_2D))
        self.wait(1.5)
        
        self.play(
            Transform(formula_2D, scatter_uncorrelated),
            Write(label_2d), 
            Write(legend)
        )
        self.wait(1.5)
        
        # Setup for correlation
        rho_tracker = ValueTracker(0.0)
        
        def get_cov(rho):
            return np.array([
                [1, rho],
                [rho, 1]
            ])
        
        # We will throttle the random generation by caching
        # and only regenerate every N frames
        regeneration_interval = 3  # Increase this to slow flickering more
        frame_count = [0]  # Using a list for mutability in the nested function
        cached_data = None

        def get_correlated_points(rho_value):
            nonlocal cached_data
            # Increment frame count
            frame_count[0] += 1

            # Only re-generate after certain intervals
            if cached_data is None or frame_count[0] % regeneration_interval == 0:
                cov = get_cov(rho_value)
                data = np.random.multivariate_normal(mean_2d[:2], cov, 300)
                cached_data = data
            else:
                data = cached_data

            return VGroup(*[
                Dot(point=axes.coords_to_point(*p), radius=0.03, color=RED) for p in data
            ])
        
        def get_ellipse(rho_value):
            lam1 = 1 + rho_value
            lam2 = 1 - rho_value
            width = 2*np.sqrt(lam1)
            height = 2*np.sqrt(lam2)
            e = Ellipse(width=width, height=height, color=YELLOW)
            e.move_to(axes.coords_to_point(0,0))
            e.rotate(PI/4)
            return e
        
        # Create static correlated points and ellipse at rho=0 (which should look the same as no correlation)
        correlated_points_static = get_correlated_points(0.0)
        ellipse_static = get_ellipse(0.0)
        
        legend_with_correlation = Text("With Correlation", font_size=16).move_to(legend.get_center())
        rho_label = Text(f"ρ = {0.00:.2f}", font_size=24, color=RED).next_to(legend_with_correlation, DOWN)
        
        # Transform to the static correlated points and ellipse (which look like a circle at rho=0)
        self.play(
            Transform(formula_2D, correlated_points_static, run_time=2),
            Transform(legend, legend_with_correlation, run_time=2),
            Create(ellipse_static, run_time=2),
            FadeIn(rho_label),
        )
        self.wait(0.5)
        
        # Now that we are at rho=0 but with the "With Correlation" scene, 
        # we remove the static objects and add always_redraw versions.
        self.remove(formula_2D, ellipse_static, rho_label)
        
        correlated_points_dynamic = always_redraw(lambda: get_correlated_points(rho_tracker.get_value()))
        ellipse_dynamic = always_redraw(lambda: get_ellipse(rho_tracker.get_value()))
        rho_label_dynamic = always_redraw(lambda: 
            Text(f"ρ = {rho_tracker.get_value():.2f}", font_size=24, color=RED)
            .next_to(legend_with_correlation, DOWN)
        )
        
        self.add(correlated_points_dynamic, ellipse_dynamic, rho_label_dynamic)
        
        # Animate rho changing from 0 to 0.9 (now always_redraw is active)
        self.play(rho_tracker.animate.set_value(0.9), run_time=4)
        self.wait(2)

        # Fade everything out
        self.play(
            FadeOut(ellipse_dynamic), 
            FadeOut(label_2d), 
            FadeOut(legend), 
            FadeOut(rho_label_dynamic), 
            FadeOut(axes), 
            FadeOut(correlated_points_dynamic)
        )
        self.wait()
        


        # Transition from 2D to 3D - fade out 2D scatter and labels
        # Step 4: Display a 3D Multivariate Normal Distribution
        mean_3d = np.array([0, 0, 0]) 
        cov_3d = np.array([[1, 0.8, 0.6], [0.8, 1, 0.4], [0.6, 0.4, 1]])  # Correlated 3D covariance matrix
        points_3d = np.random.multivariate_normal(mean_3d, cov_3d, 300)

        # Convert points to 3D dots
        scatter_3d = VGroup(*[Dot3D(point=point, radius=0.05, color=BLUE) for point in points_3d])

        # Set the 3D camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        label_3d = Text("3D Multivariate Normal Distribution", font_size=24).to_edge(UP)

        # Make the text fixed in the frame so it doesn't move with the camera
        self.add_fixed_in_frame_mobjects(label_3d)
            
        # Create a transparent sphere to represent the outer contour
        sphere = Sphere(radius=2, color=YELLOW).move_to(mean_3d)
        sphere.set_opacity(0.3)  # Set opacity with method instead of keyword

        # Show 3D scatter plot and sphere
        self.play(Write(label_3d))
        self.play(Create(sphere), Create(scatter_3d),run_time=2.5)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5.5)

        # Fade out all elements
        self.play(FadeOut(scatter_3d), FadeOut(sphere), FadeOut(label_3d))
