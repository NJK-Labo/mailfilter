from flask_wtf import FlaskForm  # type: ignore


class MockSearchFormField:
    """検索フォームのテスト用モックフィールド"""

    def __init__(self, name, value):
        self.name = name
        self.data = value
        self.errors = []


class MockSearchForm(FlaskForm):
    """検索フォームのテスト用モック"""

    def __init__(self, data, is_valid, errors):
        self._data = data
        self._is_valid = is_valid
        self._errors = errors

        self._fields = {k: MockSearchFormField(k, v) for k, v in data.items()}
        for field_name, field in self._fields.items():
            setattr(self, field_name, field)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def validate(self):
        return self._is_valid

    @property
    def errors(self):
        return self._errors
