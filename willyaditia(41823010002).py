from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///buku.db')
Session = sessionmaker(bind=engine)
session = Session()

class Buku:
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, iktisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.iktisar = iktisar

    def read(self, halaman):
        if halaman > len(self.konten):
            halaman = len(self.konten)
        for i in range(halaman):
            print(f"Bab {i + 1}: {self.konten[i]}")

    def __str__(self):
        return f"{self.judul} by {self.penulis}"

class BukuDB(Base):
    __tablename__ = 'buku'
    id = Column(Integer, primary_key=True)
    judul = Column(String, nullable=False)
    penulis = Column(String, nullable=False)
    penerbit = Column(String, nullable=False)
    tahun_terbit = Column(Integer, nullable=False)
    konten = Column(Text, nullable=False)
    iktisar = Column(Text, nullable=False)

Base.metadata.create_all(engine)

def get_buku(id):
    try:
        buku = session.query(BukuDB).filter_by(id=id).first()
        if buku:
            return buku
        else:
            logger.error("Buku tidak ditemukan")
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    except Exception as e:
        logger.error(f"Error fetching buku: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_buku(buku):
    try:
        buku_db = BukuDB(
            judul=buku.judul,
            penulis=buku.penulis,
            penerbit=buku.penerbit,
            tahun_terbit=buku.tahun_terbit,
            konten=",".join(buku.konten),
            iktisar=buku.iktisar
        )
        session.add(buku_db)
        session.commit()
        logger.info("Buku berhasil disimpan")
    except Exception as e:
        logger.error(f"Error saving buku: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

class HTTPException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)

    def __str__(self):
        return f"HTTP {self.status_code}: {self.detail}"

# Example usage
if __name__ == "__main__":
    # Example book
    buku = Buku(
        judul="Python Programming",
        penulis="John Doe",
        penerbit="Tech Books",
        tahun_terbit=2020,
        konten=["Introduction", "Variables", "Data Types", "Control Flow", "Functions"],
        iktisar="This book provides an introduction to Python programming..."
    )
    post_buku(buku)
    buku_db = get_buku(1)
    if buku_db:
        print(buku_db.judul, buku_db.penulis)
