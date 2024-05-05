## Overview of the Peer-to-Peer Chat System

The peer-to-peer chat system consists of two main components in separate Python files:
 - chatDB.py: Manages the database operations using SQLAlchemy. It handles user data (usernames and IP addresses) and messaging data (message content, sender, and recipient details).
 - p2pChat.py: Manages the application logic, including a GUI, networking for message exchange, and encryption for secure communication.
 - Reference: https://github.com/rashidkolaghassi/P2P-Chat-System
<br>

## Key Features and Enhancements

 - End-to-End Encryption: Messages are encrypted before sending and decrypted upon reception using the cryptography library, ensuring that communications remain confidential and secure.
 - Local Database Storage: Uses a local SQLite database to store user and message data, allowing for persistence and retrieval of message history.
 - Graphical User Interface (GUI): Implemented using tkinter, providing a user-friendly interface that includes a text display area, a message input field, and a send button.
 - Network Communication: Direct socket connections are used for sending and receiving messages, supporting real-time peer-to-peer communication without needing a central server.
<br>

## data sanitization and protection
 - Inside the p2pDataProjection folder.
 - ### chatDB-new.py:
    - **Encryption of Sensitive User Data:** Usernames and IP addresses are encrypted before storage to protect sensitive information.
    - **Protection Against SQL Injection:** The use of SQLAlchemy's ORM utilizes parameterized queries, ensuring user inputs are treated as data rather than executable SQL code, effectively preventing SQL injection.
 - ### p2pChat.py:
    - **Input Sanitization:** User inputs are sanitized to prevent XSS and other potential injection vulnerabilities.
    - **Encryption Handling:** Messages are encrypted before being sent and decrypted upon reception to secure communication.

## Running Process

To run the application:
 - Ensure you have Python and necessary packages (SQLAlchemy, cryptography, tkinter) installed.
 - Save the two Python files (chatDB.py and p2pChat.py) in the same directory. Run p2pChat.py to start the application.
