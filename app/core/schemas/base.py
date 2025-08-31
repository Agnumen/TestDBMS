from pydantic import BaseModel as BaseModel_, ConfigDict

class BaseModel(BaseModel_):
    model_config = ConfigDict(
        use_enum_values = True,
        from_attributes = True,
    )
