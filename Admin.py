import Base as Base
import datetime as datetime


class Admin(Base.Base):
    count_id = 0

    def __init__(self, code, gender, email,remarks,password):
        super().__init__(datetime.datetime.now())
        Admin.count_id += 1
        self.__admin_id = Admin.count_id
        self.__code = code
        self.__remarks = remarks
        self.__gender = gender
        self.__email = email
        self.__password = password

    def get_admin_id(self):
        return self.__admin_id

    def get_code(self):
        return self.__code

    def get_remarks(self):
        return self.__remarks

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_password(self):
        return self.__password

    def set_admin_id(self, admin_id):
        self.__admin_id = admin_id

    def set_code(self, code):
        self.__code = code

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_password(self,password):
        self.__password = password
