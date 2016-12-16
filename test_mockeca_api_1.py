from unittest.case import TestCase


class ProductGateway:
    def find_by_name(self, name):
        pass

    def find_by_code(self, code):
        pass

    def fetch(self):
        pass

    def save(self, product):
        pass


class Product:
    def __init__(self, name, code):
        self.name = name
        self.code = code


class QueryBuilderTests(TestCase):
    def setUp(self):
        self.mockeca = mockeca.setup()
        self.product_gateway = self.mockeca.mock(ProductGateway)

    def test_can_mock_query_builders(self):
        product = Product()
        stub(self.product_gateway.find_by_name('tapioca').find_by_code(123).fetch(),
             return_value=product)

        with self.mockeca.ready():
            result = self.product_gateway.find_by_name('tapioca').find_by_code(123).fetch()

        self.assertIs(product, result)

    def test_exception_when_do_not_calls_the_last_method_of_the_stub_chain(self):
        product = Product()
        stub(self.product_gateway.find_by_name('tapioca').find_by_code(123).fetch(),
             return_value=product)

        with self.assertRaises(StubNotUsedException)
            with self.mockeca.ready:
                self.product_gateway.find_by_name('tapioca').find_by_code(123)

    def test_exception_when_do_not_respect_the_stub_chain(self):
        product = Product()
        stub(self.product_gateway.find_by_name('tapioca').find_by_code(123).fetch(),
             return_value=product)

        with self.assertRaises(InvalidStubChainException):
            with self.mockeca.ready():
                self.product_gateway.fetch()

        self.assertIsInstance(ctx.exception, InvalidStubChainException)

    def test_exception_when_invoke_something_that_wasnt_stubbed(self):
        product = Product()
        stub(self.product_gateway.find_by_code(123).fetch(),
             return_value=product)

        with self.assertRaises(InvalidStubChainException):
            with self.mockeca.ready():
                self.product_gateway.find_by_name(123)

    def test_exception_when_try_to_use_an_partial_method_chain(self):
        product = Product()
        stub(self.product_gateway.find_by_code(123).fetch(),
             return_value=product)

        with self.assertRaises(MisuseOfAStubChain):
            with self.mockeca.ready():
                incomplete_chain = self.product_gateway.find_by_name(123)
                incomplete_chain += 1

    def test_do_not_raise_exception_when_method_is_expected(self):
        expected(self.product_gateway.save)

        with self.mockeca.ready():
            self.product_gateway.save(Product('example', '007'))

        self.assertEqual('example', self.product_gateway.save.args[0])
        self.assertEqual('007', self.product_gateway.save.args[1])

    def test_raise_exception_when_method_is_expected_but_with_wrong_arguments(self):
        expected(self.product_gateway.save('007', 'example'))

        with self.assertRaises(ExpectationNotMatchException):
            with self.mockeca.ready():
                self.product_gateway.save(Product('example', '007'))
