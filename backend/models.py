from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database import Base # Import Base from the new database.py

class UserManifesto(Base):
    __tablename__ = "user_manifestos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="Anonymous")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Human Design Chart Fields
    birth_datetime_utc = Column(DateTime, nullable=True)
    birth_latitude = Column(Float, nullable=True)
    birth_longitude = Column(Float, nullable=True)
    birth_timezone_str = Column(String, nullable=True)
    chart_type = Column(String, nullable=True)
    chart_strategy = Column(String, nullable=True)
    chart_inner_authority = Column(String, nullable=True)
    chart_profile = Column(String, nullable=True)
    chart_incarnation_cross = Column(Text, nullable=True)
    chart_data_json = Column(Text, nullable=True) # To store the full JSON response of HumanDesignChartResponse