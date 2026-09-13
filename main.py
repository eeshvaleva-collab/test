from datetime import datetime
from utils import generate_unique_id


class User:
    _USER_CONFIGS = {
        "student": {
            "max_books": 3,
            "time_limit": 14,
        },
        "faculty": {
            "max_books": 10,
            "time_limit": 30,
        },
        "guest": {
            "max_books": 1,
            "time_limit": 7,
        },
    }
    def __init__(self, name, email, type):
        self._name = name
        self._email = email
        self._type = type
        self._borrowed_books = set()

        if self._type not in User._USER_CONFIGS:
            raise ValueError(
                f"Invalid user type - '{type}'. Available types: {", ".join(User._USER_CONFIGS)}"
            )

        self._userId = generate_unique_id(self._email)
        self._max_books = User._USER_CONFIGS[self._type]["max_books"]
        self._time_limit = User._USER_CONFIGS[self._type]["time_limit"]

    @property
    def userId(self):
        return self._userId

    @property
    def borrowed_books(self):
        return self._borrowed_books

    @property
    def max_books(self):
        return self._max_books
    
    @property
    def time_limit(self):
        return self._time_limit

    @property
    def canBorrow(self):
        return len(self.borrowed_books) < self.max_books

    @property
    def is_debtor(self):
        current_time = datetime.now()
        return any((current_time - book.borrowed_date).days > self.time_limit for book in borrowed_books)

    def take_book(self, book):
        if self.is_debtor:
            raise ValueError(
                f"You can't take any books. You are debtor!!!!!!!!!"
            )
        if self.canBorrow:
            raise ValueError(
                f"Max limit exeeded. You can't take any new books. You should return at least one"
            )
        book.borrow_book()
        self._borrowed_books.add(book.isbn)
    
    def return_book(self, book):
        if book.isbn not in self._borrowed_books:
            raise ValueError(
                f"You can't return this book. You don't have it"
            )
        book.return_book()
        self._borrowed_books.remove(book.isbn)


class Book:
    def __init__(self, title, author):
        self.title = title.lower().strip()
        self.author = author.lower().strip()
        self._borrowed_date = None

        self._isbn = generate_unique_id(f"{self.author}{self.title}{datetime.now()}")

    @property
    def isbn(self):
        return self._isbn
    
    @property
    def is_vacant(self):
        return self._borrowed_date is None

    @property
    def borrowed_date(self)
        return self._borrowed_date

    def borrow_book(self):
        if not self.is_vacant:
            raise ValueError(f"This book '{self.title}' is not available!")
        self._borrowed_date = datetime.now()

    def return_book(self):
        if self.is_vacant:
            return
        self._borrowed_date = None
        
class Library:
    def __init__(self):
        self._users = {}
        self._books = {}

    @property
    def users(self):
        return self._users

    def register_user(self, name, email, type):
        email_norm = email.strip().lower()
        type_norm = type.strip().lower()
        name.norm = name.strip().lower()

        if any(user.email == email_normalized for user in self.users.values()):
                raise ValueError(f"user with email {email_norm} has been alreade registered")

        new_user = User(name = name_norm, email = email_norm, type = type_norm)
        self._users[new_user.id] = new_user

        print(f"User {name} has been succesfully regirestered in the library")

    def find_user(user_id):
        user = self._users.get(user_id) 
        if user is None:
            print("There is no such user  in the library")
        else:
            print("User is registered in the library")
        
        return user
    

    