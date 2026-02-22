🔐 Encrypted Chat Application (AES + TCP)

A secure client-server chat application that encrypts all messages using AES symmetric encryption before transmission over TCP sockets.
The project demonstrates practical cryptography implementation, secure communication design, and multi-client concurrency handling.

🚀 Features

AES symmetric encryption for all messages

Secure IV generation per message

TCP socket-based client/server architecture

Multi-client support using threading

Pre-shared key handling

Encrypted message transmission (no plaintext exposure)

Message logging support

🛠️ Tech Stack

Language: Python

Networking: TCP Sockets

Encryption: AES (CBC mode recommended)

Library: PyCryptodome

Concurrency: Threading

🏗️ Architecture Overview

The server listens for incoming TCP connections.

Multiple clients connect concurrently.

Each outgoing message is:

Encrypted using AES

Assigned a securely generated IV

The server decrypts incoming messages.

Messages are broadcast to other connected clients.

Logs are stored for session tracking.

🔐 Security Implementation

AES symmetric encryption

Secure random IV generation per message

No plaintext communication

Pre-shared key authentication model

Basic protection against replay through unique IV usage

Note: This implementation is designed for educational and demonstration purposes.

▶️ How to Run
1️⃣ Clone the Repository
git clone https://github.com/yourusername/encrypted-chat-app.git
cd encrypted-chat-app
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Start the Server
python server.py
4️⃣ Start the Client (Multiple Terminals)
python client.py
🌐 Live Demo
https://encrypted-chat-app-6zaryrbdcceng8yuwqvdne.streamlit.app/
