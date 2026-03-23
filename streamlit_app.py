import streamlit as st
from supabase import create_client, client
from dotenv import load_dotenv
import os

# 1. Initialize session state at the very top to avoid KeyErrors
if "local_pedido" not in st.session_state:
    st.session_state["local_pedido"] = ""

# ... (Font and CSS code is fine) ...

# ... (Supabase setup) ...
load_dotenv()
url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
supabase: client = create_client(url, key)

# --- Updated product_card ---
def product_card(title, price, description, img_url, producto):
    with st.container(border=True):
        st.image(img_url, use_container_width=True)
        st.subheader(title)
        st.write(description)
        st.badge(f"**Precio:** {price}€", color="green")
        if st.button("Pedir", key=title):
            # Update state
            st.session_state["local_pedido"] = producto
            # IMPORTANT: Rerun so the text_input below sees the change immediately
            st.rerun()

# --- Design ---
st.header("Imprint")
# ... (Header text) ...

col1, col2, col3 = st.columns(3)
with col1:
    product_card("Anillo Planetario", 3.99, "Engranajes de precisión.", "https://makerworld.bblmw.com/...", "https://makerworld.com/...")
# ... (Other columns) ...

st.divider()

# --- Pedir Section ---
email = st.text_input("Tu email")

# FIX 1: Use parentheses () for .get, not square brackets []
# FIX 2: We use the state as the value
pedido_input = st.text_input("URL del modelo", value=st.session_state.get("local_pedido", ""))

if st.button("Enviar Pedido Final", key="submit_order"):
    if pedido_input and email:
        supabase.table('todos').insert({
            'pedido': pedido_input,
            'email': email,
            'estado': 'pendiente'
        }).execute()
        st.success("¡Ya has pedido!")
        # Optional: Clear the selection after ordering
        st.session_state["local_pedido"] = ""
    else:
        st.error("Rellena todo")