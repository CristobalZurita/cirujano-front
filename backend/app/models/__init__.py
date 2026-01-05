"""
SQLAlchemy ORM Models
Define database schema for Cirujano de Sintetizadores
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Brand(Base):
    """
    Marca de sintetizador
    Ej: Moog, Sequential, Oberheim
    """
    __tablename__ = "brands"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    tier = Column(String(20))  # legendary, professional, standard, specialized, boutique, historic
    founded = Column(Integer)
    country = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    instruments = relationship("Instrument", back_populates="brand")

    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name}, tier={self.tier})>"


class Instrument(Base):
    """
    Instrumento/Modelo de sintetizador
    Ej: Moog Mother-32, Sequential Prophet-5
    """
    __tablename__ = "instruments"

    id = Column(String(100), primary_key=True, index=True)
    brand_id = Column(String(50), ForeignKey("brands.id"), index=True)
    model = Column(String(100), index=True)
    type = Column(String(50))  # Synthesizer, Sampler, Drum Machine, etc.
    year = Column(Integer)
    description = Column(Text)
    components = Column(JSON)  # Audio outputs, MIDI, etc.
    valor_min = Column(Float)  # Minimum estimated value (CLP)
    valor_max = Column(Float)  # Maximum estimated value (CLP)
    fallas_comunes = Column(JSON)  # List of common fault IDs
    imagen_url = Column(String(255))
    manual_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    brand = relationship("Brand", back_populates="instruments")
    repairs = relationship("Repair", back_populates="instrument")

    def __repr__(self):
        return f"<Instrument(id={self.id}, model={self.model}, brand={self.brand_id})>"


class Fault(Base):
    """
    Tipo de falla/problema
    Ej: POWER, AUDIO_NO_OUTPUT, MIDI_NOT_RECOGNIZED
    """
    __tablename__ = "faults"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    base_price = Column(Float)  # Precio base de diagnóstico/reparación (CLP)
    is_precedence = Column(Boolean, default=False)  # Si es crítica, prevalece sobre otras
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    repairs = relationship("RepairDetail", back_populates="fault")

    def __repr__(self):
        return f"<Fault(id={self.id}, name={self.name}, price={self.base_price})>"


class Diagnostic(Base):
    """
    Cotización/Diagnóstico solicitada por cliente
    """
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), index=True)
    client_email = Column(String(100), index=True)
    client_phone = Column(String(20))
    brand_id = Column(String(50), ForeignKey("brands.id"))
    instrument_id = Column(String(100), ForeignKey("instruments.id"))
    faults_json = Column(JSON)  # {fault_id: true, ...}
    estimated_cost = Column(Float)  # Cotización calculada
    status = Column(String(20), default="pending")  # pending, confirmed, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brand = relationship("Brand")
    instrument = relationship("Instrument")

    def __repr__(self):
        return f"<Diagnostic(id={self.id}, email={self.client_email}, cost={self.estimated_cost})>"


class Repair(Base):
    """
    Reparación completada - para historial de reparaciones
    """
    __tablename__ = "repairs"

    id = Column(Integer, primary_key=True, index=True)
    diagnostic_id = Column(Integer, ForeignKey("diagnostics.id"))
    instrument_id = Column(String(100), ForeignKey("instruments.id"), index=True)
    brand_id = Column(String(50), ForeignKey("brands.id"))
    client_name = Column(String(100))
    client_email = Column(String(100))
    actual_cost = Column(Float)  # Costo real después de completada
    hours_worked = Column(Float)  # Horas invertidas
    notes = Column(Text)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    instrument = relationship("Instrument", back_populates="repairs")
    details = relationship("RepairDetail", back_populates="repair")

    def __repr__(self):
        return f"<Repair(id={self.id}, instrument={self.instrument_id}, cost={self.actual_cost})>"


class RepairDetail(Base):
    """
    Detalle de fallas reparadas en una reparación
    """
    __tablename__ = "repair_details"

    id = Column(Integer, primary_key=True, index=True)
    repair_id = Column(Integer, ForeignKey("repairs.id"), index=True)
    fault_id = Column(String(50), ForeignKey("faults.id"))
    description = Column(Text)  # Descripción específica de lo que se hizo
    parts_used = Column(JSON)  # Lista de partes usadas {name, cost, ...}
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    repair = relationship("Repair", back_populates="details")
    fault = relationship("Fault", back_populates="repairs")

    def __repr__(self):
        return f"<RepairDetail(id={self.id}, fault={self.fault_id})>"
