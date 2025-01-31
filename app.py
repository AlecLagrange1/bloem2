import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

def generate_flower_chart(scores, student_name):
    competenties_labels = list(scores.keys())
    aantallen = list(scores.values())
    
    centrum_x, centrum_y = 0, 0  # Middelpunt van de bloem
    stralen = [score * 0.8 for score in aantallen]  # Blaadjes groter maken
    hoek_offset = 360 / len(competenties_labels)  # Hoek per blaadje
    colors = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#FFD700"]
    
    fig, ax = plt.subplots(figsize=(8, 8))

    for i, (label, straal) in enumerate(zip(competenties_labels, stralen)):
        hoek = i * hoek_offset
        blaadje = patches.Wedge(center=(centrum_x, centrum_y), r=straal, 
                                theta1=hoek, theta2=hoek + hoek_offset, 
                                facecolor=colors[i % len(colors)], alpha=0.7)
        ax.add_patch(blaadje)
        
        label_x = centrum_x + straal * 1.2 * np.cos(np.radians(hoek + hoek_offset / 2))
        label_y = centrum_y + straal * 1.2 * np.sin(np.radians(hoek + hoek_offset / 2))
        ax.text(label_x, label_y, label, fontsize=12, fontweight='bold', ha='center', va='center')

    centrum = patches.Circle((centrum_x, centrum_y), 0.5, facecolor="gold", edgecolor="black")
    ax.add_patch(centrum)
    ax.text(centrum_x, centrum_y, student_name, fontsize=12, fontweight="bold", ha="center", va="center")

    ax.set_xlim(-max(stralen) - 1, max(stralen) + 1)
    ax.set_ylim(-max(stralen) - 1, max(stralen) + 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    plt.title(f"Competentie Bloem voor {student_name}", fontsize=14, fontweight='bold')
    
    return fig

def generate_pdf(student_name, scores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Competentie Bloem Rapport voor {student_name}", ln=True, align='C')
    pdf.ln(10)
    
    for key, value in scores.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)
    
    pdf_file = f"competentie_bloem_{student_name}.pdf"
    pdf.output(pdf_file)
    return pdf_file

def send_email(student_name, recipient_email, pdf_file):
    msg = EmailMessage()
    msg['Subject'] = f"Competentie Bloem Rapport voor {student_name}"
    msg['From'] = "jouw-email@example.com"
    msg['To'] = recipient_email
    
    msg.set_content(f"Beste,\n\nHierbij het competentie rapport voor {student_name}.\n\nMet vriendelijke groet,\nHet beoordelingssysteem")
    
    with open(pdf_file, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=pdf_file)
    
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login("jouw-email@example.com", "jouw-wachtwoord")
        server.send_message(msg)

st.set_page_config(page_title="Competentie Bloem Generator", page_icon="🌸", layout="wide")
st.title("🌸 Competentie Bloem Generator 🌸")

if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    st.subheader("Stap 1: Voer je gegevens in")
    student_name = st.text_input("Naam van de student", placeholder="Voornaam en achternaam")
    recipient_email = st.text_input("E-mail van de student", placeholder="student@email.com")
    if st.button("Volgende →"):
        if student_name and recipient_email:
            st.session_state["student_name"] = student_name
            st.session_state["recipient_email"] = recipient_email
            st.session_state["step"] = 2
            st.rerun()
        else:
            st.warning("Vul alle velden in.")

elif st.session_state["step"] == 2:
    st.subheader("Stap 2: Beoordeel de competenties")
    competentiegebieden = ["LERAAR/EXPERT", "KUNSTENAAR/EXPERT", "ONDERZOEKER", "ORGANISATOR", "COMMUNICATOR", "SAMENWERKER"]
    scores = {competentie: st.slider(f"{competentie}", 1, 5, 3) for competentie in competentiegebieden}
    if st.button("Genereer Bloem →"):
        st.session_state["scores"] = scores
        st.session_state["step"] = 3
        st.rerun()

elif st.session_state["step"] == 3:
    st.subheader("Stap 3: Bekijk en exporteer je competentie bloem")
    fig = generate_flower_chart(st.session_state["scores"], st.session_state["student_name"])
    st.pyplot(fig)
    pdf_file = generate_pdf(st.session_state["student_name"], st.session_state["scores"])
    st.download_button("📄 Download PDF Rapport", open(pdf_file, "rb"), file_name=pdf_file, mime="application/pdf")
    if st.button("✉️ Verstuur per e-mail"):
        send_email(st.session_state["student_name"], st.session_state["recipient_email"], pdf_file)
        st.success("📧 E-mail succesvol verzonden!")
