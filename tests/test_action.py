from dingdongditch import action


class TestStrike:
    def test_new_instance(self):
        instance = action.Strike(1)
        assert instance

    def test_get__new_instance(self):
        instance = action.Strike.get(1)
        assert instance

    def test_get__existing_instance(self):
        instance1 = action.Strike.get(1)
        instance2 = action.Strike.get(1)
        assert instance1 is instance2
