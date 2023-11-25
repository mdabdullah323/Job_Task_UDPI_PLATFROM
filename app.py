from uuid import uuid4

from api import ParentApi, ChildApi
from enums import UserChoice, ApiOperation, Status
from exceptions import ExitException, InvalidUser
from file import File
from models import ChildModel, ParentModel, UserModel


class ConsoleUI:
    app_name = None
    db_file = "./data/database.json"
    description = "create parent, child and store their information"
    exit_message = "program exited"

    def __init__(self):
        self.file = File("./data/database.json")
        self.parent_api = ParentApi(self.file)
        self.child_api = ChildApi(self.file)
        self.child_model: ChildModel
        self.paren_model: ParentModel
        self.user_model: UserModel
        self.api_operation: ApiOperation
        self.user: UserChoice

    def _select_user_type_form(self):

        _choice_message = "\n1: Parent \n 2: Child"
        _choices = tuple(c.value for c in UserChoice)

        print(_choice_message)
        choice = input("select: ")
        if choice in _choices:
            self.user = UserChoice(choice)

    def _api_operation_form(self):
        print("1: create user \n 2: update user \n 3: delete user")
        _choice = input("select: ")
        _choices = tuple(c.value for c in ApiOperation)
        if _choice in _choices:
            self.api_operation = ApiOperation(_choice)

    def _user_form(self):
        first_name = input("first name: ")
        last_name = input("last name: ")
        self.user_model = UserModel(first_name=first_name,
                                    last_name=last_name)

    def _child_form(self):
        print("---------- provide child  information -------- ")
        self._user_form()
        _data = {"id": str(uuid4()), **self.user_model.model_dump()}
        self.child_model = ChildModel(**_data)

    def _parent_form(self):
        print("---------- provide parent  information -------- ")
        if self.user == UserChoice.PARENT:
            self._user_form()
            print("----------- address ---------------")
            street = input("street: ")
            city = input("city: ")
            state = input("state: ")
            zip_code = input("zip: ")
            self._child_form()
            _child_data = {"id": str(uuid4()), **self.user_model.model_dump()}
            _child_data = ChildModel(**_child_data)
            _data = {
                "id": str(uuid4()),
                **self.user_model.model_dump(),
                "street": street,
                "city": city,
                "state": state,
                "zip": zip_code,
                "child": _child_data
            }
            self.parent_model = ParentModel(**_data)

    def _user_create_form(self):
        _header = "Choose user Type to Create a new User\n"
        print(_header)
        self.user = None
        status = None
        while not self.user:
            self._select_user_type_form()
        if self.user == UserChoice.PARENT:
            self._parent_form()
            res = self.parent_api.create(self.parent_model)
            status = res["status"]
            print(f'\nparent id :{res["id"]}\n')
        if self.user == UserChoice.CHILD:
            self._child_form()
            _parent_id = input("parent id: ")
            status = self.child_api.create(self.child_model, parent_id=_parent_id)["status"]
        if status == Status.CRATED:
            print("created")
        else:
            print("failed")

    def _user_delete_form(self):
        print("_______ DELETE USER ___________")
        self._select_user_type_form()
        _id = input("user id: ")
        if self.user == UserChoice.PARENT:
            res = self.parent_api.delete(_id)
            status = res["status"]
            if status == Status.DELETED:
                print("deleted")
            else:
                print("failed")
        if self.user == UserChoice.CHILD:
            res = self.child_api.delete(_id)
            status = res["status"]
            if status == Status.DELETED:
                print("deleted")
            else:
                print("failed")
    def _user_update_form(self):
        print("_______ UPDATE USER ___________")
        self._select_user_type_form()
        if self.user == UserChoice.PARENT:
            _id = input("user id: ")
            self._parent_form()
            res = self.parent_api.update(_id, self.parent_model)
            status = res["status"]
            if status == Status.UPDATED:
                print("updated")
            else:
                print("failed")
        if self.user == UserChoice.CHILD:
            _id = input("user id: ")
            self._child_form()
            res = self.child_api.update(_id, self.child_model)
            status = res["status"]
            if status == Status.UPDATED:
                print("updated")
            else:
                print("failed")

    def _api_dashboard(self):
        print("________ User Management Api _________")
        while True:
            self._api_operation_form()
            if self.api_operation == ApiOperation.CREATE:
                self._user_create_form()
            if self.api_operation == ApiOperation.DELETE:
                self._user_delete_form()
            if self.api_operation == ApiOperation.UPDATE:
                self._user_update_form()

            _choice = input("c: Continue \n x: Exit\n")
            _choices = ("c", "x")
            if _choice in _choices:
                if _choice.lower() == "x":
                    raise ExitException

    def _exit_program(self):
        print(self.exit_message)

    def run(self):
        try:
            self._api_dashboard()
        except ExitException or InvalidUser:
            self._exit_program()


if __name__ == '__main__':
    ConsoleUI().run()
