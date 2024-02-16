"""
User operation module contains methods to create new user, get user name by e-mail and etc.
Users module contains a method to extract user by an email from a database
Users module contains a method to create a user in a database, to get user avatar by his/her email
Users module contains a method to update user token in a database
Users module contains a method to confirm a user email in a database
Users module contains a method to update user avatar in a database
"""

from typing import Union

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel

async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a single contact with the specified id for the specific user with the specified email of the user.

    :param email: The email of the user.
    :type email: str

    :param db: The database session.
    :type db: Session

    :return: The user.
    :rtype: User
    """

    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user with the specific avatar with the specified email of the user.

    :param body: The data for the User to create.
    :type body: UserModel

    :param db: The database session.
    :type db: Session

    :return: The user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: Union[str, None], db: Session) -> None:
    """
    Returns updated token for a specific user.

    :param user: The user to update the token for.
    :type user: User

    :param token: The token of the user to be updated.
    :type token: Union[str, None]

    :param db: The database session.
    :type db: Session

    :return: The updated token.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Returns confirmed email.

    :param email: The email to be confirmed.
    :type email: str

    :param db: The database session.
    :type db: Session

    :return: The confirmed email.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Returns updated avatar with the specified email of the user.

    :param email: The email of the user.
    :type email: str

    :param url: The url of the user avatar.
    :type url: str

    :param db: The database session.
    :type db: Session

    :return: The updated avatar.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


