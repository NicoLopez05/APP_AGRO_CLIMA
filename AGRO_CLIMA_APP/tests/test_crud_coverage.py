# tests/test_crud_coverage.py

from app import crud, models, schemas
from app.database import SessionLocal
from sqlalchemy.orm import Session
import pytest

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_sensor(db: Session):
    data = schemas.SensorCreate(
        nombre="Sensor Test",
        tipo="Humedad",
        ubicacion="Campo A",
        zona="Zona 1",
        cultivo="Papa"
    )
    sensor = crud.create_sensor(db, data)
    assert sensor.nombre == "Sensor Test"

def test_get_sensores(db: Session):
    sensores = crud.get_sensores(db)
    assert isinstance(sensores, list)

def test_get_sensor(db: Session):
    sensores = crud.get_sensores(db)
    if sensores:
        sensor = crud.get_sensor(db, sensores[0].id)
        assert sensor is not None

def test_update_sensor(db: Session):
    sensores = crud.get_sensores(db)
    if sensores:
        sensor = sensores[0]
        data = schemas.SensorUpdate(
            nombre="Nuevo Nombre",
            tipo=sensor.tipo,
            ubicacion=sensor.ubicacion,
            zona=sensor.zona,
            cultivo=sensor.cultivo
        )
        updated = crud.update_sensor(db, sensor.id, data)
        assert updated.nombre == "Nuevo Nombre"

def test_delete_sensor(db: Session):
    sensores = crud.get_sensores(db)
    if sensores:
        sensor = sensores[0]
        deleted = crud.delete_sensor(db, sensor.id)
        assert deleted is True or deleted is not None

def update_sensor(db: Session, sensor_id: int, sensor_update: schemas.SensorUpdate):
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        return None

    for field, value in sensor_update.model_dump().items():
        setattr(sensor, field, value)
    
    db.commit()
    db.refresh(sensor)
    return sensor


