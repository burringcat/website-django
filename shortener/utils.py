encoded_ascii_numbers = list(range(48, 58)) + \
                        list(range(65, 91)) + list(range(97, 123)) + [95, 126]
encoded_ascii_counts = len(encoded_ascii_numbers)


def decimal2encoded(num):
    result = []
    while num >= 1:
        remainder = int(num % encoded_ascii_counts)
        encoded_number = encoded_ascii_numbers[remainder]
        num /= encoded_ascii_counts
        result.append(chr(encoded_number))
    return ''.join(result[::-1])


def encoded2decimal(num):
    result = 0
    for i, c in enumerate(reversed(num)):
        base = encoded_ascii_numbers.index(ord(c))
        result += base * (encoded_ascii_counts ** i)
    return result