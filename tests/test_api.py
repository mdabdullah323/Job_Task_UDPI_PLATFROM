from unittest import TestCase
from uuid import uuid4
from api import ParentApi, ChildApi
from enums import Status
from file import File
from models import ParentModel, ChildModel


class TestApi(TestCase):
    file = File("./data/test_database.json")
    parent_api = ParentApi(file)
    child_api = ChildApi(file)

    def test_parent_create_success(self):
        model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=ChildModel(first_name="junior",
                             last_name="john",
                             id=str(uuid4()))
        )
        _res = self.parent_api.create(model)
        self.assertEqual(Status.CRATED, _res["status"])
        self.assertEqual(str(model.model_dump()["id"]), _res["id"])

    def test_child_create_success(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(model=parent_model)
        _res_id = self.child_api.create(model=child_model, parent_id=str(parent_model.id))

        self.assertEqual(_res_id["status"], Status.CRATED)

    def test_child_create_failed_check(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(model=parent_model)
        _res_id = self.child_api.create(model=child_model, parent_id="dfsdfsdf")
        self.assertEqual(_res_id["status"], Status.Failed)

    def test_parent_deleted_success(self):
        model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=ChildModel(first_name="junior",
                             last_name="john",
                             id=str(uuid4()))
        )
        self.parent_api.create(model)
        status = self.parent_api.delete(str(model.id))["status"]
        self.assertEqual(status, Status.DELETED)

    def test_child_deleted_success(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(parent_model)
        status = self.child_api.delete(str(child_model.id))["status"]
        self.assertEqual(status, Status.DELETED)

    def test_child_deleted_failed_check(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(parent_model)
        status = self.child_api.delete(str("sfsdfsdf"))["status"]
        self.assertEqual(status, Status.Failed)

    def test_parent_update_success(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        updated_parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(parent_model)
        status = self.parent_api.update(str(parent_model.id), updated_parent_model)["status"]
        self.assertEqual(status, Status.UPDATED)

    def test_parent_update_failed_check(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        updated_parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        self.parent_api.create(parent_model)
        status = self.parent_api.update(str("invalid_id"), updated_parent_model)["status"]
        self.assertEqual(status, Status.Failed)

    def test_child_update_success(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        updated_child_model = ChildModel(first_name="junior",
                                         last_name="john",
                                         id=str(uuid4()))
        self.parent_api.create(parent_model)
        status = self.child_api.update(str(child_model.id), updated_child_model)["status"]
        self.assertEqual(status, Status.UPDATED)

    def test_child_update_failed_check(self):
        child_model = ChildModel(first_name="junior",
                                 last_name="john",
                                 id=str(uuid4()))
        parent_model = ParentModel(
            id=str(uuid4()),
            first_name="john",
            last_name="doe",
            street="9",
            city="A",
            zip="123",
            state="B",
            child=child_model
        )
        updated_child_model = ChildModel(first_name="junior",
                                         last_name="john",
                                         id=str(uuid4()))
        self.parent_api.create(parent_model)
        status = self.child_api.update(str("invalid_id"), updated_child_model)["status"]
        self.assertEqual(status, Status.Failed)
        pass



