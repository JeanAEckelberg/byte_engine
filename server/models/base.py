from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    This class is used in all base classes in the ``models`` folder. All models inherit from ``DeclarativeBase``, so
    this helps simplify the inheritance and import slightly.
    """
    pass
