class User:
    count_id = 0


    def __init__(self, username, name, gender, membership, remarks):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__username = username
        self.__name = name
        self.__gender = gender
        self.__membership = membership
        self.__remarks = remarks

    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    def set_user_id(self,user_id):
        self.__user_id = user_id

    def set_username(self,username):
        self.__username = username

    def set_name(self,name):
        self.__name = name

    def set_gender(self,gender):
        self.__gender = gender

    def set_membership(self,membership):
        self.__membership = membership

    def set_remarks(self,remarks):
        self.__remarks = remarks


def query():
    return None