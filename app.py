import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import smtplib
import sqlite3
from email.message import EmailMessage
from fpdf import FPDF

def generate_flower_chart(scores, student_name):
    competenties_labels = list(scores.keys())
    aantallen = list(scores.values())
    
    # Instellingen voor de bloem
    centrum_x, centrum_y = 0, 0  # Middelpunt van de bloem
    stralen = [score * 0.8 for score in aantallen]  # Blaadjes groter maken
    hoek_offset = 360 / len(competenties_labels)  # Hoek per blaadje
    colors = ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#FFD700"]
    
    fig, ax = plt.subplots(figsize=(8, 8))

    # Maak de blaadjes
    for i, (label, straal) in enumerate(zip(competenties_labels, stralen)):
        hoek = i * hoek_offset
        blaadje = patches.Wedge(center=(centrum_x, centrum_y), r=straal, 
                                theta1=hoek, theta2=hoek + hoek_offset, 
                                facecolor=colors[i % len(colors)], alpha=0.7)
        ax.add_patch(blaadje)
        
        # Voeg labels toe aan de uiteinden van de blaadjes
        label_x = centrum_x + straal * 1.2 * np.cos(np.radians(hoek + hoek_offset / 2))
        label_y = centrum_y + straal * 1.2 * np.sin(np.radians(hoek + hoek_offset / 2))
        ax.text(label_x, label_y, label, fontsize=12, fontweight='bold', ha='center', va='center')

    # Voeg een cirkel in het midden toe (hart van de bloem)
    centrum = patches.Circle((centrum_x, centrum_y), 0.5, facecolor="gold", edgecolor="black")
    ax.add_patch(centrum)
    ax.text(centrum_x, centrum_y, student_name, fontsize=12, fontweight="bold", ha="center", va="center")

    # Verwijder assen voor een schone presentatie
    ax.set_xlim(-max(stralen) - 1, max(stralen) + 1)
    ax.set_ylim(-max(stralen) - 1, max(stralen) + 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # Titel
    plt.title(f"Competentie Bloem voor {student_name}", fontsize=14, fontweight='bold')
    
    return fig

st.set_page_config(page_title="Competentie Bloem Generator", page_icon="🌸", layout="wide")
st.title("🌸 Competentie Bloem Generator 🌸")

# Downloadknop voor de code
code = '''import streamlit as st\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport matplotlib.patches as patches\nfrom io import BytesIO\nimport smtplib\nimport sqlite3\nfrom email.message import EmailMessage\nfrom fpdf import FPDF\n\n# De volledige code die hierboven staat\n'''
st.download_button("📥 Download de Code", code, file_name="app.py", mime="text/plain")
