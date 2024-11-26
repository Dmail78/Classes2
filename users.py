import hashlib
import uuid

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.sesions = []

    def register(self, user_class, username, email, password, *args):
        print(f"Регистрация нового пользователя {username} типа {user_class} ")
        result = True 
        if len(list(filter(lambda x: x.username == username, User.users))) == 0:
            if user_class == 'User':
                temp_user = User(username, email, password)
            elif user_class == 'Customer':
                temp_user = Customer(username, email, password, args[0])
            else:
                temp_user = Admin(username, email, password, args[0])
        else:
            print("Такой пользователь существует, создайте другое имя")
            result = False
        if result:
            User.users.append(temp_user)
        return result
        
        
    def login(self, username, password):
        # Проверяем пароль и устанавливаем сессию
        temp_user  = AuthenticationService.get_user(username)
        if not temp_user is None and temp_user.check_password(temp_user.password, password):
            if len(list(filter(lambda x: x["username"] == username, self.sesions))) > 0 :
                print('Сессия уже открыта')
            else:
                token_id = str(uuid.uuid4())
                self.sesions.append({"username": username, "password": password, "token_id" : token_id})
                print(f"Сессия {token_id} открыта")
            return True
        print("Неверные имя пользователя или пароль")
        return False
       

    def logout(self):
        if len(self.sesions) > 0:
            temp = self.sesions.pop()
            print(f"Пользователь {temp["username"]} сессия {temp["token_id"]} покинул чат")
            return "Операция успешна"
        else:
            print("Больше нет открытых сессий")
            return "Ошибка"

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if len(self.sesions) > 0:
            temp = self.sesions[-1]
            print(f"Пользователь {temp["username"]} сессия {temp["token_id"]}")
            AuthenticationService.get_user(temp["username"]).get_details()
            return "Операция успешна"
        else:
            return "Ошибка"
        
    @staticmethod
    def get_user(username):
        result = None
        for u in User.users:
                if u.username == username:
                    result = u
                    break
        return result


class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
    
    @staticmethod
    def hash_password(password):
      # Преобразуем пароль в байтовую строку
        password_bytes = password.encode('utf-8')
        # Создаем объект хеш-функции SHA-256
        hash_object = hashlib.sha256()
        # Обновляем хеш-объект байтами пароля
        hash_object.update(password_bytes)
        return hash_object.hexdigest()  

    @staticmethod
    def check_password(stored_password, provided_password):
        return stored_password == User.hash_password(provided_password)

    def get_details(self):
        return f"Пользователь {type(self).__name__} {self.username}"
    
        
class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        return f"Пользователь {type(self).__name__} {self.username}"
        

class Admin(User):
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level
          
    def get_details(self):
        return f"Админ {type(self).__name__} {self.username}"

    @staticmethod
    def list_users():
        print("Cписок всех пользователей")
        print(*[u.username for u in User.users], sep="\n")
        
    @staticmethod
    def delete_user(username):
        for u in User.users:
            if u.username == username:
                User.users.remove(u)
        
            
a_service = AuthenticationService()
a_service.register("User", "user1", "email", "123")
a_service.register("User", "user2", "email", "12356")
a_service.register("User", "user1", "email", "123") # Пользователь уже есть такой

a_service.login("user1", "123") 
a_service.login("user2", "123") #Пароль не тот 
a_service.login("user2", "12356")

a_service.logout()
a_service.logout()
a_service.logout() # Ошибка, так как нет открытых сессий

a_service.login("user1", "123") 
a_service.get_current_user() # Текущий пользователь

a_service.register("Customer", "cs1", "email", "123", "Белгород")
c_user = a_service.get_user("cs1")
print(c_user.get_details())
a_service.register("Admin", "admin", "email", "123", 5)
adminson = a_service.get_user("admin")
adminson.list_users()
adminson.delete_user("user1")
adminson.list_users() # печать без удаленного пользователя