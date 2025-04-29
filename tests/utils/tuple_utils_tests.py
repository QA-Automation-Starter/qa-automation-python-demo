import attr
from hamcrest import *
from python_selenium.utils.tuple_utils import *


def should_assert_from_tuple():
    @attr.define
    class Foo(FromTupleMixin):
        id: int
        name: str

    assert_that(str(Foo.from_tuple((1, "kuku"))),
                is_("Foo(id=1, name='kuku')"))
