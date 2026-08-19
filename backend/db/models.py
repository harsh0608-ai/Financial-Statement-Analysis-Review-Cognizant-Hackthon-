from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    status = Column(String, default="queued")
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Optional link to a previously-reviewed statement (e.g. last year's
    # signed filing) used for prior-year tie-out. Self-referential FK.
    linked_prior_statement_id = Column(Integer, ForeignKey("statements.id"), nullable=True)

    line_items = relationship(
        "FinancialLineItem", back_populates="statement", cascade="all, delete-orphan",
        foreign_keys="FinancialLineItem.statement_id",
    )
    findings = relationship("Finding", back_populates="statement", cascade="all, delete-orphan")


class FinancialLineItem(Base):
    __tablename__ = "financial_line_items"

    id = Column(Integer, primary_key=True, index=True)
    statement_id = Column(Integer, ForeignKey("statements.id"))
    year = Column(String, nullable=False)
    statement_type = Column(String, nullable=False)
    label = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    page_number = Column(Integer, nullable=True)

    # Hierarchy information preserved from extraction/normalization so the
    # rule engine can respect parent/child relationships instead of
    # summing every number on a page. See extraction/normalizer.py.
    table_id = Column(Integer, nullable=True)
    order_index = Column(Integer, nullable=True)
    is_total = Column(Boolean, default=False)
    group_id = Column(Integer, nullable=True)

    statement = relationship("Statement", back_populates="line_items", foreign_keys=[statement_id])


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    statement_id = Column(Integer, ForeignKey("statements.id"))
    check_type = Column(String, nullable=False)
    location = Column(String, nullable=True)
    severity = Column(String, default="medium")
    description = Column(Text, nullable=False)

    # Unified finding schema -- only the fields relevant to a given
    # check_type are populated; the rest stay null. See rules/*.py.
    reported_value = Column(Float, nullable=True)
    expected_value = Column(Float, nullable=True)
    difference = Column(Float, nullable=True)

    current_year_value = Column(Float, nullable=True)
    prior_year_value = Column(Float, nullable=True)
    percentage_change = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)

    page_number = Column(Integer, nullable=True)
    evidence = Column(Text, nullable=True)  # JSON-encoded list of {label, value, page_number}

    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    statement = relationship("Statement", back_populates="findings")
