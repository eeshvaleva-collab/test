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
    self._name = name.lower().strip()
    self._email = email.lower().strip()
    self._type = type.lower().strip()
    self.borrowed_books = {}

    if self._type not in User._USER_CONFIGS:
        raise ValueError(
            f"Invalid user type - '{type}'. Available types: {", ".join(User._USER_CONFIGS)}"
        )

    self._userId = generate_unique_id(self._email)
    self._max_books = User._USER_CONFIGS[self._type]["max_books"]
    self._time_limit = User._USER_CONFIGS[self._type]["time_limit"]

    @property
    def userId(self):
        return self.userId

    @property
    def borowed_books(self):
        return self.borrowed_books

    @property
    def canBorrow(self):
        return 

    # public abstract int getMaxBooks();
    # public abstract int getBorrowDays();
    # public abstract double getFinePerDay();
    
    # public boolean canBorrow() {
    #     return borrowedBooks.size() < getMaxBooks();
    # }



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
        self.books = {}

    