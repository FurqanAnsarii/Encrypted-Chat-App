import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# --- PRO AES LOGIC ---
AES_KEY = b'SixteenByteKey12' # 16 bytes for AES-128
BLOCK_SIZE = 16

def encrypt_message(plain_text):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), BLOCK_SIZE))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return f"{iv}:{ct}"

def decrypt_message(encoded_msg):
    try:
        iv_res, ct_res = encoded_msg.split(':')
        iv = base64.b64decode(iv_res)
        ct = base64.b64decode(ct_res)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), BLOCK_SIZE).decode('utf-8')
    except: return "[Decryption Error]"

# --- PROFESSIONAL INTERFACE ---
st.set_page_config(page_title="CipherShield Pro", layout="wide")
st.title("🛡️ Advanced Encrypted Communication")

# Sidebar for Recruiter's Info
st.sidebar.header("Cybersecurity Specs")
st.sidebar.code("Algorithm: AES-128\nMode: CBC\nPadding: PKCS7", language="text")
st.sidebar.info("This app demonstrates end-to-end encryption logic.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Chat Input
user_input = st.chat_input("Enter message to encrypt and send...")

if user_input:
    encrypted_data = encrypt_message(user_input)
    # Simulation: We store the encrypted data to show the recruiter how it looks
    st.session_state.messages.append({
        "role": "user", 
        "plain": user_input, 
        "cipher": encrypted_data
    })

# Displaying Messages
for msg in st.session_state.messages:
    with st.chat_message("user"):
        st.write(f"**Plaintext:** {msg['plain']}")
        st.caption(f"🛡️ **Encrypted Data (On-Wire):** {msg['cipher']}")

st.divider()
st.caption("Developed as a Cybersecurity Portfolio Project")