from pydantic.json_schema import (
    DEFAULT_REF_TEMPLATE,
    GenerateJsonSchema,
    JsonSchemaMode,
    model_json_schema,
)
from typing import Any
from pydantic import BaseModel, Field
from openai.lib._pydantic import _ensure_strict_json_schema


class BaseModelOpenAI(BaseModel):
    @classmethod
    def model_json_schema(
        cls,
        by_alias: bool = True,
        ref_template: str = DEFAULT_REF_TEMPLATE,
        schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
        mode: JsonSchemaMode = "serialization",
    ) -> dict[str, Any]:
        json_schema = model_json_schema(
            cls,
            by_alias=by_alias,
            ref_template=ref_template,
            schema_generator=schema_generator,
            mode=mode,
        )
        return _ensure_strict_json_schema(json_schema, path=(), root=json_schema)
