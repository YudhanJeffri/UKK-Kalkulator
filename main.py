import tkinter as tk
import re

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#4dd2ff"
WHITE = "#F5F5F5"
LIGHT_BLUE = "#FFFFFF"
LIGHT_GRAY = "#FFFFFF"
LABEL_COLOR = "#000000"
DIGIT_COLOR = "#FFFFFF"


class Calculator:
    def __init__(self):
        window = self.window = tk.Tk()
        window.geometry("375x667")
        window.resizable(0, 0)
        window.title("Kalkulator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.button_frame = self.create_buttons_frame()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 3)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.create_digit_buttons()
        self.create_op_buttons()
        self.create_clear_button()
        self.create_ce_button()
        #self.create_half_button()
        self.create_remove_last_button()
        self.create_result_button()
        self.create_special_buttons()
        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

    def create_half_button(self):
        button = tk.Button(self.button_frame, text="1/2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.half)
        button.grid(row=4, column=1, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def evaluate(self):
        if self.current_expression == "Error":
            self.current_expression = ""
            self.total_expression = ""
            self.update_label()
            self.update_total_label()
        else:
            self.total_expression += self.current_expression
            self.update_total_label()
            try:
                self.current_expression = str(eval(self.total_expression))
                self.total_expression = ""
            except Exception as e:
                self.current_expression = "Error"
            finally:
                self.update_label()

    def clear_text(self):
        self.entry.delete(0, 'end')

    def create_clear_button(self):
        button = tk.Button(self.button_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_result_button()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_ce_button(self):
        button = tk.Button(self.button_frame, text="CE", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def remove_last(self):
        prev_number = self.current_expression
        if "Error" in prev_number:
            prev_number = "0"
            self.current_expression = prev_number
            self.clear()
        else:
            prev_number = prev_number[:-1]
            self.current_expression = prev_number
            self.update_label()


    def create_remove_last_button(self):
        button = tk.Button(self.button_frame, text="<", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.remove_last)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_result_button(self):
        button = tk.Button(self.button_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=4, sticky=tk.NSEW)

    # for update label

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()
    # def half(self):
    #     var = int(f"{self.current_expression}) / 2
    #     self.current_expression = var
    #     self.update_label()
    #     self.update_total_label()
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')


        return total_label, label

    def create_op_buttons(self):

        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.button_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            if self.total_expression != operator:
                i += 1
            else:
                self.current_expression = "Error"

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE
                               , borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # add function to button
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Calculator().run()
