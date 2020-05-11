def safe_division(x, y):
    try:
        return 1.0 * x / y
    except ZeroDivisionError:
        return 0.0

def word_idx(token, sent):
    return token.i - sent.start + 1
