HW_SOURCE_FILE=__file__


def num_eights(x):
    """Returns the number of times 8 appears as a digit of x.

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AugAssign'])
    True
    """
    if x == 0:
        return 0
    elif x % 10 == 8:
        return 1 + num_eights(x // 10)
    else:
        return num_eights(x // 10)

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(8)
    8
    >>> pingpong(10)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    -2
    >>> pingpong(30)
    -2
    >>> pingpong(68)
    0
    >>> pingpong(69)
    -1
    >>> pingpong(80)
    0
    >>> pingpong(81)
    1
    >>> pingpong(82)
    0
    >>> pingpong(100)
    -6
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    def is_switch(k):
        return k % 8 == 0 or '8' in str(k)

    """
    这个版本使用了一个辅助函数helper，它接受当前的数值k、方向direction和计数器count，
    然后根据乒乓规则递归调用自己，直到计数器达到n。
    """
    def helper(k, direction, count):
        if count == n:
            return k
        return helper(k + direction, -direction if is_switch(count+1) else direction, count + 1)

    return helper(1, 1, 1)








def missing_digits(n):
    """Given a number a that is in sorted, increasing order,
    return the number of missing digits in n. A missing digit is
    a number between the first and last digit of a that is not in n.
    >>> missing_digits(1248) # 3, 5, 6, 7
    4
    >>> missing_digits(1122) # No missing numbers
    0
    >>> missing_digits(123456) # No missing numbers
    0
    >>> missing_digits(3558) # 4, 6, 7
    3
    >>> missing_digits(35578) # 4, 6
    2
    >>> missing_digits(12456) # 3
    1
    >>> missing_digits(16789) # 2, 3, 4, 5
    4
    >>> missing_digits(19) # 2, 3, 4, 5, 6, 7, 8
    7
    >>> missing_digits(4) # No missing numbers between 4 and 4
    0
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'missing_digits', ['While', 'For'])
    True
    """
    def count_missing_digits(first, last):
        if first > last:
            return 0
        elif str(first) not in str(n):
            return 1 + count_missing_digits(first + 1, last)
        else:
            return count_missing_digits(first + 1, last)

    # Extract the first and last digits of n
    first_digit = int(str(n)[0])
    last_digit = int(str(n)[-1])

    # Call the recursive helper function
    return count_missing_digits(first_digit, last_digit)


def next_largest_coin(coin):
    """Return the next coin. 
    >>> next_largest_coin(1)
    5
    >>> next_largest_coin(5)
    10
    >>> next_largest_coin(10)
    25
    >>> next_largest_coin(2) # Other values return None
    """
    if coin == 1:
        return 5
    elif coin == 5:
        return 10
    elif coin == 10:
        return 25


def count_coins(total):
    """Return the number of ways to make change for total using coins of value of 1, 5, 10, 25.
    >>> count_coins(15)
    6
    >>> count_coins(10)
    4
    >>> count_coins(20)
    9
    >>> count_coins(100) # How many ways to make change for a dollar?
    242
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_coins', ['While', 'For'])                                          
    True
    """
    coin_values = [25, 10, 5, 1]

    def count_ways(amount, coin_index):
        if amount == 0:
            return 1  # One way to make change: no remaining amount

        if amount < 0 or coin_index == len(coin_values):
            return 0  # No way to make change

        current_coin = coin_values[coin_index]
        use_current_coin = count_ways(amount - current_coin, coin_index)
        skip_current_coin = count_ways(amount, coin_index + 1)

        return use_current_coin + skip_current_coin

    return count_ways(total, 0)


from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return lambda n: (lambda f: f(f))(lambda f: lambda x: 1 if x == 1 else mul(x, f(f)(sub(x, 1))))(n)

