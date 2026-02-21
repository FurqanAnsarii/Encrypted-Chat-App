import streamlit as st
import socket
import threading
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# --- AES Configuration ---
# Use a 16-byte key (128-bit AES)
AES_KEY = b'SixteenByteKey12' 
BLOCK_SIZE = 16

def encrypt_data(data):
    """Encrypts raw bytes using AES CBC mode."""
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, BLOCK_SIZE))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return f"{iv}:{ct}"

def decrypt_data(encoded_str):
    """Decrypts the iv:ciphertext string back to raw bytes."""
    try:
        iv_res, ct_res = encoded_str.split(':')
        iv = base64.b64decode(iv_res)
        ct = base64.b64decode(ct_res)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), BLOCK_SIZE)
    except Exception:
        return None

# --- UI Configuration ---
st.set_page_config(page_title="CipherShield Pro", layout="wide")
st.title("🛡️ SecureShield: Encrypted Communication Suite")

# Sidebar for Network Traffic Monitoring
st.sidebar.header("🔐 Encrypted Traffic Monitor")
if 'traffic_logs' not in st.session_state:
    st.session_state.traffic_logs = []

# --- Socket Management ---
if 'socket' not in st.session_state:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 8585))
        st.session_state.socket = s
        
        def receive_handler(sock):
            while True:
                try:
                    raw_data = sock.recv(1048576).decode() # Increased buffer for files
                    if raw_data:
                        decrypted_payload = decrypt_data(raw_data)
                        if decrypted_payload:
                            # Check if it's a file or text
                            msg_str = decrypted_payload.decode('utf-8', errors='ignore')
                            st.session_state.messages.append({"role": "Assistant", "content": msg_str})
                            st.session_state.traffic_logs.append(f"INCOMING: {raw_data[:50]}...")
                            st.rerun()
                except: break
        
        threading.Thread(target=receive_handler, args=(s,), daemon=True).start()
    except:
        st.error("Connection Failed: Ensure server.py is running on port 8585.")

# --- Chat & File Interface ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Layout: 2 Columns
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Message Board")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type a secure message...")
    if user_input:
        encrypted_payload = encrypt_data(user_input.encode())
        st.session_state.socket.send(encrypted_payload.encode())
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.traffic_logs.append(f"OUTGOING TEXT: {encrypted_payload[:60]}...")
        st.rerun()

with col2:
    st.subheader("Secure File Transfer")
    uploaded_file = st.file_uploader("Choose file to encrypt & send", type=['txt', 'png', 'jpg', 'pdf'])
    if uploaded_file is not None:
        if st.button("Encrypt & Send File"):
            file_bytes = uploaded_file.read()
            file_name = f"FILE_SEND: {uploaded_file.name}"
            # Encrypt file content
            encrypted_file = encrypt_data(file_bytes)
            # Sending header + encrypted content
            st.session_state.socket.send(encrypted_file.encode())
            st.success(f"File '{uploaded_file.name}' encrypted and sent!")
            st.session_state.traffic_logs.append(f"OUTGOING FILE: {encrypted_file[:60]}...")

# Render Traffic Logs in Sidebar
for log in reversed(st.session_state.traffic_logs):
    st.sidebar.code(log, language="bash")