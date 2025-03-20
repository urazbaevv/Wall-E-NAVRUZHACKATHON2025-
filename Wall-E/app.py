import streamlit as st
import folium
import requests
from streamlit_folium import folium_static
import base64

# **Streamlit sahifasi**
st.set_page_config(page_title="WALL-E APP", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        margin-top: 0px;  /* 🔥 Butun sahifani 50px pastga suradi */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def add_bg_from_local(image_file):
    """Local rasmni background sifatida qo‘shish."""
    with open(image_file, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()

    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        width: 100vw;
        height: 200vh;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ✅ Background qo‘shish
add_bg_from_local("background.png")

# 📌 Streamlit UI

# **API dan konteynerlar ro‘yxatini olish**
API_URL = "http://127.0.0.1:8000/api/containers/"  # Backend API manzili

def get_containers():
    try:
        response = requests.get(API_URL)
        return response.json()
    except:
        return []

st.markdown("<h1 style='font-size: 70px;color: white;text-align: center;'>♻️ Waste Containers Monitoring</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color: white;text-align: center;'>This application automatically sends a notification when containers are full.</h1>", unsafe_allow_html=True)

# **Konteynerlar ma’lumotlarini olish**
containers = get_containers()

# **Xarita yaratish**
map_center = [41.2995, 69.2401]  # Toshkent koordinatalari
m = folium.Map(location=map_center, zoom_start=8,)

# **Har bir konteynerni xaritada ko‘rsatish**
for container in containers:
    color = "green" if container["weight"] < container["max_weight"] else "red"
    folium.Marker(
        [container["lat"], container["lon"]],
        popup=f"{container['name']} ({container['weight']} kg / {container['max_weight']} kg)",
        icon=folium.Icon(color=color),
    ).add_to(m)

# **Xaritani Streamlit orqali ko‘rsatish**
folium_static(m)

# **Statistika**
total_containers = len(containers)
full_containers = sum(1 for c in containers if c["weight"] >= c["max_weight"])

st.markdown("<h1 style='font-size:50px;color: white'>📊 Statistics</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='font-size:25px;'>Total containers: <b>{total_containers}</b></h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style='font-size:25px;'>Full containers: <b>{full_containers}</b></h3>", unsafe_allow_html=True)
# **Ogohlantirish**
if full_containers > 0:
    st.error("🚨 Some containers are full! They need to be emptied immediately.")
else:
    st.success("✅ All containers are in normal condition.")


