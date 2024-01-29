from pydantic import BaseModel


class TenantSchema(BaseModel):
    id: str  # noqa: A003
    external_id: str
    organization_id: int
    email_address: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
