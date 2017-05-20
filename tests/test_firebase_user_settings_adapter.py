import pytest

from dingdongditch import firebase_user_settings_adapter as user_settings

class TestFirebaseData__get_path_list:
    def test_no_path(self):
        data = user_settings.FirebaseData()
        result = data._get_path_list('')
        assert result == []

    def test_root_path(self):
        data = user_settings.FirebaseData()
        result = data._get_path_list('/')
        assert result == []

    def test_absolute_child_path(self):
        data = user_settings.FirebaseData()
        result = data._get_path_list('/foo/bar')
        assert result == ['foo', 'bar']

    def test_relative_child_path(self):
        data = user_settings.FirebaseData()
        result = data._get_path_list('foo/bar')
        assert result == ['foo', 'bar']


class TestFirebaseData_set:
    def test_set_root(self):
        data = user_settings.FirebaseData()
        data.set('/', {'foo': 1})
        assert data == {'foo': 1}

    def test_set_missing_child(self):
        data = user_settings.FirebaseData()
        data.set('/foo/bar', 1)
        assert data == {'foo': {'bar': 1}}

    def test_set_existing_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_missing_then_set_existing(self):
        data = user_settings.FirebaseData()
        data.set('/foo', {'bar': 1})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_different_type(self):
        data = user_settings.FirebaseData({'foo': 1})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_missing_then_set_different_type(self):
        data = user_settings.FirebaseData()
        data.set('/foo', 1)
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_different_type_then_set_missing(self):
        data = user_settings.FirebaseData({'foo': 1})
        data.set('/foo/bar', 2)
        data.set('/foo/bar/baz', {'qux': 1})
        assert data == {'foo': {'bar': {'baz': {'qux': 1}}}}


class TestFirebaseData_get:
    def test_get_root(self):
        data = user_settings.FirebaseData()
        result = data.get('/')
        assert result == {}

    def test_get_missing_key(self):
        data = user_settings.FirebaseData()
        result = data.get('/foo/bar')
        assert result == None

    def test_get_different_type_key(self):
        data = user_settings.FirebaseData({'foo': 1})
        result = data.get('/foo/bar')
        assert result == None

    def test_existing_key(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        result = data.get('/foo/bar')
        assert result == 1


class TestFirebaseData_merge:
    def test_merge_root(self):
        data = user_settings.FirebaseData()
        data.merge('/', {'foo': 1})
        assert data == {'foo': 1}

    def test_merge_missing(self):
        data = user_settings.FirebaseData()
        data.merge('/foo', {'bar': 1})
        assert data == {'foo': {'bar': 1}}

    def test_merge_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.merge('/foo', {'baz': 1})
        assert data == {'foo': {'bar': 1, 'baz': 1}}

    def test_cannot_merge_different_type(self):
        data = user_settings.FirebaseData({'foo': 1})
        with pytest.raises(TypeError):
            data.merge('/foo', {'bar': 1})
