from GUI import*
# Utilities imports

import re

# allowed operators in a program
operators = [
    'x',
    '/',
    '+',
    '*',
    '^',
    '-'
]

# converstion string as input from user to mathematical function
replacements = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'sqrt': 'np.sqrt',
    '^': '**',
}


def validation(equation):
    # find all words and check if all are allowed:
    equation = equation.lower()
    equation = equation.replace(" ", "")
    for word in re.findall('[a-zA-Z_]+', equation):
        if word not in operators:
            raise ValueError(
                f"Function of 'x' only allowed ,e.g: 5*x^3 + 2*x. \n Supported Operators: {', '.join(operators)}"
            )
    for old, new in replacements.items():
        equation = equation.replace(old, new)
    if "x" not in equation:
        equation = f"{equation}+0*x"

    # TODO : rest of validation ==> Exp Sin Cos
    def func(x):
        return eval(x)

    return func
