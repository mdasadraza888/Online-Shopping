from fastapi import Exception, status


class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, value: str):
        self.value = value
    


class AuthenticationException(AppException):
    """User authentication failed."""
    def __init__(self, value: str):
        super().__init__(value)


class AuthorizationException(AppException):
    """User is authenticated but not allowed to perform an action."""
    pass


class UserNotFoundException(AppException):
    pass


class ProductNotFoundException(AppException):
    pass


class CategoryNotFoundException(AppException):
    pass


class CartNotFoundException(AppException):
    pass


class OrderNotFoundException(AppException):
    pass


class PaymentException(AppException):
    pass


class InsufficientStockException(AppException):
    pass

