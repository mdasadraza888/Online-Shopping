from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import ProductNotFoundException, UserNotFoundException, AppException, AuthenticationException, AuthorizationException, CategoryNotFoundException, CartNotFoundException, OrderNotFoundException, PaymentException, InsufficientStockException

async def user_authentication_handler(request: Request, exc: AuthenticationException):
    return JSONResponse(
        status_code=401,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )


async def user_authorization_handler(request: Request, exc: AuthorizationException):
    return JSONResponse(
        status_code=401,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )



async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=401,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )


async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )

async def category_not_found_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )

async def cart_not_found_handler(request: Request, exc: CartNotFoundException):
    return JSONResponse(
        status_code=404, 
        content={
            "status": "Error",
            "message": str(exc)
        }
    )


async def order_not_found_handler(request: Request, exc: OrderNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )

async def payment_handler(request: Request, exc: PaymentException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "Error",
            "message": str(exc)
        }
    )







