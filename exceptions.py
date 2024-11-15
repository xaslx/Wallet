from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# Пользователи
class UserAlreadyExistsException(BaseException):
    status_code = 409
    detail = "Пользователь уже существует"


class IncorrectUsernameOrPasswordException(BaseException):
    status_code = 401
    detail = "Неверное имя пользователя или пароль"



class UserNotFound(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь не найден"


class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED



#wallet

class WalletNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Кошелек не найден"


class NotEnoughMoney(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Недостаточно средств"


class InvalidJson(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid Json Request"




# JWT token
class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"