from pydantic import BaseModel, Field

from app.core.enums import OperationType


class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: int = Field(gt=0, description="Amount must be positive!")
