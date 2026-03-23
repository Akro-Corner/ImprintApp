import streamlit as st
from supabase import create_client, client
from dotenv import load_dotenv
import os

font_url = "https://fonts.googleapis.com/css2?family=Sora:wght@400;700&display=swap"
font_name = "Sora"

st.markdown(
    f"""
    <style>
    @import url('{font_url}');

    /* This targets EVERY element in the app */
    html, body, [class*="st-"], .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, span {{
        font-family: '{font_name}', sans-serif !important;
    }}
    
    /* Specifically targeting the sidebar if it's still being stubborn */
    [data-testid="stSidebar"] {{
        font-family: '{font_name}', sans-serif !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Usar Secrets si está en Streamlit Cloud, sino .env en local
url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

load_dotenv()

supabase: client = create_client(url, key)

def add_todo(pedido):
    supabase.table('todos').insert({'pedido': pedido}).execute()

#--------------------------------------------- Diseño

st.header("Imprint")
st.badge("Envíos 24-48h", color="green")
st.write("Imprint es la mejor manera de obtener modelos 3D en tus\nmanos ya que tardamos menos de **24-48 horas** en entregarlo.\nTambién disponemos de\n**muchos colores como: azul, verde, beige, marrón, blanco y negro.**\n\n ¡Disfrutad! 😀")

st.divider()

def product_card(title, price, description, img_url):
    with st.container(border=True):
        st.image(img_url, use_container_width=True)
        st.subheader(title)
        st.write(description)
        st.badge(f"**Price:** ${price}", color="green")
        if st.button("Add to Cart", key=title):
            st.success(f"Added {title}!")

col1, col2, col3 = st.columns(3)

with col1:
    product_card("Classic Watch", 120, "This is a simple description of a product\nwhich has still not been created, but still is going to be\nvery cool!", "https://via.placeholder.com/300")
with col2:
    product_card("Wireless Buds", 80, "This is a simple description of a product\nwhich has still not been created, but still is going to be\nvery cool!", "https://via.placeholder.com/300")
with col3:
    product_card("Leather Bag", 250, "This is a simple description of a product\nwhich has still not been created, but still is going to be\nvery cool!","https://via.placeholder.com/300")

st.divider()
#--------------------------------------------- Pedir

email = st.text_input("Tu email")
pedido = st.text_input("URL del modelo")

if st.button("Pedir"):
    if pedido and email:
        supabase.table('todos').insert({
            'pedido': pedido,
            'email': email,
            'estado': 'pendiente'
        }).execute()
        st.success("¡Ya has pedido!")
    else:
        st.error("Rellena todo")