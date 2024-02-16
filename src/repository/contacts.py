"""
Contact operation module contains
methods to create new contact, get contact and other CRUD type operations.

Contacts module contains calculation of the age of a person ahead
Contacts module checks if there is a birthday of a person within the given days ahead
Contacts module contains a method to extract the user contact from database and put it on the list of the users who have birthdays within the given days ahead
Contacts module contains a method to create a list of the users contacts, limited to the given records limit number and with the ability to omit the given number of records.
Contacts module contains a method to extract a user contact from a database
Contacts module contains a method to extract notes of the first user contact from a database
Contacts module contains a method to create a contacts list of contacts filtered by email from a database
Contacts module contains a method to create a contacts list of contacts filtered by a first name from a database
Contacts module contains a method to create a contacts list of contacts filtered by a last name from a database
Contacts module contains a method to create a contacts list of contacts filtered by first and last name from a database
Contacts module contains a method to create a user contact, to add it to a database and to refresh a database
Contacts module contains a method to remove a user contact by contact id from a database
Contacts module contains a method to update a user contact by contact id in a database
Contacts module contains a method to update notes of a user contact by contact id in a database
"""

from datetime import timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, Interval
from src.database.models import Contact, User
from src.schemas import ContactBase


def age_in_years_for_days_ahead(birthday, next_days: int = 0):
    """
   Returns the age of the user within the given days ahead.

    :param birthday: The birthday of the user.
    :type birthday: date

    :param next_days: The number of days to calculate birthday.
    :type next_days: int

    :return: The age of the user who has birthday within the given days ahead.
    :rtype: int
    """
    stmt = func.age(
        (birthday - func.cast(timedelta(next_days), Interval)) if next_days != 0 else birthday
    )
    stmt = func.date_part("year", stmt)

    return stmt


def has_birthday_next_days(birthday, next_days: int = 0):
    """
    Returns the age of the user who has birthday within the given days ahead.

    :param birthday: The birthday of the user.
    :type birthday: date

    :param next_days: The number of days to calculate birthday.
    :type next_days: int

    :return: The age of the user who has birthday within the given days ahead.
    :rtype: int
    """

    return age_in_years_for_days_ahead(birthday, next_days) > age_in_years_for_days_ahead(birthday)


async def get_contacts_birthday_ahead(days: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with the specified id for the specific user with birthday within the given days.

    :param days: The number of days ahead to calculate birthday.
    :type days: int

    :param user: The user with birthday to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    # if contacts is None:
    #    return None

    return (
        db.query(Contact).filter(and_(Contact.user_id == user.id, has_birthday_next_days(Contact.birthday, days))).all()
    )


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with the specified id for the specific user with the specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int

    :param limit: The maximum number of contacts to return.
    :type limit: int

    :param user: The user to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(
        Contact.user_id == user.id
    ).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
        Retrieves a single contact with the specified id for the specific user.

    :param contact_id: The id of a user.
    :type contact_id: int

    :param user: The user to update the notes for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The contact.
    :rtype: ContactResponse
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.id == contact_id
        )
    ).first()


async def get_contact_notes(contact_id: int, user: User, db: Session) -> Contact | None:
    """
   Retrieves a list of notes with the specified id for the specific user.

    :param contact_id: The id of a user.
    :type contact_id: int

    :param user: The user to update the notes for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The updated notes.
    :rtype: ContactResponse
    """
    contact = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.id == contact_id
        )
    ).first()

    return contact


async def get_contacts_by_email(contact_email: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with the specified id for the specific user with the specified email of the user.

    :param contact_email: The email of the user.
    :type contact_email: str

    :param user: The user to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            #Contact.email.ilike(f'%{contact_email}%')
            Contact.email == contact_email
        )
    ).all()


async def get_contacts_by_firstname(firstname: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with the specified id for the specific user with the specified first name of the user.

    :param firstname: The first name of the user.
    :type firstname:  str

    :param user: The user to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.firstname.ilike(f'%{firstname}%')
        )
    ).all()


async def get_contacts_by_secondname(secondname: str, user: User, db: Session) -> List[Contact]:
    """
     Retrieves a list of contacts with the specified id for the specific user with the specified second name of the user.

    :param secondname: The second name of the user.
    :type secondname:  str

    :param user: The user to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.secondname.ilike(f'%{secondname}%')
        )
    ).all()


async def get_contacts_by_first_and_second_name(firstname: str, secondname: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with the specified first and second name of the user.

    :param firstname: The first name of the user.
    :type firstname:  str

    :param secondname: The second name of the user.
    :type secondname:  str

    :param user: The user to get contacts for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.firstname.ilike(f'%{firstname}%'),
            Contact.secondname.ilike(f'%{secondname}%')
        )
    ).all()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    """
   Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactBase

    :param user: The user to create the contact for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(firstname=body.firstname,
                      secondname=body.secondname,
                      email=body.email,
                      telephone=body.telephone,
                      birthday=body.birthday,
                      user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
      Removes a single user contact with the specified id for a specific user.

    :param contact_id: The id of a user.
    :type contact_id: int

    :param user: The user to remove the contact for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The removed contacts or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.id == contact_id
        )
    ).first()

    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def update_contact(contact_id: int, body: ContactBase, user: User, db: Session) -> Contact | None:
    """
    Returns updated contact with the specified id for a specific user.

    :param contact_id: The id of a user.
    :type contact_id: int

    :param body: The updated data for the contact.
    :type body: ContactBase

    :param user: The user to update the contact for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The updated contact or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.id == contact_id
        )
    ).first()

    if contact:
        contact.firstname = body.firstname
        contact.secondname = body.secondname
        contact.email = body.email
        contact.telephone = body.telephone
        contact.birthday = body.birthday

        db.commit()

    return contact


async def update_contact_notes(contact_id: int, notes: str, user: User, db: Session) -> Contact | None:
    """
    Returns updated notes with the specified id for a specific user.

    :param contact_id: The id of a user.
    :type contact_id: int

    :param notes: The updated contact notes.
    :type notes: str

    :param user: The user to update the notes for.
    :type user: User

    :param db: The database session.
    :type db: Session

    :return: The updated notes or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.id == contact_id
        )
    ).first()

    if contact:
        contact.notes = notes

        db.commit()

    return contact
