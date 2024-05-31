import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns

# Initiate Database
conn = sqlite3.connect('mahasiswa.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Mahasiswa
             (Nama TEXT, NIM TEXT, Gender TEXT, Kontak TEXT, Jurusan TEXT, Semester INTEGER, UTS INTEGER, UAS INTEGER)''')

# Python OOP
class Mahasiswa:
    # Encapsulation
    def __init__(self, name, nim, gender, kontak, uts, uas):
        self._name = name
        self._nim = nim
        self._gender = gender
        self._kontak = kontak
        self._uts = uts
        self._uas = uas

# Polymorphism
class D3(Mahasiswa):
    def __init__(self, name, nim, gender, kontak, uts, uas):
        # Inheritance
        super().__init__(name, nim, gender, kontak, uts, uas)
        self._lama_kuliah = 6
        self._program = ['IT', 'ELEKTRO']

    # Getter methods specific to D3
    def get_lama_kuliah(self):
        return self._lama_kuliah

    def get_program(self):
        return self._program

class D4(Mahasiswa):
    def __init__(self, name, nim, gender, kontak, uts, uas):
        super().__init__(name, nim, gender, kontak, uts, uas)
        self._lama_kuliah = 8
        self._program = ['IT', 'ELEKTRO','DS', 'TELKOM', 'GAME']

    # Getter methods specific to D4
    def get_lama_kuliah(self):
        return self._lama_kuliah

    def get_program(self):
        return self._program

class S2(Mahasiswa):
    def __init__(self, name, nim, gender, kontak, uts, uas):
        super().__init__(name, nim, gender, kontak, uts, uas)
        self._lama_kuliah = 4
        self._program = ['IT','ELEKTRO']

    # Getter methods specific to S2
    def get_lama_kuliah(self):
        return self._lama_kuliah

    def get_program(self):
        return self._program

# Fitur login
def creds_entered():
    list_user = ["admin"]
    list_passwd = ["admin"]
    if st.session_state["user"].strip() in list_user and st.session_state["passwd"].strip() in list_passwd:
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if not st.session_state["passwd"]:
            st.warning("Please enter password.")
        elif not st.session_state["user"]:
            st.warning("Please enter username.")
        else:
            st.error("Username/Password Salah :face_with_raised_eyebrow")

# user autentifikasi
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label='Username: ', value="", key="user", on_change=creds_entered)
        st.text_input(label='Password: ', value="", key="passwd", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label='Username: ', value="", key="user", on_change=creds_entered)
            st.text_input(label='Password: ', value="", key="passwd", type="password", on_change=creds_entered)
            return False

# Front End
st.title('📚WEBSITE MANAJEMEN HIMIT✅')

if authenticate_user():
    # Input data
    pilihan_mahasiswa = st.radio('Pilih Mahasiswa', ['D3', 'D4'])
    name = st.text_input('Nama Mahasiswa')
    nim = st.text_input('NIM Mahasiswa')
    gender = st.selectbox('Gender Mahasiswa', ['Laki-laki', 'Perempuan'])
    kontak = st.text_input('Kontak Mahasiswa')
    uts = st.number_input('Nilai UTS', min_value=0, max_value=100)
    uas = st.number_input('Nilai UAS', min_value=0, max_value=100)

    # Buat objek mahasiswa
    if pilihan_mahasiswa == 'D3':
        student = D3(name, nim, gender, kontak, uts, uas)
        jurusan = st.selectbox('Jurusan', student.get_program())
        semester = student.get_lama_kuliah()
    elif pilihan_mahasiswa == 'D4':
        student = D4(name, nim, gender, kontak, uts, uas)
        jurusan = st.selectbox('Jurusan', student.get_program())
        semester = student.get_lama_kuliah()

    list_mahasiswa = st.session_state.get('list_mahasiswa', [])
    
    # Button
    if st.button('Simpan Mahasiswa'):
        # Insert data into database
        c.execute("INSERT INTO Mahasiswa (Nama, NIM, Gender, Kontak, Jurusan, Semester, UTS, UAS) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, nim, gender, kontak, jurusan, semester, uts, uas))
        conn.commit()

    # Retrieve data from database
    c.execute("SELECT * FROM Mahasiswa")
    rows = c.fetchall()

    # Show tabel
    df = pd.DataFrame(rows, columns=['Nama', 'NIM', 'Gender', 'Kontak', 'Jurusan', 'Total Semester', 'Nilai UTS', 'Nilai UAS'])
    st.table(df)
    
    # Show plot visualization
    if st.button('Plot Nilai UTS UAS'):
        # Plot 1: Rata-rata Nilai UTS dan UAS Tiap Total Semester
        rata_rata_nilai = df.groupby('Total Semester')[['Nilai UTS', 'Nilai UAS']].mean().reset_index()
        fig1 = go.Figure()

        fig1.add_trace(go.Bar(
            x=rata_rata_nilai['Total Semester'].replace({4: 'S2', 6: 'D3', 8: 'D4'}),
            y=rata_rata_nilai['Nilai UTS'],
            name='Rata-rata UTS',
            marker_color='blue'
        ))

        fig1.add_trace(go.Bar(
            x=rata_rata_nilai['Total Semester'].replace({4: 'S2', 6: 'D3', 8: 'D4'}),
            y=rata_rata_nilai['Nilai UAS'],
            name='Rata-rata UAS',
            marker_color='red'
        ))

        fig1.update_layout(
            title='Rata-rata Nilai UTS dan UAS Tiap Total Semester',
            xaxis_title='Jenjang Pendidikan',
            yaxis_title='Rata-rata Nilai',
            barmode='group'
        )
        st.plotly_chart(fig1)
        
        # Plot 2: Jumlah Mahasiswa per Jurusan
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Jurusan', data=df, color='red')
        plt.title('Jumlah Mahasiswa per Jurusan')
        plt.xlabel('Jurusan')
        plt.ylabel('Jumlah Mahasiswa')
        plt.gca().patch.set_alpha(0)  # Set background to transparent
        st.pyplot(plt.gcf())

        # Plot 3: Distribusi Penyebaran Nilai UTS dan UAS
        trace_uts = go.Histogram(x=df['Nilai UTS'], name='UTS', opacity=0.75)
        trace_uas = go.Histogram(x=df['Nilai UAS'], name='UAS', opacity=0.75)

        layout = go.Layout(
            title='Distribusi Penyebaran Nilai UTS dan UAS',
            xaxis=dict(title='Nilai', showgrid=False),
            yaxis=dict(title='Jumlah Mahasiswa', showgrid=False),
            bargap=0.2,
            bargroupgap=0.1
        )

        fig2 = go.Figure(data=[trace_uts, trace_uas], layout=layout)
        st.plotly_chart(fig2)
conn.close()