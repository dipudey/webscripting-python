from book import Book

if __name__ == '__main__':
    book = Book()
    books = book.set_url('https://www.rokomari.com/book/author/1/humayun-ahmed?ref=mm_p0').get_book_list()
    print(books)