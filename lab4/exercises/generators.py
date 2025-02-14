# Generator to yield squares of numbers up to N
def generate_squares(N):
    for i in range(N + 1):
        yield i ** 2


# Generator to yield even numbers up to N
def even_numbers(N):
    for i in range(0, N + 1, 2):
        yield i



# Generator for numbers divisible by 3 and 4
def divisible_by_3_and_4(N):
    for i in range(N + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i



# Generator to yield squares between a and b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2



# Generator to yield numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
