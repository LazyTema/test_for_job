import json


# Структура книги
class Book:
    def __init__(self, title, author, year):
        self.id = None  # id будет назначено автоматически при добавлении
        self.title = title
        self.author = author
        self.year = year
        self.status = 'в наличии'


# Библиотека для хранения книг
class Library:
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = self.load_books()

    # Загрузка данных из файла
    def load_books(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        except FileNotFoundError:
            return []

    # Сохранение данных в файл
    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            data = [book.__dict__ for book in self.books]
            json.dump(data, file, ensure_ascii=False, indent=4)

    # Добавление книги
    def add_book(self, title, author, year):
        book = Book(title, author, year)
        book.id = self.generate_id()
        self.books.append(book)
        self.save_books()

    # Удаление книги по id
    def remove_book(self, book_id):
        book_to_remove = self.find_book_by_id(book_id)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
        else:
            print(f'Книга с id {book_id} не найдена.')

    # Поиск книги по любому из полей
    def search_books(self, search_term):
        results = []
        for book in self.books:
            if (search_term.lower() in book.title.lower() or
                    search_term.lower() in book.author.lower() or
                    search_term.lower() in str(book.year)):
                results.append(book)
        return results

    # Отображение всех книг
    def display_books(self):
        if not self.books:
            print('Нет доступных книг в библиотеке.')
        for book in self.books:
            print(
                f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')

    # Изменение статуса книги
    def change_status(self, book_id, new_status):
        book = self.find_book_by_id(book_id)
        if book:
            if new_status in ['в наличии', 'выдана']:
                book.status = new_status
                self.save_books()
            else:
                print('Недопустимый статус. Используйте "в наличии" или "выдана".')
        else:
            print(f'Книга с id {book_id} не найдена.')

    # Поиск книги по id
    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    # Генерация уникального id
    def generate_id(self):
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1


# Основное меню
def main():
    library = Library()

    while True:
        print('\n1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книги')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('6. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            title = input('Название книги: ')
            author = input('Автор книги: ')
            year = int(input('Год издания: '))
            library.add_book(title, author, year)
            print('Книга добавлена.')

        elif choice == '2':
            book_id = int(input('Введите id книги для удаления: '))
            library.remove_book(book_id)

        elif choice == '3':
            search_term = input('Введите название, автора или год для поиска: ')
            results = library.search_books(search_term)
            if results:
                for book in results:
                    print(
                        f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')
            else:
                print('Книги не найдены.')

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input('Введите id книги для изменения статуса: '))
            new_status = input('Введите новый статус ("в наличии" или "выдана"): ')
            library.change_status(book_id, new_status)

        elif choice == '6':
            print('Выход из программы.')
            break

        else:
            print('Неверный выбор. Пожалуйста, выберите действие из списка.')


if __name__ == '__main__':
    main()