from typing import Annotated

import grpc
from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from google.protobuf.json_format import MessageToDict

from app.auth.exceptions import Forbidden, Unauthorized
from app.auth.schemas import UserRead
from app.config import settings
from app.grpc import grpc_clients
from app.protos import auth_pb2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/login")

Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Token = Annotated[str, Depends(oauth2_scheme)]


async def current_user(token: Token) -> UserRead:
    try:
        request = auth_pb2.Token(token=token)
        user = await grpc_clients["auth"].User(
            request,
            timeout=settings.grpc_timeout,
        )
        data = MessageToDict(
            user,
            always_print_fields_with_no_presence=True,
            preserving_proto_field_name=True,
        )
        return UserRead(**data)
    except grpc.aio.AioRpcError as e:
        raise Unauthorized() from e


CurrentUser = Annotated[UserRead, Depends(current_user)]


async def current_active_user(
    user: CurrentUser,
    security_scopes: SecurityScopes,
) -> UserRead:
    if not user.is_active:
        raise Unauthorized()
    for scope in security_scopes.scopes:
        if scope not in user.user_type.scopes:
            raise Forbidden()
    return user


CurrentActiveUser = Annotated[UserRead, Depends(current_active_user)]
# AdminScopedUser = Annotated[UserRead, Security(current_active_user, scopes=["admin"])]
