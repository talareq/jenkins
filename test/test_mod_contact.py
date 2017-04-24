from model.formfiller import Contact
from random import randrange


def test_modify_first_contact(app):

    if app.contact.count() == 0:
        app.contact.add_new_contact(Contact(firstname="tester", lastname="tester"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = Contact(firstname="roman", lastname="erotoman")
    contact.id = old_contacts[index].id
    app.contact.modify_contact_by_index(index, contact)
    assert len(old_contacts) == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

