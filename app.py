import streamlit as st
import json
import datetime
import sqlite3
import uuid
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurazione pagina
st.set_page_config(
    page_title="IntelliCall Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializzazione session state
if 'chiamate' not in st.session_state:
    st.session_state.chiamate = []
if 'clienti' not in st.session_state:
    st.session_state.clienti = []
if 'voicemail' not in st.session_state:
    st.session_state.voicemail = []
if 'statistiche' not in st.session_state:
    st.session_state.statistiche = {
        'chiamate_oggi': 0,
        'voicemail_da_ascoltare': 0,
        'soddisfazione_media': 0.0
    }

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .urgent {
        border-left: 5px solid #ff4757;
    }
    .high {
        border-left: 5px solid #ffa502;
    }
    .medium {
        border-left: 5px solid #2ed573;
    }
</style>
""", unsafe_allow_html=True)

# Titolo
st.markdown('<h1 class="main-header">🤖 IntelliCall Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Segreteria Telefonica AI Professionale")

# Layout con colonne
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Chiamate Oggi", st.session_state.statistiche['chiamate_oggi'], "+12")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Voicemail da Ascoltare", st.session_state.statistiche['voicemail_da_ascoltare'], "3 urgenti")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Soddisfazione Media", f"{st.session_state.statistiche['soddisfazione_media']}%", "+2.5%")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabs principale
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📞 Dashboard", 
    "📱 Simula Chiamata", 
    "🎙️ Voicemail", 
    "👥 Clienti", 
    "⚙️ Configurazione"
])

# Tab 1: Dashboard
with tab1:
    st.header("📊 Dashboard in Tempo Reale")
    
    # Grafico chiamate
    fig = go.Figure(data=[
        go.Bar(
            x=['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
            y=[12, 19, 15, 22, 18, 14, 21, 17],
            name='Chiamate'
        )
    ])
    fig.update_layout(
        title='Distribuzione Chiamate per Ora',
        xaxis_title='Ora',
        yaxis_title='Numero Chiamate'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Ultime chiamate
    st.subheader("📞 Ultime Chiamate")
    if st.button("🔄 Aggiorna", key="refresh_calls"):
        st.rerun()
    
    # Tabella chiamate
    data = {
        'Ora': ['09:15', '10:30', '11:45', '13:20', '14:35'],
        'Cliente': ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Giulia Neri', 'Paolo Gialli'],
        'Numero': ['+39 123456789', '+39 987654321', '+39 456123789', '+39 789456123', '+39 321654987'],
        'Durata': ['2:15', '5:30', '1:45', '3:20', '4:10'],
        'Stato': ['✅ Completata', '⏳ In attesa', '✅ Completata', '❌ Fallita', '✅ Completata']
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Tab 2: Simula Chiamata
with tab2:
    st.header("📱 Simula Chiamata in Entrata")
    
    col1, col2 = st.columns(2)
    
    with col1:
        numero = st.text_input("Numero Chiamante", "+39 123 456 7890")
        nome = st.text_input("Nome Cliente", "Mario Rossi")
        tipo_cliente = st.selectbox(
            "Tipo Cliente",
            ["Nuovo", "Regolare", "VIP", "Aziendale"]
        )
    
    with col2:
        priorita = st.select_slider(
            "Priorità",
            options=["Bassa", "Media", "Alta", "Urgente"],
            value="Media"
        )
        motivo = st.text_area("Motivo Chiamata", "Richiesta informazioni su prodotti")
    
    if st.button("📞 Simula Chiamata", type="primary", use_container_width=True):
        nuova_chiamata = {
            'id': str(uuid.uuid4())[:8],
            'data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            'numero': numero,
            'nome': nome,
            'tipo': tipo_cliente,
            'priorita': priorita,
            'motivo': motivo
        }
        
        st.session_state.chiamate.append(nuova_chiamata)
        st.session_state.statistiche['chiamate_oggi'] += 1
        
        st.success(f"✅ Chiamata simulata con ID: {nuova_chiamata['id']}")
        
        # Mostra risposta automatica
        st.info("""
        **🤖 Risposta Automatica Generata:**
        
        "Buongiorno! Grazie per aver chiamato IntelliCall Assistant. 
        Il suo messaggio è stato registrato e verrà gestito al più presto.
        Un nostro operatore la ricontatterà entro 24 ore."
        """)

# Tab 3: Voicemail
with tab3:
    st.header("🎙️ Gestione Voicemail")
    
    # Lista voicemail
    voicemail_list = [
        {'id': 'VM001', 'data': '04/12 10:15', 'cliente': 'Mario Rossi', 'durata': '1:45', 'priorita': 'Urgente', 'ascoltata': False},
        {'id': 'VM002', 'data': '04/12 11:30', 'cliente': 'Luigi Bianchi', 'durata': '2:20', 'priorita': 'Alta', 'ascoltata': True},
        {'id': 'VM003', 'data': '04/12 14:45', 'cliente': 'Anna Verdi', 'durata': '0:55', 'priorita': 'Media', 'ascoltata': False},
        {'id': 'VM004', 'data': '04/12 16:20', 'cliente': 'Giulia Neri', 'durata': '3:10', 'priorita': 'Urgente', 'ascoltata': False},
    ]
    
    for vm in voicemail_list:
        priority_class = vm['priorita'].lower()
        status = "🔴" if not vm['ascoltata'] else "🟢"
        
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{vm['id']}**")
            with col2:
                st.markdown(f"**{vm['cliente']}** - {vm['data']}")
            with col3:
                st.markdown(f"⏱️ {vm['durata']}")
            with col4:
                st.markdown(f"**{status} {vm['priorita']}**")
            
            st.markdown("---")
    
    if st.button("🎧 Ascolta Tutte", use_container_width=True):
        st.success("Tutte le voicemail sono state contrassegnate come ascoltate!")

# Tab 4: Clienti
with tab4:
    st.header("👥 Gestione Clienti")
    
    # Aggiungi nuovo cliente
    with st.expander("➕ Aggiungi Nuovo Cliente"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_nome = st.text_input("Nome")
            new_cognome = st.text_input("Cognome")
            new_email = st.text_input("Email")
        
        with col2:
            new_telefono = st.text_input("Telefono")
            new_azienda = st.text_input("Azienda")
            new_tipo = st.selectbox("Tipo", ["Nuovo", "Regolare", "VIP", "Aziendale"])
        
        if st.button("Salva Cliente"):
            st.success(f"Cliente {new_nome} {new_cognome} aggiunto con successo!")
    
    # Lista clienti
    st.subheader("📋 Lista Clienti")
    clienti_data = {
        'Nome': ['Mario', 'Luigi', 'Anna', 'Giulia', 'Paolo'],
        'Cognome': ['Rossi', 'Bianchi', 'Verdi', 'Neri', 'Gialli'],
        'Telefono': ['+39 123456789', '+39 987654321', '+39 456123789', '+39 789456123', '+39 321654987'],
        'Tipo': ['VIP', 'Regolare', 'Nuovo', 'Aziendale', 'Regolare'],
        'Ultima Chiamata': ['04/12', '03/12', '02/12', '01/12', '30/11']
    }
    
    df_clienti = pd.DataFrame(clienti_data)
    st.dataframe(df_clienti, use_container_width=True)

# Tab 5: Configurazione
with tab5:
    st.header("⚙️ Configurazione Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Impostazioni Azienda")
        nome_azienda = st.text_input("Nome Azienda", "IntelliCall Solutions")
        orari_apertura = st.text_input("Orari Apertura", "Lun-Ven 9:00-18:00")
        numero_emergenza = st.text_input("Numero Emergenza", "+39 333 1234567")
    
    with col2:
        st.subheader("Impostazioni AI")
        api_key = st.text_input("OpenAI API Key", type="password")
        lingua = st.selectbox("Lingua Predefinita", ["Italiano", "Inglese", "Francese", "Tedesco", "Spagnolo"])
        analisi_automatica = st.checkbox("Analisi Automatica Sentiment", value=True)
    
    st.subheader("Notifiche")
    col_not1, col_not2 = st.columns(2)
    
    with col_not1:
        notifica_email = st.text_input("Email Notifiche", "admin@intellicall.com")
        notifica_sms = st.checkbox("Attiva notifiche SMS", value=True)
    
    with col_not2:
        notifica_whatsapp = st.checkbox("Attiva notifiche WhatsApp", value=False)
        intervallo_aggiornamento = st.select_slider(
            "Intervallo Aggiornamento",
            options=["30s", "1m", "5m", "15m", "30m"],
            value="5m"
        )
    
    if st.button("💾 Salva Configurazione", type="primary", use_container_width=True):
        st.success("Configurazione salvata con successo!")

# Sidebar
with st.sidebar:
    st.title("⚡ Controlli Rapidi")
    
    if st.button("🔄 Aggiorna Sistema", use_container_width=True):
        st.rerun()
    
    if st.button("📊 Genera Report", use_container_width=True):
        st.info("Report generato e inviato via email!")
    
    if st.button("💾 Backup Dati", use_container_width=True):
        st.success("Backup completato!")
    
    st.markdown("---")
    st.subheader("📈 Statistiche Live")
    
    st.metric("Chiamate Totali", "342", "+8.2%")
    st.metric("Voicemail", "24", "+3")
    st.metric("Clienti Attivi", "156", "+12")
    
    st.markdown("---")
    st.subheader("🔔 Notifiche Recenti")
    
    notifiche = [
        "⚠️ Chiamata urgente da Mario Rossi",
        "✅ Voicemail processata VM003",
        "📅 Appuntamento domani 10:00",
        "🔄 Sistema aggiornato v1.2.3"
    ]
    
    for notifica in notifiche:
        st.markdown(f"• {notifica}")

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f2:
    st.markdown("<p style='text-align: center; color: gray;'>🤖 IntelliCall Assistant v1.0 • © 2025 • CONDORPROF</p>", unsafe_allow_html=True)
