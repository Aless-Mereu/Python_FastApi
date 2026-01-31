class BankAccount:
    def __init__ (self,owner, inicial_balance):
        self.owner = owner
        self.__balance = inicial_balance #encapsulamiento del atributo balance

    def deposit (self, amount):
        if amount >0:
            self.__balance += amount


    def withdraw (self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return amount 
        else:
            return "Fondos insuficientes"
        
    def check_balance (self):
        return f"El balance de la cuenta de {self.owner} es a {self.__balance}"
    
account = BankAccount ("Alessandro", 1000) #Abstraccion de datos

account.deposit (500)
account.withdraw (200)
print (account.check_balance())

