from datetime import date
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactBase, ContactNotes
from src.repository.contacts import (
    #age_in_years_for_days_ahead,
    #has_birthday_next_days,
    get_contacts_birthday_ahead,
    get_contacts,
    get_contact,
    get_contact_notes,
    get_contacts_by_email,
    get_contacts_by_firstname,
    get_contacts_by_secondname,
    get_contacts_by_first_and_second_name,
    create_contact,
    remove_contact,
    update_contact,
    update_contact_notes,
)
import unittest
from unittest.mock import MagicMock

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts_birthday_ahead(self):
        contacts = [Contact(birthday=date(2002, 2, 10)),
                    Contact(birthday=date(2003, 2, 10)),
                    Contact(birthday=date(2004, 2, 10))]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_birthday_ahead(days=5, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        contact = ContactBase(firstname="fname",
                              secondname="sname",
                              email="email value",
                              telephone="0000",
                              birthday=date(2001, 1, 1),
                              )

        result = await create_contact(body=contact, user=self.user, db=self.session)

        self.assertEqual(result.firstname, contact.firstname)
        self.assertEqual(result.secondname, contact.secondname)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.telephone, contact.telephone)
        self.assertEqual(result.birthday, contact.birthday)

        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_found(self):
        contact = ContactBase(firstname="fname2",
                              secondname="sname2",
                              email="email value2",
                              telephone="0000",
                              birthday=date(2002, 2, 2),
                              )
        contact_update = Contact()
        self.session.query().filter().first.return_value = contact_update
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact, user=self.user, db=self.session)
        self.assertEqual(result, contact_update)

    async def test_update_contact_not_found(self):
        contact = ContactBase(firstname="fname2",
                              secondname="sname2",
                              email="email value2",
                              telephone="0000",
                              birthday=date(2002, 2, 2),
                              )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_notes_found(self):
        contact = ContactNotes(firstname="fname2",
                               secondname="sname2",
                               email="email value2",
                               telephone="0000",
                               birthday=date(2002, 2, 2),
                               notes="notes are here!"
                               )
        contact_update = Contact()
        self.session.query().filter().first.return_value = contact_update
        self.session.commit.return_value = None
        result = await update_contact_notes(contact_id=1, notes=contact.notes, user=self.user, db=self.session)
        self.assertEqual(result, contact_update)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_notes_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_notes(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_notes_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_by_email_found(self):
        contact_email = "sth@sth.com"
        contacts = [
            Contact(email=contact_email),
            Contact(email=contact_email),
            Contact(email=contact_email),
        ]

        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_email(contact_email=contact_email, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_email_not_found(self):
        email = "sth@sth.com"
        contacts = []

        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_email(contact_email=email, user=self.user, db=self.session)
        self.assertEqual(result, [])

    async def test_get_contacts_by_firstname_found(self):
        firstname = "Ann"
        contacts = [
            Contact(firstname=firstname),
            Contact(firstname=firstname),
            Contact(firstname=firstname)
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_firstname(firstname=firstname, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_firstname_not_found(self):
        firstname = "Ann"
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_firstname(firstname=firstname, user=self.user, db=self.session)
        self.assertEqual(result, [])

    async def test_get_contacts_by_secondname(self):
        secondname = "Leen"
        contacts = [
            Contact(secondname=secondname),
            Contact(secondname=secondname),
            Contact(secondname=secondname)
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_secondname(secondname=secondname, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_secondname_not_found(self):
        secondname = "Leen"
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_secondname(secondname=secondname, user=self.user, db=self.session)
        self.assertEqual(result, [])

    async def test_get_contacts_by_first_and_secondname(self):
        firstname = "Ann"
        secondname = "Leen"
        contacts = [
            Contact(firstname=firstname, secondname=secondname),
            Contact(firstname=firstname, secondname=secondname),
            Contact(firstname=firstname, secondname=secondname)
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_first_and_second_name(firstname=firstname, secondname=secondname, user=self.user,
                                                             db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_first_and_secondname_not_found(self):
        firstname = "Ann"
        secondname = "Leen"
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_first_and_second_name(firstname=firstname, secondname=secondname, user=self.user,
                                                             db=self.session)
        self.assertEqual(result, [])



if __name__ == '__main__':
    unittest.main()
