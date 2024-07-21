CREATE TABLE buku (
    id SERIAL PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(255) NOT NULL,
    penerbit VARCHAR(255) NOT NULL,
    tahun_terbit INT NOT NULL,
    konten TEXT NOT NULL,
    iktisar TEXT NOT NULL
);
