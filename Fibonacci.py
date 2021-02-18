"""
Fibonacci
"""

def fibonacci_recursive(n):
    if n == 0 or n == 1:
        return n
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_loop(n):
    F = 0
    prev = 1
    next = 0
    for i in range(n):
        next = F + prev
        prev = F
        F = next
        print(F)

    return

fibonacci_recursive(10)
