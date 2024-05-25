def truncate(number, n_digits: int = 1) -> float:
    '''
    :param number: real number ℝ
    :param n_digits: Maximum number of digits after the decimal point after truncation
    :return: truncated floating point number with at least one digit after decimal point
    '''
    decimal_index = str(number).find('.')
    if decimal_index == -1:
        return float(number)
    else:
        return float(str(number)[: decimal_index + n_digits + 1])
