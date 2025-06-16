CREATE DATABASE IF NOT EXISTS sklep CHARACTER SET utf8mb4 COLLATE utf8mb4_polish_ci;
USE sklep;

CREATE TABLE klienci (
    id INT PRIMARY KEY AUTO_INCREMENT,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefon VARCHAR(15)
);

CREATE TABLE produkty (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nazwa VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50) NOT NULL,
    cena DECIMAL(10,2) NOT NULL
);

CREATE TABLE zamowienia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    klient_id INT NOT NULL,
    data_zamowienia DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (klient_id) REFERENCES klienci(id)
);

CREATE TABLE pozycje_zamowienia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    zamowienie_id INT NOT NULL,
    produkt_id INT NOT NULL,
    ilosc INT NOT NULL,
    FOREIGN KEY (zamowienie_id) REFERENCES zamowienia(id),
    FOREIGN KEY (produkt_id) REFERENCES produkty(id)
);

INSERT INTO klienci (imie, nazwisko, email, telefon) VALUES
('Jan', 'Kowalski', 'jan.kowalski@email.pl', '123456789'),
('Anna', 'Nowak', 'anna.nowak@email.pl', '987654321'),
('Piotr', 'Wiśniewski', 'piotr.wisniewski@email.pl', '555666777'),
('Maria', 'Dąbrowska', 'maria.dabrowska@email.pl', '111222333'),
('Tomasz', 'Lewandowski', 'tomasz.lewandowski@email.pl', '444555666'),
('Ewa', 'Wójcik', 'ewa.wojcik@email.pl', '777888999'),
('Marek', 'Kamiński', 'marek.kaminski@email.pl', '222333444');

INSERT INTO produkty (nazwa, kategoria, cena) VALUES
('Laptop Dell', 'Elektronika', 3499.99),
('Smartfon Samsung', 'Elektronika', 1299.99),
('Biurko', 'Meble', 449.99),
('Krzesło gamingowe', 'Meble', 899.99),
('Klawiatura mechaniczna', 'Akcesoria', 299.99),
('Mysz bezprzewodowa', 'Akcesoria', 129.99),
('Monitor 27"', 'Elektronika', 999.99);

INSERT INTO zamowienia (klient_id, data_zamowienia) VALUES
(1, '2025-06-15 10:00:00'),
(2, '2025-06-15 11:30:00'),
(3, '2025-06-15 12:45:00'),
(4, '2025-06-15 14:15:00'),
(5, '2025-06-15 15:30:00'),
(1, '2025-06-15 16:45:00'),
(2, '2025-06-15 17:00:00');

INSERT INTO pozycje_zamowienia (zamowienie_id, produkt_id, ilosc) VALUES
(1, 1, 1),
(1, 5, 1),
(2, 2, 1),
(3, 3, 2),
(4, 4, 1),
(5, 6, 3),
(6, 7, 2),
(7, 2, 1);
