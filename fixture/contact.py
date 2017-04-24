from model.formfiller import Contact
import re

class ContactHelper:

    def __init__(self, app):
        self.app = app


    def add_new_contact(self, contact):
        wd = self.app.wd
        if not len(wd.find_elements_by_name("searchstring")) > 0:
            self.app.open_home_page()
        # add mew contact
        wd.find_element_by_xpath("//div[@id='nav']//a[.='nowy wpis']").click()
        self.fill_contact_form(contact)
        # accept
        wd.find_element_by_xpath("//div[@id='content']/form/input[21]").click()
        self.contact_cache = None

    def delete_first_contact(self):
        wd = self.app.wd
        self.delete_contact_by_index(0)

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        if not len(wd.find_elements_by_name("searchstring")) > 0:
            self.app.open_home_page()
        self.select_contact_by_index(index)
        #submit deletion
        wd.find_element_by_xpath("//div[@id='content']/form[2]/div[2]/input").click()
        wd.switch_to_alert().accept()
        self.contact_cache = None

    def modify_first_contact(self):
        wd = self.app.wd
        self.modify_contact_by_index(0)


    def modify_contact_by_index(self, index, contact):
        wd = self.app.wd
        if not len(wd.find_elements_by_name("searchstring")) > 0:
            self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cells = row.find_elements_by_tag_name("td")
        cells[7].click()
        self.fill_contact_form(contact)
        #accept changes
        wd.find_element_by_xpath("//div[@id='content']/form[1]/input[22]").click()
        self.contact_cache = None



    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))




    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("homephone", contact.homephone)
        self.change_field_value("mobilephone", contact.mobilephone)
        self.change_field_value("workphone", contact.workphone)
        self.change_field_value("secondaryphone", contact.secondaryphone)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)


    contact_cache = None


    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                firstname = cells[2].text
                lastname = cells[1].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("value")
                all_phones = cells[5].text
                adress = cells[3].text
                all_emails = cells[4].text
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname,
                                                  id=id, all_phones_from_home_page=all_phones, all_emails_from_home_page=all_emails, adress=adress))

        return list(self.contact_cache)


    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cells = row.find_elements_by_tag_name("td")[7]
        cells.find_element_by_tag_name("a").click()

    def open_contact_to_view_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cells = row.find_elements_by_tag_name("td")[6]
        cells.find_element_by_tag_name("a").click()

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        adress=wd.find_element_by_name("address").get_attribute("value")
        return Contact(firstname=firstname, lastname=lastname, id=id,
                       homephone=homephone, mobilephone=mobilephone, workphone=workphone, secondaryphone=secondaryphone,
                       email=email, email2=email2, email3=email3, adress=adress)




    def get_contact_view_page(self, index):
        wd = self.app.wd
        self.open_contact_to_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        return Contact(homephone=homephone, mobilephone=mobilephone, workphone=workphone, secondaryphone=secondaryphone)
