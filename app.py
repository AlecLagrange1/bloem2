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

st.set_page_config(page_title="Competentie Bloem Generator", page_icon="🌸", layout="wide")
st.title("🌸 Competentie Bloem Generator 🌸")

competentie_clusters = {
    "LERAAR/EXPERT": [
        "Kan een positief, veilig en creatief leerklimaat creëren",
        "Kan verschillende werkvormen en groeperingsvormen toepassen",
        "Kan motiveren, uitdagen, activeren en stimuleren tot creativiteit",
        "Kan opdrachten helder formuleren, gerichte vragen stellen en doorvragen",
        "Gebruikt een logische opbouw en structuur",
        "Kan differentiëren in aanpak naargelang de noden",
        "Stimuleert tot zelfstandigheid en kritische reflectie",
        "Kan digitale leermiddelen inzetten",
        "Kan reflecteren over proces en product en dit evalueren",
        "Geeft positieve bekrachtiging en opbouwende feedback",
        "Heeft een groot aanpassingsvermogen"
    ]
}

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
    scores = {}
    for cluster, competenties in competentie_clusters.items():
        st.markdown(f"### {cluster}")
        for competentie in competenties:
            scores[competentie] = st.slider(f"{competentie}", 1, 5, 3)
    if st.button("Genereer Bloem →"):
        st.session_state["scores"] = scores
        st.session_state["step"] = 3
        st.rerun()

elif st.session_state["step"] == 3:
    st.subheader("Stap 3: Bekijk en exporteer je competentie bloem")
    fig = generate_flower_chart(st.session_state["scores"], st.session_state["student_name"])
    st.pyplot(fig)
    pdf_file = f"competentie_bloem_{st.session_state['student_name']}.pdf"
    st.download_button("📄 Download PDF Rapport", open(pdf_file, "rb"), file_name=pdf_file, mime="application/pdf")
