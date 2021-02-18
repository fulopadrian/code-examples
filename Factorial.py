"""
Faktoriális
"""
def factorial_loop(n):
    F = n
    for i in range(1, n):
        F = F * i

    return F

def factorial_recursive(n):
    if n == 1:
        return n
    else:
        return n * factorial_recursive(n-1)


print(factorial_recursive(5))
