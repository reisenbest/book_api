import re

class BookValidator:
    def __init__(self, book_instance: dict):
        '''

        :param book_instance: Словарь, представляющий экземпляр книги.
        '''
        self.book_instance = book_instance
        self.required_keys = ["title", "isbn", "pageCount", "thumbnailUrl",
                              'publishedDate', "status", "authors", "categories"]

        # Если статус равен 'MEAP', удаляем 'publishedDate' из обязательных ключей
        if "status" in self.book_instance and self.book_instance["status"] == "MEAP":
            self.required_keys.remove("publishedDate")



    def book_instance_validate(self):
        '''
        проверяет наличие необходимых полей для первичной валидации

        :return: при прохождение всех проверок - > true
        '''
        book_instance = self.book_instance
        validation_result = True
        for key in self.required_keys:
            if key not in book_instance:
                validation_result = False

        return validation_result

    def validate_title(self) -> bool:
        '''
        из объекта book_instance передается значение ключа title (book_instance['title']

        :return: при прохождение всех проверок - > true
        '''
        title = self.book_instance['title']
        validation_result = True
        if not isinstance(title, str):
            validation_result = False

        elif len(title) == 0:
            validation_result = False

        return validation_result

    def validate_isbn(self) -> bool:
        '''
        isbn: из объекта book_instance передается значение ключа isbn (book_instance['isbn']

        :return: при прохождение всех проверок - > true
        '''
        isbn = self.book_instance['isbn']
        validation_result = True
        if not isinstance(isbn, str):
            validation_result = False

        elif len(isbn) != 10 and len(isbn) != 13:
            validation_result = False

        if validation_result:
            if len(isbn) == 13:
                isbn_pattern = r'^\d{13}$'
                if re.match(isbn_pattern, isbn) is None:
                    validation_result = False
            elif len(isbn) == 10:
                isbn_pattern = r'^\d{9}[\d|X]$'
                if re.match(isbn_pattern, isbn) is None:
                    validation_result = False

        return validation_result

    def validate_pageCount(self) -> bool:
        '''
         из объекта book_instance передается значение ключа pageCount (book_instance['pageCount'])

        :return: при прохождение всех проверок - > true
        '''
        pageCount = self.book_instance['pageCount']
        status = self.book_instance['status']
        validation_result = True
        if not isinstance(pageCount, int):
            validation_result = False

        elif status != 'MEAP' and pageCount <= 0:
            validation_result = False

        return validation_result

    def validate_publishedDate(self) -> bool:
        '''
         из объекта book_instance передается значение ключа publishedDate (book_instance['publishedDate'])

        :return: при прохождение всех проверок - > true
        '''
        validation_result = True

        if 'publishedDate' in self.required_keys:
            publishedDate = self.book_instance['publishedDate']

            if not isinstance(publishedDate, dict):
                validation_result = False

            elif "$date" not in publishedDate or len(publishedDate["$date"]) != 28:
                validation_result = False

            return validation_result
        else:
            return validation_result

    def validate_thumbnailUrl(self) -> bool:
        '''
         из объекта book_instance передается значение ключа thumbnailUrl (book_instance['thumbnailUrl'])

        :return: при прохождение всех проверок - > true
        '''
        thumbnailUrl = self.book_instance['thumbnailUrl']
        validation_result = True
        if not isinstance(thumbnailUrl, str):
            validation_result = False

        return validation_result

    def validate_status(self) -> bool:
        '''
        :param status: из объекта book_instance передается значение ключа status (book_instance['status'])

        :return: при прохождение всех проверок - > true
        '''
        status = self.book_instance['status']
        validation_result = True
        if not isinstance(status, str):
            validation_result = False

        elif status != 'PUBLISH' and status != 'MEAP':
            validation_result = False

        return validation_result

    def validate_authors(self) -> bool:
        '''
        из объекта book_instance передается значение ключа authors (book_instance['authors'])

        :return: при прохождение всех проверок - > true
        '''
        authors = self.book_instance['authors']
        validation_result = True
        if not isinstance(authors, list):
            validation_result = False

        return validation_result

    def validate_categories(self) -> bool:
        '''
        из объекта book_instance передается значение ключа categories (book_instance['categories'])

        :return: при прохождение всех проверок - > true
        '''
        categories = self.book_instance['categories']
        validation_result = True
        if not isinstance(categories, list):
            validation_result = False

        return validation_result


