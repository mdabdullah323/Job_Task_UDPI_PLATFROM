from abc import abstractmethod, ABC
from enums import Status
from models import ParentModel, ChildModel


class Api(ABC):
    @abstractmethod
    def create(self, model, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, _id: str):
        pass

    @abstractmethod
    def update(self, _id, model):
        pass


class ParentApi(Api):
    def __init__(self, file):
        self.file = file

    def create(self, model: ParentModel, *args, **kwargs):
        _model_data = model.model_dump()
        _data = self.file.read() + [_model_data]
        self.file.save(_data)
        return {"status": Status.CRATED, "id": str(_model_data["id"])}

    def delete(self, _id: str):
        data = self.file.read()
        _data = []
        deleted = False
        for user in data:
            if user["id"] != _id:
                _data.append(user)
            else:
                deleted = True
        if deleted:
            self.file.save(_data)
            return {"status": Status.DELETED}
        else:
            return {"status": Status.Failed}

    def update(self, _id: str, model: ParentModel):
        data = self.file.read()
        _data = []
        updated = False
        for user in data:
            if user["id"] == _id:
                _data.append(model.model_dump())
                updated = True
            else:
                _data.append(user)
        if updated:
            self.file.save(_data)
            return {"status": Status.UPDATED}
        return {"status": Status.Failed}


class ChildApi(Api, ABC):
    def __init__(self, file):
        self.file = file

    def create(self, model: ChildModel, *args, **kwargs):
        parent_id = kwargs["parent_id"]
        data = self.file.read()
        for user in data:
            if user["id"] == str(parent_id):
                user["child"] = model.model_dump()
                return {"status": Status.CRATED, "id": str(model.model_dump()["id"])}
        return {"status": Status.Failed}

    def delete(self, _id: str):
        data = self.file.read()
        deleted = False
        _data = []
        for user in data:
            if user["child"] and user["child"]["id"] == _id:
                user["child"] = {}
                deleted = True
            _data.append(user)
        if deleted:
            self.file.save(_data)
            return {"status": Status.DELETED}
        return {"status": Status.Failed}

    def update(self, _id: str, model: ChildModel):
        data = self.file.read()
        _data = []
        updated = False
        for user in data:
            if user["child"] and user["child"]['id'] == _id:
                user["child"] = model.model_dump()
                updated = True
            _data.append(user)
        if updated:
            self.file.save(_data)
            return {"status": Status.UPDATED}
        return {"status": Status.Failed}
