from sqlalchemy import Column, Integer, String, Text, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(50), unique=True, nullable=False)

    jobs = relationship("Job", back_populates="country")


class DataSource(Base):
    __tablename__ = "data_sources"

    source_id = Column(Integer, primary_key=True)
    source_name = Column(String(255), nullable=False)
    reliability = Column(String(255))
    limitation = Column(Text)

    jobs = relationship("Job", back_populates="source")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    original_title = Column(String(255), nullable=False)
    normalized_title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    category = Column(String(100))
    sub_category = Column(String(150))
    role_type = Column(String(50), nullable=True)
    salary_raw = Column(String(255))
    salary_min = Column(Numeric(12, 2))
    salary_max = Column(Numeric(12, 2))
    currency = Column(String(10))
    salary_period = Column(String(10))
    posting_date = Column(Date, nullable=True)
    source_id = Column(Integer, ForeignKey("data_sources.source_id"))

    country = relationship("Country", back_populates="jobs")
    source = relationship("DataSource", back_populates="jobs")
