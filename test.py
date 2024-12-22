from manim import *
import numpy as np

# Preview Settings
config.pixel_height = 360       
config.pixel_width = 640        
config.frame_rate = 15          

class CorrelationAnimation(Scene):
    def construct(self):
        # Axes for clarity
        axes = Axes(
            x_range=[-4,4,1],
            y_range=[-4,4,1],
            x_length=6,
            y_length=4,
            axis_config={"stroke_color": GREY_B},
        )

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
        
        label_2d = Text("2D Multivariate Normal Distribution", font_size=24).to_edge(UP).shift(DOWN*0.8)
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
        regeneration_interval = 2  # Increase this to slow flickering more
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
