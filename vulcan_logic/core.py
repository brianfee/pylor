""" The vulcan-logic core. """

import copy

class Logic:
    """ A logic string container. """

    def __init__(self, logic_str=None, weight=None):
        """ Logic class initialization. """

        self.__evaluators = ['==', '!=', '<>',
                             '>=', '<=', '~=',
                             '>', '<', '~', '=']

        self.__logic_str = logic_str
        self.__logic_matrix = None
        self.__weight = None

        self.logic = logic_str
        self.weight = weight



    def __repr__(self):
        return self.to_eval_string()



    def __str__(self):
        """ Prints the __logic_matrix in a readable format. """
        print_str = ''
        for row in self.__logic_matrix:
            print_str += row['left'] + ' '
            print_str += row['eval'] + ' '
            print_str += row['right'] + '\n'
        return print_str[:-1] # Trim final newline



    def _set_weight(self, weight=None):
        """ Calculates the weight of the Logic string.

        By default, Logic weight is calculated as the number of equations
        within the logic string. Future versions should allow field names
        to contribute varying weights.
        """

        self.__weight = len(self.__logic_matrix) if weight is None else weight



    @property # weight(self)
    def weight(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__weight



    @weight.setter
    def weight(self, weight):
        return self._set_weight(weight)



    @property # logic(self)
    def logic(self):
        """ Gets or sets the weight of the Logic String. """
        return self.__logic_matrix



    @logic.setter
    def logic(self, logic):
        """ Takes a logic string and expands it into an n x 3 matrix. """

        equations = [equation.strip() for equation in logic.split(',')]
        equations_matrix = []
        for equation in equations:
            equations_matrix.append(self.split_equation(equation))

        self.__logic_matrix = equations_matrix



    def eval(self, dictionary=None):
        """ Evaluates logic equations.

        Accepts a dictionary as an argument. If no dictionary is
        provided, logic equations are evaluated at without any
        replacement.
        """

        if dictionary is not None:
            logic = self.replace_variables(dictionary)
        else:
            logic = self.__logic_matrix

        for row in logic:
            row['validity'] = False

            if row['eval'] == '==' and row['left'] == row['right']:
                row['validity'] = True

            elif row['eval'] == '!=' and row['left'] != row['right']:
                row['validity'] = True

            elif row['eval'] == 'in' and row['left'] in row['right']:
                row['validity'] = True

            elif row['eval'] == '>=' and row['left'] >= row['right']:
                row['validity'] = True

            elif row['eval'] == '<=' and row['left'] <= row['right']:
                row['validity'] = True

            elif row['eval'] == '>' and row['left'] > row['right']:
                row['validity'] = True

            elif row['eval'] == '<' and row['left'] < row['right']:
                row['validity'] = True

            else:
                row['validity'] = None

        for row in logic:
            if not row['validity'] or row['validity'] is None:
                return False

        return True



    def replace_variables(self, dictionary):
        """ Replaces variables within an equation with values from a dict. """

        logic = copy.deepcopy(self.__logic_matrix)
        for row in logic:
            for key, value in dictionary.items():
                if row['left'] == key:
                    row['left'] = value

                if row['right'] == key:
                    row['right'] = value

        return logic



    def split_equation(self, equation):
        """ Splits an equation into a dict of its parts. """

        eq_dict = {'eval': None, 'left': None, 'right': None}

        for evaluator in self.__evaluators:
            if evaluator in equation:
                left_end = equation.find(evaluator)
                right_start = left_end + len(evaluator)
                eq_dict['eval'] = evaluator
                eq_dict['left'] = equation[:left_end].strip()
                eq_dict['right'] = equation[right_start:].strip()
                break

        if eq_dict['eval'] == '<>':
            eq_dict['eval'] = '!='

        elif eq_dict['eval'] in ['~=', '~']:
            eq_dict['eval'] = 'in'
            old_left = eq_dict['left']
            eq_dict['left'] = eq_dict['right']
            eq_dict['right'] = old_left

        elif eq_dict['eval'] == '=':
            eq_dict['eval'] = '=='

        return eq_dict



    def to_eval_string(self):
        """ Converts the logic matrix into a string for eval(). """

        eval_string = None if not self.__logic_matrix else ''

        for i, row in enumerate(self.__logic_matrix):
            if i > 0:
                eval_string += ' and '

            eval_string += (row['left'] + ' ' +
                            row['eval'] + ' ' +
                            row['right'])

        return eval_string
