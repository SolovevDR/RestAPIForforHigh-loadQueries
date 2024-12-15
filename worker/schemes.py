from pydantic import BaseModel, field_validator


class EngineV1Params(BaseModel):
    param_1: str | None = None
    param_2: float | None = None
    param_3: bool | None = None

    @field_validator("param_1")
    def validate_param_1(cls, param_1: str):
        if param_1:
            return f"--param_1 {param_1}"
        return None

    @field_validator("param_2")
    def validate_param_2(cls, param_2: float):
        if param_2 is not None:
            return f"--param_2 {param_2}"
        return None

    @field_validator("param_3")
    def validate_param_3(cls, param_3: bool):
        if param_3 is not None:
            return f"--param_3 {param_3}"
        return None

    class Config:
        exclude_none = True


class EngineV2Params(BaseModel):
    param_1: str | None = None
    param_2: float | None = None

    @field_validator("param_1")
    def validate_param_1(cls, param_1: str):
        if param_1:
            return f"--param_1 {param_1}"
        return None

    @field_validator("param_2")
    def validate_param_2(cls, param_2: float):
        if param_2 is not None:
            return f"--param_2 {param_2}"
        return None

    class Config:
        exclude_none = True
