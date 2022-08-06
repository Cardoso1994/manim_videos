#!/usr/bin/env python3

from manim import *
import numpy as np

FONT_COLOR= "#282828"
NO_TEX_FONT = "Bookerly"
# NO_TEX_FONT = "JetBrains Mono"
# NO_TEX_FONT = "JuliaMono"
TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsbsy}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath}")
TEX_TEMPLATE.add_to_preamble(r"\usepackage{mathtools}")
DM_CHANGE_COLOR = "#8F3F71"

VAL_COLOR_RIGHT = "#427B58"
VAL_COLOR_WRONG = "#B16286"
LEFT_BRACKET = '('
RIGHT_BRACKET = ')'

"""
slices of DM
1. 2:9
"""

EPSILON = r"\epsilon = 1"

class lernmatrix_1(Scene):
    """Main scene for lermatrix didactic resource."""

    def construct(self):
        """scene constructor."""
        self.camera.background_color = WHITE
        COLOR_SLICES_DM = np.array([[2, 9],
                                    [7, 14],
                                    [12, 19]])
        #################
        # introduction
        #################
        title = Text("La Lernmatrix", font=NO_TEX_FONT, slant=ITALIC,
                     color=FONT_COLOR)
        title.font_size *= 1.7
        subtitle = Text("Ejemplo 1", font=NO_TEX_FONT, color=FONT_COLOR)
        subtitle.next_to(title, DOWN)

        self.play(Write(title, scale=2), run_time=3.5)
        self.play(title.animate.shift(1.5*UP))
        self.play(Write(subtitle))
        self.wait(2)
        self.remove(title, subtitle)

        #################
        # training set
        #################
        title = Text("Conjunto de Entrenamiento", font=NO_TEX_FONT,
                     color=FONT_COLOR)
        # title.font_size *= 0.9
        training_set = MathTex(
            r"""
            \boldsymbol{x^1} = \begin{pmatrix}
            1 \\ 0 \\ 1 \\ 0 \\ 1
            \end{pmatrix}
            \boldsymbol{y^1} = \begin{pmatrix}
            1 \\ 0 \\ 0
            \end{pmatrix} &;
            \boldsymbol{x^2} = \begin{pmatrix}
            1 \\ 1 \\ 0 \\ 0 \\ 1
            \end{pmatrix}
            \boldsymbol{y^2} = \begin{pmatrix}
            0 \\ 1 \\ 0
            \end{pmatrix};
            \\
            \boldsymbol{x^3} = \begin{pmatrix}
            1 \\ 0 \\ 1 \\ 1 \\ 0
            \end{pmatrix}
            & \mbox{ }
            \boldsymbol{y^3} = \begin{pmatrix}
            0 \\ 0 \\ 1
            \end{pmatrix}
            """,
            tex_template=TEX_TEMPLATE, color=FONT_COLOR)

        self.play(FadeIn(title, scale=2), run_time=1.2)
        self.play(title.animate.to_edge(UP), run_time=2)

        training_set.next_to(title, DOWN)
        self.play(FadeIn(training_set, scale=1.1), run_time=2)
        self.wait(1.5)
        self.remove(title, training_set)

        # entrenamiento
        title = Text("Fase de Entrenamiento", font=NO_TEX_FONT,
                     color=FONT_COLOR)
        title.font_size *= 1.25
        self.play(Write(title), run_time=1.5)
        self.play(title.animate.to_edge(UP), run_time=1.2)

        M = np.zeros((3, 5), dtype=int)
        X = np.array([[1, 0, 1, 0, 1],
                      [1, 1, 0, 0, 1],
                      [1, 0, 1, 1, 0]])
        Y = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

        M_str = np_to_pmatrix(M)
        M_manim = IntegerMatrix(M, left_bracket=LEFT_BRACKET,
                                right_bracket=RIGHT_BRACKET)
        M_manim.color = FONT_COLOR
        M_tex = MathTex('M = ', color=FONT_COLOR)
        M_manim.next_to(M_tex, RIGHT)
        M_group = Group(M_tex, M_manim)
        M_group.width *= 0.75
        M_group.to_edge(LEFT)

        training_set.scale(0.7)
        training_set.to_edge(RIGHT)

        self.play(FadeIn(M_group),
                  FadeIn(training_set),
                  run_time=2)
        self.wait(4)

        self.play(FadeOut(title),
                  FadeOut(M_group),
                  FadeOut(training_set),
                  run_time=1)
        self.remove(title, M_group, training_set)
        self.wait(0.8)

        # training loop
        epsilon_tex = MathTex(EPSILON, color=FONT_COLOR)
        epsilon_tex.next_to(title, DOWN)
        epsilon_tex.to_edge(RIGHT)
        epsilon_tex.shift(DOWN * 0.15)
        epsilon_tex.shift(LEFT * 0.25)
        epsilon_tex.scale(1.5)
        epsilon_tex.set_color(BLUE_E)
        for i in range(X.shape[0]):
            title = Text(f"Par asociado {i + 1}", font=NO_TEX_FONT,
                         color=FONT_COLOR)
            title.to_edge(UP)
            x_i = X[i, :]
            y_i = Y[i, :]
            x_i_tex = MathTex(r"\boldsymbol{" + f"x^{i + 1}" + "} = ",
                              color=FONT_COLOR)
            x_i_manim = IntegerMatrix(x_i.reshape((1, X.shape[1])),
                                      left_bracket=LEFT_BRACKET,
                                      right_bracket=RIGHT_BRACKET)
            x_i_manim.color = FONT_COLOR
            x_i_manim.next_to(x_i_tex, RIGHT)
            x_i_group = Group(x_i_tex, x_i_manim)

            y_i_tex = MathTex(r"\boldsymbol{" + f"y^{i + 1}" + "} = ",
                              color=FONT_COLOR)
            y_i_manim = IntegerMatrix(y_i.reshape((Y.shape[1], 1)),
                                      left_bracket=LEFT_BRACKET,
                                      right_bracket=RIGHT_BRACKET)
            y_i_manim.color = FONT_COLOR
            y_i_manim.next_to(y_i_tex, RIGHT)
            y_i_group = Group(y_i_tex, y_i_manim)

            # actual Lernmatrix training
            DM = np.zeros((Y.shape[1], X.shape[1]), dtype=int)
            rows = y_i == 1
            row_idx = np.where(rows)[0][0]
            cols_plus = x_i == 1
            cols_minus = x_i == 0
            DM[rows, cols_plus] = 1
            DM[rows, cols_minus] = -1

            # location of elements on screen
            DM_manim = IntegerMatrix(DM, left_bracket=LEFT_BRACKET,
                                     right_bracket=RIGHT_BRACKET)
            DM_manim.color = FONT_COLOR
            DM_manim.shift(DOWN)

            x_i_group.width *= 1.03
            x_i_group.next_to(DM_manim, UP)
            x_i_group.shift(0.62 * LEFT)
            y_i_group.next_to(DM_manim, LEFT)
            y_i_group.shift(0.4 * LEFT)
            y_i_group.shift(0.04 * DOWN)

            # color elements that will change during training
            DM_manim.get_rows()[row_idx].color = DM_CHANGE_COLOR
            y_i_manim.get_rows()[row_idx].color = DM_CHANGE_COLOR

            self.play(FadeIn(title),
                      FadeIn(epsilon_tex),
                      FadeIn(DM_manim, scale=1),
                      FadeIn(x_i_group),
                      FadeIn(y_i_group),
                      run_time=2)
            self.wait(2)
            self.remove(DM_manim, x_i_group, y_i_group)

            NM = M + DM
            NM_tex = MathTex(r"M &= M + \Delta M_{" + f"{i+1}" + r"} \\ &= "
                            + np_to_pmatrix(M)
                            + r" + "
                            + np_to_pmatrix(DM)
                            + r"\\ &= "
                             + np_to_pmatrix(NM),
                             tex_template=TEX_TEMPLATE, color=FONT_COLOR)
            NM_tex.shift(DOWN)
            self.play(FadeIn(NM_tex), run_time=3)
            self.wait(4)
            M = NM
            self.remove(title, NM_tex, epsilon_tex)

        title = Text("Final del entrenamiento", font=NO_TEX_FONT,
                     color=FONT_COLOR)
        title.to_edge(UP)
        M_tex = MathTex(r"M &= "
                        + np_to_pmatrix(M),
                        tex_template=TEX_TEMPLATE, color=FONT_COLOR)
        M_tex.scale(1.4)
        self.play(FadeIn(title),
                  FadeIn(M_tex),
                  run_time=2)
        self.wait(4)
        self.remove(title, M_tex)

        #######################################
        # Recuperacion. Resubstitution Error
        #######################################
        title = Text("Fase de Recuperación", font=NO_TEX_FONT,
                     color=FONT_COLOR)
        subtitle = Text("Resubstitution Error", font=NO_TEX_FONT,
                        color=FONT_COLOR)
        subtitle.font_size *= 0.85
        subtitle.next_to(title, DOWN)
        self.play(Write(title),
                  Write(subtitle), run_time=2)
        self.play(FadeOut(subtitle, shift=DOWN),
                  FadeOut(title, shift=UP), run_time=1.5)
        self.remove(subtitle, title)
        self.wait(2)

        # loop de recuperacion
        total_test = 0
        right = 0
        times = MathTex(r" \times ", color=FONT_COLOR)
        equals = MathTex(" = ", color=FONT_COLOR)
        y_omega = MathTex(r"y^{\omega} = ", color=FONT_COLOR)

        M_manim = IntegerMatrix(M, left_bracket=LEFT_BRACKET,
                                right_bracket=RIGHT_BRACKET)
        M_manim.color = FONT_COLOR
        M_manim.width *= 0.85

        cross = Cross(stroke_color=RED_C)

        patrones_probados = Variable(total_test,
                                        Text('P. probados', font=NO_TEX_FONT),
                                        var_type=Integer)
        patrones_correctos = Variable(total_test, Text('P. correctos',
                                                        font=NO_TEX_FONT),
                                        var_type=Integer)
        for i in range(X.shape[0]):
            # titulos y posicion
            subtitle = Text(f"Patrón de entrada {i + 1}", font=NO_TEX_FONT,
                            color=FONT_COLOR)
            subtitle.to_edge(UP)

            if i == 0:
                patrones_probados.width *= 0.65
                patrones_correctos.width *= 0.65
                patrones_probados.color = FONT_COLOR
                patrones_correctos.color = VAL_COLOR_RIGHT
                patrones_probados.next_to(subtitle, DOWN)
                patrones_probados.to_edge(RIGHT)
                patrones_correctos.next_to(patrones_probados, DOWN)
                self.play(Write(subtitle),
                        Write(patrones_probados),
                        Write(patrones_correctos), run_time=2)
            else:
                self.play(Write(subtitle), run_time=2)

            # patrones de prueba
            x_i = X[i].reshape(X.shape[1], 1)
            y_i = Y[i].reshape(Y.shape[1], 1)
            y_hat = M @ x_i
            y_hat_final = np.copy(y_hat)

            max_y_hat = np.max(y_hat)
            mask_max = y_hat == max_y_hat
            mask_not_max = ~mask_max
            y_hat_final[mask_max] = 1
            y_hat_final[mask_not_max] = 0

            are_equal = np.all(y_hat_final == y_i)

            # operacion M * x_i
            operation = MathTex(r"M \times " + "x^{" + str(i + 1) + "} = ",
                                color=FONT_COLOR)
            x_i_manim = IntegerMatrix(x_i, left_bracket=LEFT_BRACKET,
                                      right_bracket=RIGHT_BRACKET)
            x_i_manim.color = FONT_COLOR
            x_i_manim.width *= 0.85
            y_hat_manim = IntegerMatrix(y_hat, left_bracket=LEFT_BRACKET,
                                        right_bracket=RIGHT_BRACKET)
            y_hat_manim.color = FONT_COLOR
            y_hat_manim.width *= 0.85
            y_final_manim = IntegerMatrix(y_hat_final,
                                          left_bracket=LEFT_BRACKET,
                                          right_bracket=RIGHT_BRACKET)
            y_final_manim.color = FONT_COLOR
            y_final_manim.width *= 0.85

            operation.shift(DOWN * 1.5)
            operation.to_edge(LEFT)
            M_manim.next_to(operation, RIGHT)
            times.next_to(M_manim, RIGHT)
            x_i_manim.next_to(times, RIGHT)
            equals.next_to(x_i_manim, RIGHT)
            y_hat_manim.next_to(equals, RIGHT)

            self.play(FadeIn(operation), FadeIn(M_manim), FadeIn(times),
                      FadeIn(x_i_manim), FadeIn(equals), FadeIn(y_hat_manim),
                      run_time=2.5)
            self.wait(3)
            self.play(FadeOut(operation), FadeOut(M_manim), FadeOut(times),
                      FadeOut(x_i_manim), FadeOut(equals),
                      run_time=1.5)
            self.play(y_hat_manim.animate.to_edge(LEFT), run_time=1.5)

            self.remove(operation, x_i_manim)

            # encontrando maximo de vector resultante de M * x_i
            max_operation = MathTex(r" ; \vee_{h=1}^{p}\left[\sum_{j=1}^{n}"
                                    + r" m_{hj} \cdot x_j^{" + str(i+1)
                                    + r"}\right] = " + f"{max_y_hat}"
                                    + r"\mbox{  } \therefore",
                                    color=FONT_COLOR,
                                    tex_template=TEX_TEMPLATE)
            max_operation.next_to(y_hat_manim, RIGHT)
            max_operation.shift(RIGHT * 0.25)
            y_omega.next_to(max_operation)
            y_omega.shift(RIGHT * 0.25)
            y_final_manim.next_to(y_omega)
            group_omega = Group(y_omega, y_final_manim)
            self.play(FadeIn(max_operation), FadeIn(y_omega),
                      FadeIn(y_final_manim), run_time=1.5)
            self.wait(3)
            self.play(FadeOut(y_hat_manim), FadeOut(max_operation),
                      run_time=1.5)
            self.remove(y_hat_manim, max_operation)

            # comparando y_omega vs y_i
            y_i_manim = IntegerMatrix(y_i, left_bracket=LEFT_BRACKET,
                                      right_bracket=RIGHT_BRACKET)
            y_i_manim.width *= 0.85
            self.play(group_omega.animate.shift(LEFT * 5))
            y_i_tex = MathTex(r"y^{" + f"{i + 1}" + "} = ", color=FONT_COLOR)
            y_i_tex.next_to(group_omega, RIGHT)
            y_i_tex.shift(RIGHT)
            y_i_manim.next_to(y_i_tex, RIGHT)
            y_i_manim.color = FONT_COLOR
            self.play(FadeIn(y_i_tex), FadeIn(y_i_manim), run_time=1.5)

            # check if recall was right
            total_test += 1
            if are_equal:
                right += 1
                group_i = Group(y_i_tex, y_i_manim)
                self.play(y_omega.animate.set_fill(VAL_COLOR_RIGHT),
                          y_final_manim.animate.set_fill(VAL_COLOR_RIGHT),
                          y_i_tex.animate.set_fill(VAL_COLOR_RIGHT),
                          y_i_manim.animate.set_fill(VAL_COLOR_RIGHT),
                          run_time=0.8)
                self.play(group_omega.animate.scale(1.3),
                          group_i.animate.scale(1.3), run_time=0.8)
                self.play(group_omega.animate.scale(0.77),
                          group_i.animate.scale(0.77),
                          patrones_probados.tracker.animate.set_value(
                              total_test),
                          patrones_correctos.tracker.animate.set_value(right),
                          run_time=0.8)
            else:
                cross.next_to(y_i_manim, RIGHT)
                cross.shift(RIGHT)
                self.play(FadeIn(cross), run_time=0.8)
                patrones_probados_tracker = patrones_probados.tracker
                self.play(patrones_probados_tracker.animate.set_value(
                    total_test), run_time=0.8)
                self.wait(0.8)

            self.wait(2.5)
            self.play(FadeOut(y_i_tex), FadeOut(y_i_manim),
                      FadeOut(y_omega), FadeOut(y_final_manim),
                      FadeOut(subtitle), run_time=1.5)
            y_omega.set_fill(FONT_COLOR)

        self.remove(subtitle, y_i_tex, y_i_manim, y_omega, y_final_manim,
                    patrones_probados, patrones_correctos)
        self.wait(1)

        # resubstitution error computation
        title = Text("Desempeño de la Lernmatrix", font=NO_TEX_FONT,
                     color=FONT_COLOR)
        frac = MathTex(r"Resubstitution \mbox{  } error = "
                       + r"\frac{P. \mbox{  }correctos}{P. \mbox{  }probados}="
                       + r"\frac{" + f"{right}" + "}{"
                       + f"{total_test}" + "}="
                       + f"{right / total_test * 100:.2f}" + r"\%",
                       color=FONT_COLOR)
        frac.shift(DOWN * 0.75)
        self.play(Write(title), run_time=1.5)
        self.play(title.animate.to_edge(UP), run_time=1)
        self.play(Write(patrones_probados), Write(patrones_correctos),
                  run_time=1.5)
        self.play(FadeIn(frac), run_time=1.5)
        self.wait(10)



def np_to_pmatrix(arr):
    """
    Return the string Latex pmatrix representation of an np.array.

    Parameter
    --------
    arr : np.array
            array to be parsed to latex
    Return
    ------
    tex : string
        string pmatrix representation of an array
    """
    if len(arr.shape) > 2:
        raise ValueError('Matrix should be at most 2D')

    lines = str(arr).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{pmatrix*}[r]']
    rv += [' ' + ' & '.join(l.split()) + r'\\' for l in lines]
    # rv[-1] = rv[-1].replace(r"\\", "")
    rv += [r'\end{pmatrix*}']

    return '\n'.join(rv)
    # return rv
