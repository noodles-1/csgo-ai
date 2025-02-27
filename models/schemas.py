from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    '''
    User table with columns ID (PK), email, username, full name, is admin, and privilege
    to change vehicles to detect, congestion prices, edit hours, and download CSV.
    '''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50))
    firstName: Mapped[str] = mapped_column(String(80))
    lastName: Mapped[str] = mapped_column(String(80))
    isAdmin: Mapped[bool]
    canChangeDetect: Mapped[bool]
    canChangePrice: Mapped[bool]
    canEditHours: Mapped[bool]
    canDownload: Mapped[bool]
    password: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'User(userId={self.id}, email={self.email}, username={self.username}, fullName={self.firstName} {self.lastName}, isAdmin={self.isAdmin})'
    
class Camera(Base):
    '''
    Camera table with columns ID containing the IP address (PK) and the camera name.
    '''
    __tablename__ = 'camera'

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(50))
    originCoords: Mapped[str] = mapped_column(String(255))
    destCoords: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'Camera(cameraId={self.id}, name={self.name}, location={self.location}, origin={self.originCoords}, destination={self.destCoords})'

class DetectedLicensePlate(Base):
    '''
    DetectedLicensePlate table with columns ID (PK), user ID (FK from User), camera ID (FK from Camera),
    license number, vehicle type, and datetime of detection.
    '''
    __tablename__ = 'detected_license_plate'

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey('user.id'))
    settingId: Mapped[int]
    location: Mapped[str] = mapped_column(String(255))
    licenseNumber: Mapped[str] = mapped_column(String(14))
    vehicleType: Mapped[str] = mapped_column(String(20))
    price: Mapped[float]
    date: Mapped[Date] = mapped_column(Date())
    time: Mapped[Time] = mapped_column(Time(timezone=True))
    image: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'Detection(id={self.id}, userId={self.userId}, setting={self.settingId}, location={self.location}, licenseNumber={self.licenseNumber}, vehicleType={self.vehicleType}, price={self.price}, date={self.date}, time={self.time}, image={self.image})'
    
class CurrentSetting(Base):
    '''
    Setting table that contains current different settings for the congestion pricing system.
    '''
    __tablename__ = 'current_setting'

    id: Mapped[int] = mapped_column(primary_key=True)
    hourFrom: Mapped[Time] = mapped_column(Time(timezone=True))
    hourTo: Mapped[Time] = mapped_column(Time(timezone=True))
    day: Mapped[str] = mapped_column(String(20))
    detectCar: Mapped[bool]
    detectMotorcycle: Mapped[bool]
    detectBus: Mapped[bool]
    detectTruck: Mapped[bool]
    carPrice: Mapped[float]
    motorcyclePrice: Mapped[float]
    busPrice: Mapped[float]
    truckPrice: Mapped[float]

    def __repr__(self) -> str:
        return f'Setting(settingId={self.id}, hourFrom={self.hourFrom}, hourTo={self.hourTo}, day={self.day}, detectMotorcycle={self.detectMotorcycle}, detectBus={self.detectBus}, detectTruck={self.detectTruck}, carPrice={self.carPrice}, motorcyclePrice={self.motorcyclePrice}, busPrice={self.busPrice}, truckPrice={self.truckPrice})'
    
class FutureSetting(Base):
    '''
    Setting table that contains future different settings for the congestion pricing system.
    '''
    __tablename__ = 'future_setting'

    id: Mapped[int] = mapped_column(primary_key=True)
    hourFrom: Mapped[Time] = mapped_column(Time(timezone=True))
    hourTo: Mapped[Time] = mapped_column(Time(timezone=True))
    day: Mapped[str] = mapped_column(String(20))
    startDate: Mapped[Date] = mapped_column(Date())
    startTime: Mapped[Time] = mapped_column(Time(timezone=True))
    detectCar: Mapped[bool]
    detectMotorcycle: Mapped[bool]
    detectBus: Mapped[bool]
    detectTruck: Mapped[bool]
    carPrice: Mapped[float]
    motorcyclePrice: Mapped[float]
    busPrice: Mapped[float]
    truckPrice: Mapped[float]

    def __repr__(self) -> str:
        return f'Setting(settingId={self.id}, hourFrom={self.hourFrom}, hourTo={self.hourTo}, day={self.day}, startDate={self.startDate}, detectCar={self.detectCar}, detectMotorcycle={self.detectMotorcycle}, detectBus={self.detectBus}, detectTruck={self.detectTruck}, carPrice={self.carPrice}, motorcyclePrice={self.motorcyclePrice}, busPrice={self.busPrice}, truckPrice={self.truckPrice})'
    
class Congestion(Base):
    '''
    Congestion table that contains the congestion rate (from 0 to 1) of a location
    along with its timestamp.
    '''

    __tablename__ = 'congestion'

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String(50))
    congestion: Mapped[float]
    date: Mapped[Date] = mapped_column(Date())
    time: Mapped[Time] = mapped_column(Time(timezone=True))

    def __repr__(self) -> str:
        return f'Congestion(id={self.id}, location={self.location}, congestion={self.congestion}, date={self.date}, time={self.time})'