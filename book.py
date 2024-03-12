import requests
from bs4 import BeautifulSoup

class Book:
    __book_list = []

    def __init__(self):
        self.__url = None

    def set_url(self, url: str):
        self.__url = url
        return self

    def get_url_html_content(self):
        return requests.get(self.__url).text

    def _get_book_list_soup_instance(self):
        soup = BeautifulSoup(self.get_url_html_content(), 'lxml')
        book_list = soup.find_all("div", class_="books-wrapper__item")
        for book in book_list:
            self.__book_list.append(self._get_book_data(book))

    def _get_book_data(self, book):
        book_url = book.find('a').get('href')
        image_div = book.find('div', class_='book-img')
        image_url = image_div.find('img').get('src')
        discount_percentage = image_div.find('div', class_='discount-badge-common badge-common').text
        book_text_area = book.find('div', class_="book-text-area")
        book_name = book_text_area.find('h4', class_='book-title').text
        book_author = book_text_area.find('p', class_='book-author').text
        book_price_div = book_text_area.find('p', class_='book-price')
        book_regular_price_div = book_price_div.find('strike', class_='original-price pl-2')
        book_regular_price = book_regular_price_div.text.replace("TK. ", "")

        # skip the strike tag as its regular price and get it before
        book_price_div.strike.decompose()
        discount_price = book_price_div.text.replace("TK. ", '')

        return {
            'book_name': book_name,
            'book_author': book_author,
            'book_url': book_url,
            'book_image': image_url,
            'book_price': book_regular_price.replace(' ', ''),
            'book_discount_price': discount_price.replace(' ', ''),
            'book_discount_percentage': discount_percentage.replace(' ', '')
        }


    def get_book_list(self):
        self._get_book_list_soup_instance()
        return self.__book_list


if __name__ == '__main__':
    book = Book()
    books = book.set_url('https://www.rokomari.com/book/author/1/humayun-ahmed?ref=mm_p0').get_book_list()
    print(books)
