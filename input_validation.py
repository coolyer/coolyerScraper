def get_integer_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        print("Invalid input. Please enter a number.")
        return