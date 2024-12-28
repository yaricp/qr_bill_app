from uuid import uuid4
from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Boolean,
    UUID, DateTime
)

from .metadata import mapper_registry


partners_table = Table(
    "partners",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    ),
    Column("name", String, nullable=False, unique=True),
    Column("address", String, nullable=False),
    Column("email", String, nullable=False),
    Column("phone", String, nullable=False),
)

attractions_table = Table(
    "attractions",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("name", String, nullable=False),
    Column("location", String, nullable=False),
    Column("link_to_attraction_domain", String),
    Column("work_status", String, nullable=False),
    Column(
        "partner_id", UUID,
        ForeignKey(
            "partners.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
)

lisenses_table = Table(
    "lisenses",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("type", String, nullable=False),
    Column("status", String, nullable=False),
    Column("activated", DateTime, nullable=True),
    Column("expirated", DateTime, nullable=True),
    Column("created", DateTime, nullable=False),
    Column("expiration", DateTime, nullable=True),
    Column("count_packages", Integer, nullable=True),
    Column(
        "partner_id", UUID,
        ForeignKey("partners.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    ),
    Column("attraction_id", UUID, nullable=True)
)

attraction_statistic_row_table = Table(
    "attraction_statistic_rows",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("created", DateTime, nullable=False),
    Column("count_packages", Integer, nullable=False),
    Column(
        "attraction_id", UUID,
        ForeignKey("attractions.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
)

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("user_id", UUID, primary_key=True, nullable=False, unique=True),
    Column("partner_id", UUID, nullable=True),
    Column("attraction_id", UUID, nullable=True),
    Column("email", String, nullable=True),
    Column("tg_id", String, nullable=True),
    Column("superadmin", Boolean, default=False)
)


def start_mappers():
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from ...domain.entities.partner_entity import (
        PartnerEntity
    )
    from ...domain.entities.attraction_entity import (
        AttractionEntity
    )
    from ...domain.entities.attractaction_stat_row_entity import (
        AttractionStatisticRowEntity
    )
    from ...domain.entities.license_entity import (
        LicenseEntity
    )
    from ...domain.entities.user_entity import (
        UserEntity
    )

    mapper_registry.map_imperatively(
        class_=PartnerEntity, local_table=partners_table
    )
    mapper_registry.map_imperatively(
        class_=AttractionEntity, local_table=attractions_table
    )
    mapper_registry.map_imperatively(
        class_=AttractionStatisticRowEntity,
        local_table=attraction_statistic_row_table
    )
    mapper_registry.map_imperatively(
        class_=LicenseEntity, local_table=lisenses_table
    )
    mapper_registry.map_imperatively(
        class_=UserEntity, local_table=users_table
    )
