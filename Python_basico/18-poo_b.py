from abc import ABC,abstractmethod

class BankAccount(ABC):
    def __init__ (self,owner, inicial_balance):
        self.owner = owner
        self.__balance = inicial_balance #encapsulamiento del atributo balance

    def deposit (self, amount):
        if amount >0:
            self.__balance += amount

    def _get_balance(self):
        return self.__balance
    
    def _set_balance(self, new_balance):
        if new_balance >=0:
            self.__balance = new_balance


    @abstractmethod
    def withdraw (self, amount):
        pass #Polimorfismo
        
    def check_balance (self):
        return f"El balance de la cuenta de {self.owner} es a {self.__balance}"
    

class SavingsAccount(BankAccount): # Herencia
    def withdraw(self, amount):
        penalty = amount * 0.05
        total = amount + penalty
        if total <= self._get_balance():
            self._set_balance(self._get_balance() - total)
        else:
            print ("Fondos insuficientes en la cuenta de ahorros")
                

class PayrollAccount(BankAccount): # Herencia
    def withdraw(self, amount):
        if amount<= self._get_balance():
            self._set_balance(self._get_balance() - amount)
        else:
            print( "Fondos insuficientes en la cuenta nomina")


savings = SavingsAccount("Alessandro", 3000)
payrroll = PayrollAccount("Alessandro", 3000)

savings.withdraw(1500)
payrroll.withdraw(1500)

print ("Saldo cuenta de ahorros:", savings.check_balance())
print ("Saldo cuenta nomina:", payrroll.check_balance())