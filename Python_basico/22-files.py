try:
    with open("test.txt", "w") as my_file:
        text = my_file.write("\nNew line added to the file.")

    with open("test.txt", "r") as my_file:
        print(my_file.readlines())

    with open ('test.txt', 'r+') as my_file: 
        print(my_file.readlines())
        my_file.write("\nAnother new line added.")

    with open("test.txt", "a") as my_file:
        text = my_file.write("\n1234.")
        print(text) # Number of characters written
    

except FileNotFoundError:
    print("The file does not exist.")        
except Exception as e:
    print(f"An error occurred: {e}")