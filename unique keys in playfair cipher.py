import math

# Part 1: Approximate number of possible keys
factorial_25 = math.factorial(25)
log2_factorial_25 = math.log2(factorial_25)

# Part 2: Number of effectively unique keys
symmetries = math.factorial(5) * math.factorial(5) * 2 * 4
effective_keys = factorial_25 // symmetries
log2_effective_keys = math.log2(effective_keys)

# Display results
(log2_factorial_25, log2_effective_keys)
