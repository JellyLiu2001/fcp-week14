#!/usr/bin/env python


#-------------------------------------------------------------------#
#                                                                   #
#                   Command-line interface                          #
#                                                                   #
#-------------------------------------------------------------------#

PROGRAM_EXPLANATION = """
Usage:
$ python roots.py COEFF1 COEFF2 ...

Find integer roots of a polynomial with integer coefficients.

Example:

Find the roots of x^4 - 3x^3 - 75x^2 + 475x - 750.

$ python roots.py 1 -3 -75 475 -750
-10
3
5
"""


def main(*arguments):
    """Main entry point for the program"""
    if not arguments:
        print(PROGRAM_EXPLANATION)
        return

    poly = parse_coefficients(arguments)
    # Convert string arguments to integer
    roots = integer_roots(poly)
    # Solve all integer roots of a polynomial.
    print_roots(roots)
    # Print the roots one per line if there are any


def parse_coefficients(arguments):
    """Convert string arguments to integer

    >>> parse_coefficients(["2", "3"])
    [2, 3]

    parameters:
        arguments: The tuple of all coefficients of the polynomial.
    
    returns:
        roots: The list of all integer roots of the polynimial with int type.
    """
    return [int(arg) for arg in arguments]


def print_roots(roots):
    """Print the roots one per line if there are any

    >>> print_roots([2, 3])
    2
    3

    parameters:
        roots: The list of all integer roots of the polynimial.
    """
    if roots:
        roots_str = [str(r) for r in roots]
        print('\n'.join(roots_str))


#-------------------------------------------------------------------#
#                                                                   #
#                      Polynomial functions                         #
#                                                                   #
#-------------------------------------------------------------------#


class BadPolynomialError(Exception):
    """Raised by polynomial routines when the polynomial is invalid.

    A valid polynomial is a list of coefficients like [1, 2, 1]

    The first (leading) coefficient must *not* be zero in a valid polynomial.
    """
    pass

def Errors(poly):
    '''Custom exception'''
    if not isinstance(poly,list):
        raise BadPolynomialError('Error: poly is not a list!')
    elif poly == []:
        pass
    elif not isinstance(poly[0],int):
        raise BadPolynomialError("Error: The first coefficient of the polynomial is not an integer!")
    elif poly[0] == 0:
        raise BadPolynomialError('Error: The first coefficient of the polynomial is zero!')


def integer_roots(poly):
    '''Solve all integer roots of the polynomial by using rational root theorem.

    >>> integer_roots([1, 2, 1])
    [-2]

    Parameters:
        poly: A list of the coefficients of the polynomial.
    
    Returns:
        true_roots: The list of all integer roots of the polynomial.
    '''
    Errors(poly)
    if poly == []:
        return []
    elif poly[-1] > 0:
        root_list=[number for number in range(-poly[-1],poly[-1]+1)]
        true_roots=[]
        for root in root_list:
            if is_root(poly,root) == True:
                true_roots.append(root)
        return true_roots
    elif poly[-1] < 0:
        root_list=[number for number in range(poly[-1],-poly[-1]+1)]
        true_roots=[]
        for root in root_list:
            if is_root(poly,root) == True:
                true_roots.append(root)
        return true_roots


def evaluate_polynomial(poly, xval):
    '''Calculates the value of the polynomial p(x) at x.

    >>> evaluate_polynomial([1,2,1],3)
    16

    Parameters:
        poly: A list of the coefficients of the polynomial.
        xval: The x value that needs to be judged whether it is the root of the polynomial.
    
    Returns:
        ans: An interger answer.
    '''
    Errors(poly)
    if len(poly) == 0:
        return 0
    else:
        power = len(poly) - 1
        ans=0
        for number in poly:
            ans += number * xval ** power
            power -= 1
        return ans
    


def is_root(poly, xval):
    '''Check if xval is the root of the polynomial poly.

    >>> is_root([1, 2, 1], 3)
    False
    >>> is_root([1, 2, 1], -1)
    True

    Parameters:
        poly: A list of the coefficients of the polynomial.
        xval: The x value that needs to be judged whether it is the root of the polynomial.
    
    Returns:
        Boolean result: True or False
    '''
    Errors(poly)
    power = len(poly) - 1
    ans=0
    for number in poly:
        ans += number * xval ** power
        power -= 1
    if ans == 0:
        return True
    else:
        return False


#-------------------------------------------------------------------#
#                                                                   #
#                           Unit tests                              #
#                                                                   #
#-------------------------------------------------------------------#


# Run these tests with pytest:
#
#    $ pytest roots.py


def test_evaluate_polynomial():
    assert evaluate_polynomial([], 1) == 0
    assert evaluate_polynomial([1], 2) == 1
    assert evaluate_polynomial([1, 2], 3) == 5
    assert evaluate_polynomial([1, 2, 1], 4) == 25

    # Invalid inputs should raise BadPolynomialError
    from pytest import raises
    raises(BadPolynomialError, lambda: evaluate_polynomial([0], 1))
    raises(BadPolynomialError, lambda: evaluate_polynomial({}, 1))
    raises(BadPolynomialError, lambda: evaluate_polynomial([[1]], 1))


def test_is_root():
    assert is_root([], 1) is True
    assert is_root([1], 1) is False
    assert is_root([1, 1], 1) is False
    assert is_root([1, 1], -1) is True
    assert is_root([1, -1], 1) is True
    assert is_root([1, -1], -1) is False
    assert is_root([1, -5, 6], 2) is True
    assert is_root([1, -5, 6], 3) is True
    assert is_root([1, -5, 6], 4) is False

    # Invalid inputs should raise BadPolynomialError
    from pytest import raises
    raises(BadPolynomialError, lambda: is_root([0], 1))
    raises(BadPolynomialError, lambda: is_root({}, 1))
    raises(BadPolynomialError, lambda: is_root([[1]], 1))


def test_integer_roots():
    # In the case of the zero polynomial every value is a root but we return
    # the empty list because we can't list every possible value!
    assert integer_roots([]) == []
    assert integer_roots([1]) == []
    assert integer_roots([1, 1]) == [-1]
    assert integer_roots([2, 1]) == []
    assert integer_roots([1, -5, 6]) == [2, 3]
    assert integer_roots([1, 5, 6]) == [-3, -2]
    assert integer_roots([1, 2, 1]) == [-1]
    assert integer_roots([1, -2, 1]) == [1]
    assert integer_roots([1, -2, 1]) == [1]
    assert integer_roots([1, -3, -75, 475, -750]) == [-10, 3, 5]

    # Invalid inputs should raise BadPolynomialError
    from pytest import raises
    raises(BadPolynomialError, lambda: integer_roots([0]))
    raises(BadPolynomialError, lambda: integer_roots({}))
    raises(BadPolynomialError, lambda: integer_roots([[1]]))


if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:]
    main(*arguments)