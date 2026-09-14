from classes import Library

class LibraryConsole:
    def __init__(self, library_instance):
        self.library = library_instance

    def run(self):
        while True:
            self.show_menu()

            match input("Enter option: ").strip():
                case "1":
                    self.book_menu()
                case "2":
                    self.user_menu()
                case "3":
                    self.borrowing_menu()
                case "0":
                    break
                case _:
                    print("Invalid option")

    @staticmethod
    def show_menu():
        print("""
=== Library Management ===
1. Book Management
2. User Management
3. Borrowing Operations
0. Exit
""")

    @staticmethod
    def normalize(prompt):
        return input(prompt).strip().lower()

    def book_menu(self):
        print("""
--- Book Management ---
1. Add Book
2. Remove Book
3. Search Books
0. Back
""")
        match input("Enter option: ").strip():
            case "1":
                self.add_book()
            case "2":
                self.remove_book()
            case "3":
                self.search_books()
            case "0":
                return
            case _:
                print("Invalid option")

    def add_book(self):
        title = self.normalize("Enter title: ")
        author = self.normalize("Enter author: ")
        genre = self.normalize("Enter genre: ")

        try:
            isbn = self.library.add_book(title, author, genre)
            print(f"Book has been added to the library with ISBN {isbn}")
        except ValueError as error:
            print(f"Failed to add book: {error}")

    def remove_book(self):
        isbn = self.normalize("Enter Book ISBN: ")

        try:
            self.library.remove_book(isbn)
            print("Book removed")
        except ValueError as error:
            print(f"Failed to remove book: {error}")

    def search_books(self):
        query = self.normalize("Enter search query: ")
        matched_bookes = self.library.search_books(query)
        if matched_bookes:
            print(f"Found {len(matched_books)} book(s) for query '{query}':")
            for book in matched_books:
                status = "available" if book.is_vacant else "borrowed"
                print(f"• {book.isbn} {book.title} by {book.author} [{status}]")
        else:
            print(f"No books matched your query '{query}'.")

    def user_menu(self):
        print("""
--- User Management ---
1. Register User
2. Find User
0. Back
""")
        match input("Enter option: ").strip():
            case "1":
                self.register_user()
            case "2":
                self.find_user()
            case "0":
                return
            case _:
                print("Invalid option")
    def register_user(self):
        name = self.normalize("Enter user name: ")
        email = self.normalize("Enter user email: ")
        user_type = self.normalize("Enter user type (student/faculty/guest): ")
        try:
            user_id = self.library.register_user(name, email, user_type)
            print(f"User registered with ID {user_id}")
        except ValueError as e:
            print(f"Registration failed: {e}")
                    
    def find_user(self):
        user_id = input("Enter User ID to find: ").strip()
        user = self.library.find_user(user_id)
        if user:
            print(f"\nName: {user.name}\nEmail: {user.email}\nUser type: {user.user_type}\n")
            print(f"Borrowed books (ISBNs): {user.borrowed_books if user.borrowed_books else 'None'}\n")

    def borrowing_menu(self):
        print("""
--- Borrowing Operations ---
1. Borrow Book
2. Return Book
3. Show Overdue Books
0. Back
""")
        
        match input("Enter option: ").strip():
            case "1":
                self.borrow_book()
            case "2":
                self.return_book()
            case "3":
                self.get_overdue_books()
            case "0":
                return
            case _:
                print("Invalid option")

    def borrow_book(self):
        user_id = input("Enter User ID: ").strip()
        isbn = input("Enter Book ISBN: ").strip()
        try:
            self.library.borrow_book(user_id, isbn)
            print("The book has been borrowed")
        except ValueError as e:
            print(f"Borrowing failed: {e}")
            
    def return_book(self):
        user_id = input("Enter User ID: ").strip()
        isbn = input("Enter Book ISBN: ").strip()
        try:
            self.library.return_book(user_id, isbn)
            print("The book has been returned")
        except ValueError as e:
            print(f"Return failed: {e}")
            
    def get_overdue_books(self):
        overdue_records = self.library.get_overdue_books()
        if not overdue_records:
            print("There are no overdue books at the moment")
        else:
            print(f"\nFound {len(overdue_records)} overdue record(s):")
            for record in overdue_records:
                print(f" - User ID: {record.user_id} | Book ISBN: {record.isbn} | Borrowed on: {record.borrowed_date}")
                        
            
if __name__ == "__main__":
    library = Library() 
    
    console = LibraryConsole(library)
    
    console.run()