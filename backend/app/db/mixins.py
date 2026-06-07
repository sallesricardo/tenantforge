import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column


class TimestampMixin:
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class UUIDMixin:
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TenantMixin:
    tenant_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
