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
    def __init__(self, name, email, user_type):
        self._name = name
        self._email = email
        self._user_type = user_type
        self._borrowed_books = set()

        if self._user_type not in User._USER_CONFIGS:
            raise ValueError(
                f"Invalid user type - '{user_type}'. Available types: {', '.join(User._USER_CONFIGS)}"
            )

        self._user_id = generate_unique_id(self._email)
        self._max_books = User._USER_CONFIGS[self._user_type]["max_books"]
        self._time_limit = User._USER_CONFIGS[self._user_type]["time_limit"]

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_type(self):
        return self._user_type

    @property
    def borrowed_books(self):
        return self._borrowed_books.copy()

    @property
    def max_books(self):
        return self._max_books
    
    @property
    def time_limit(self):
        return self._time_limit

    @property
    def can_borrow(self):
        return len(self.borrowed_books) < self.max_books

    def take_book(self, book):
        if not self.can_borrow:
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

class Record:
    def __init__(self, user_id, isbn, borrowed_date, time_limit):
        self.user_id = user_id
        self.isbn = isbn
        self.borrowed_date = borrowed_date
        self.time_limit = time_limit

    @property
    def is_overdue(self):
        return (datetime.now() - self.borrowed_date).days > self.time_limit if self.borrowed_date else False

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self._borrowed_date = None

        self._isbn = generate_unique_id(f"{self.author}{self.title}{datetime.now()}")

    @property
    def isbn(self):
        return self._isbn
    
    @property
    def is_vacant(self):
        return self._borrowed_date is None

    @property
    def borrowed_date(self):
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
        self._records = {}

    @property
    def users(self):
        return self._users.copy()

    @property
    def books(self):
        return self._books.copy()

    def register_user(self, name, email, user_type):
        if any(user.email == email for user in self.users.values()):
                raise ValueError(f"user with email '{email}' has been alreade registered")

        new_user = User(name = name, email = email, user_type = user_type)
        self._users[new_user.user_id] = new_user

        print(f"User {name} has been succesfully regirestered in the library")
        return new_user.user_id

    def find_user(self, user_id):
        user = self._users.get(user_id) 
        if user is None:
            print("There is no such user in the library")
        else:
            print("User is registered in the library")
        
        return user
    
    def add_book(self, title, author, genre="other"):
        new_book = Book(title, author, genre)
        self._books[new_book.isbn] = new_book
        print("Book has been added to the library")

    def find_book(self, isbn):
        book = self._books.get(isbn) 
        if book is None:
            print("There is no such book in the library")
        else:
            print("Book is present in the library")
        
        return book

    def remove_book(self, isbn):
        if isbn in self._books:
            if self._books[isbn].is_vacant:
                del self._books[isbn]
                print("The book has been removed")
            else:
                raise ValueError(f"This book is currently borrowed")
        else:
            raise ValueError(f"There is no book with id {isbn}")

    def borrow_book(self, user_id, isbn):
        user = self.find_user(user_id)
        if not user:
            raise ValueError(f"There is no such user in the library")
        book = self.find_book(isbn)
        if not book:
            raise ValueError(f"There is no such book in the library")
        
        if self.is_user_debtor(user_id):
            raise ValueError(f"User {user.name} is a debtor! Cannot borrow more books!!!")
        user.take_book(book)
        self._records[isbn] = Record(user.user_id, book.isbn, book.borrowed_date, user.time_limit)

    def is_user_debtor(self, user_id):
        return any(record.user_id == user_id and record.is_overdue for record in self._records.values())

    def return_book(self, user_id, isbn):
        user = self.find_user(user_id)
        book = self.find_book(isbn)
        if user and book:
            user.return_book(book)
            del self._records[isbn]

    def get_overdue_books(self):
        overdue_books = []
        for isbn, record in self._records.items():
            if record.is_overdue:
                overdue_books.append(record)
        return overdue_books


    def search_books(self, query):
        if not query:
            return []

        matched_books = [book for book in self._books.values() if query in book.title or query in book.author or query in book.genre]
        
        if matched_books:
            print(f"Found {len(matched_books)} book(s) for query '{query}':")
            for book in matched_books:
                status = "available" if book.is_vacant else "borrowed"
                print(f" - {book.title} by {book.author} [{status}]")
        else:
            print(f"No books matched your query '{query}'.")

        return matched_books
