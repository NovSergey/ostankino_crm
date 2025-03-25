# from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
#
# from .base import Base
#
# employee_position_association_table = Table(
#     "employee_position_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("employee_id", ForeignKey("employees.id"), nullable=False),
#     Column("position_id", ForeignKey("positions.id"), nullable=False)
# )