import sqlite3
import pandas as pd

# Dataframe
data = {
    'Nama': ['Ani', 'Budi', 'Cici', 'Dedi', 'Euis', 'Fafa', 'Gigi', 'Hadi', 'Ina', 'Joko', 'Kiki', 'Lala', 'Mimi', 'Nana', 'Opi', 'Pipi', 'Qiqi', 'Riri', 'Sisi', 'Titi', 'Uci', 'Vivi', 'Wati', 'Xena', 'Yuni', 'Zara'],
    'NIM': ['12345', '67890', '54321', '13579', '24680', '35791', '46802', '57913', '68024', '79135', '80246', '91357', '02468', '13579', '24680', '35791', '46802', '57913', '68024', '79135', '80246', '91357', '02468', '13579', '24680', '35791'],
    'Gender': ['Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki'],
    'Kontak': ['08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789', '08123456789'],
    'Jurusan': ['IT', 'ELEKTRO', 'DS', 'TELKOM', 'GAME', 'IT', 'ELEKTRO', 'DS', 'TELKOM', 'GAME', 'IT', 'ELEKTRO', 'DS', 'TELKOM', 'GAME', 'IT', 'ELEKTRO', 'DS', 'TELKOM', 'GAME', 'IT', 'ELEKTRO', 'DS', 'TELKOM', 'GAME', 'IT'],
    'Semester': [8, 6, 4, 8, 4, 8, 6, 4, 8, 4, 8, 6, 4, 8, 6, 4, 8, 6, 4, 8, 6, 4, 8, 6, 4, 8],
    'UTS': [75, 80, 85, 88, 85, 80, 85, 80, 85, 90, 75, 80, 85, 80, 85, 80, 85, 78, 85, 90, 75, 80, 85, 80, 85, 80],
    'UAS': [95, 90, 85, 90, 95, 90, 100, 90, 95, 90, 95, 90, 85, 90, 95, 90, 100, 90, 95, 90, 95, 90, 85, 90, 95, 90]
}

# Membuat dataframe
df = pd.DataFrame(data)

# Menghubungkan ke database SQLite
conn = sqlite3.connect('mahasiswa.db')

# Menyimpan dataframe ke dalam database SQLite
df.to_sql('mahasiswa', conn, if_exists='replace', index=False)

# Menutup koneksi
conn.close()