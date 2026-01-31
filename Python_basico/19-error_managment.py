
def divide_number():
    try:
        a = int(input("Enter the numerator: "))
        b = int(input("Enter the denominator: "))
        result = a / b
        print(f"The result of {a} divided by {b} is {result}")
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except ValueError:
        print("Error: Invalid input. Please enter numeric values.")    
    except Exception as error:
        print(f"An error occurred: {error}")
    else:
        pass
    finally:
        print("Division performed successfully.")       
   

divide_number()
