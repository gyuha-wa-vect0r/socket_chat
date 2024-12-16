# TCP Chat Programs: From Single to Multi-Client Solutions

This project encompasses the implementation of two progressive TCP chat systems:

1. **Task 1**: A basic 1:1 TCP chat program that establishes a reliable connection between a client and a server for text message exchange.
2. **Task 2**: An advanced multi-client chat system that supports simultaneous connections, real-time message broadcasting, user commands, and AI-powered search functionality.

Each program demonstrates the evolution of functionality, scalability, and user interactivity while maintaining robust TCP communication principles.

---
---

# Task 1: 1:1 TCP Chat Program

## Overview
Task 1 involves implementing a 1:1 chat program between a client and server using Python socket programming. The project focuses on understanding the fundamental operation of the TCP protocol and addressing various scenarios (e.g., disconnection, data loss) that can occur during data transmission. It is designed and implemented to ensure a stable communication environment with a console-based user interface for exchanging text data between the client and server.

---

## Key Features
- **1:1 TCP Connection**: Establishes a reliable and stable connection using the TCP protocol's 3-way handshake process.
- **Text Message Transmission**: Real-time exchange of text messages between the client and server.
- **Exception Handling**: Handles situations like disconnections or data transmission failures to maintain system stability.
- **Connection Termination Handling**: Safely releases socket resources when the client or server disconnects.

---

## Development Environment
- **Language**: Python 3.9.20
- **Operating System**: Ubuntu 24.04 on Windows 11 WSL2
- **Network Configuration**: Localhost (127.0.0.1)
- **Libraries Used**: Python standard library `socket`
- **Port**: 5001

---

## Program Structure

### Server (`server_task1.py`)
1. **TCP Socket Creation**:
   - Creates a socket using IPv4 (`AF_INET`) and TCP protocol (`SOCK_STREAM`).
   - Ensures reliable data transmission using the TCP protocol.
2. **Binding to IP and Port**:
   - Binds the socket to the `127.0.0.1` IP and port `5001`.
   - Waits for client connection requests.
3. **Accepting Client Connections**:
   - Accepts connection requests and returns a client socket and address.
   - Logs the connected client's information on the server side.
4. **Message Transmission**:
   - Displays messages received from the client and sends responses based on server user input.
   - Terminates the connection if empty data is received.
5. **Connection Termination Handling**:
   - Releases resources when the client disconnects and closes the server socket.

### Client (`client_task1.py`)
1. **TCP Socket Creation**:
   - Creates a socket using IPv4 (`AF_INET`) and TCP protocol (`SOCK_STREAM`).
2. **Connecting to the Server**:
   - Sends a connection request to the server at IP `127.0.0.1` and port `5001`.
   - Displays a success message upon successful connection.
3. **Message Transmission**:
   - Sends user-input messages to the server.
   - Displays messages received from the server in real-time.
4. **Connection Termination Handling**:
   - Releases socket resources and displays a termination message upon disconnecting.

---

## Test Results
1. **Successful Connection**:
   - The client successfully connects to the server and establishes communication.
   - The server accepts the connection request and logs the client's address information.
2. **Data Transmission**:
   - Text messages transmitted between the client and server are consistent, with no data loss or distortion.
   - Successfully tested under various scenarios with proper message delivery.
3. **Graceful Termination**:
   - The client or server disconnects safely, closing the corresponding socket and terminating the program.
   - Robust exception handling ensures system stability during unexpected disconnections.

---
---

# Task 2: Multi-Client Chat Program

## Overview
Task 2 is an extended version of Task 1, designed to implement a chat program that operates in a multi-client environment. It uses multithreading to allow multiple clients to connect and exchange messages simultaneously. The program supports various user commands and integrates OpenAI API for generative AI-based search functionality. These enhancements make the original TCP communication program more practical and scalable.

---

## Key Features
- **Multi-Client Support**: Enables simultaneous connections of multiple clients using multithreading.
- **Text Message Broadcasting**: Delivers messages from one client to all other connected clients.
- **OpenAI API Search Functionality**: Provides responses powered by OpenAI GPT-4 using the `/search` command.
- **User Commands**:
  - `/help`: Displays a list of available commands.
  - `/users`: Shows a list of currently connected clients.
  - `/nick`: Allows clients to change their nickname.
  - `/exit`: Disconnects from the server.
- **Message Timestamp and Nickname Display**: Records the time of message transmission and displays the sender's nickname.
- **Exception Handling and Stability**: Handles unexpected disconnections and API call failures gracefully.

---

## Development Environment
- **Language**: Python 3.9.20
- **Operating System**: Ubuntu 24.04 on Windows 11 WSL2
- **Network Configuration**: Localhost (127.0.0.1)
- **Libraries Used**:
  - Python standard libraries: `socket`, `threading`, `datetime`
  - OpenAI API library: `openai`
- **Port**: 5002

---

## Program Structure

### Server (`server_task2.py`)
1. **TCP Socket Creation**:
   - Creates a socket using IPv4 (`AF_INET`) and TCP (`SOCK_STREAM`).
2. **Binding to IP and Port**:
   - Binds the socket to IP `127.0.0.1` and port `5002`.
   - Configured to handle up to 5 simultaneous client connection requests.
3. **Accepting Client Connections**:
   - Accepts connection requests, returning a client socket and address.
   - Broadcasts a message to notify all clients of new connections.
4. **Handling Clients with Multithreading**:
   - Manages each client connection independently using separate threads.
5. **Message Broadcasting**:
   - Relays messages received from one client to all other clients.
   - Formats messages to include the sender's nickname and timestamp.
6. **Command Handling**:
   - `/search`: Calls OpenAI GPT-4 API and broadcasts the result.
   - `/users`: Sends a list of currently connected clients to the requesting client.
   - `/nick`: Processes nickname change requests.
   - `/exit`: Handles client disconnections.
   - `/help`: Provides a list of available commands.
7. **Connection Termination Handling**:
   - Notifies all clients when a client disconnects and releases resources.

### Client (`client_task2.py`)
1. **TCP Socket Creation**:
   - Creates a socket using IPv4 (`AF_INET`) and TCP (`SOCK_STREAM`).
2. **Connecting to the Server**:
   - Sends a connection request to server IP `127.0.0.1` and port `5002`.
   - Prompts the user to set a nickname upon successful connection.
3. **Message Transmission and Reception**:
   - Sends user-input messages to the server.
   - Displays messages received from the server asynchronously.
4. **Command Handling**:
   - `/search`: Requests AI-based search using OpenAI API.
   - `/users`: Requests a list of connected clients.
   - `/nick`: Changes the user's nickname.
   - `/exit`: Disconnects from the server.
5. **Connection Termination Handling**:
   - Safely releases client socket resources and displays a termination message upon disconnecting.

---

## Test Results
1. **Successful Multi-Client Connections**:
   - Multiple clients connect to the server simultaneously and exchange messages.
   - Each client's nickname is correctly set and managed by the server.
2. **Message Broadcasting**:
   - Messages sent by one client are delivered to all other clients in real time.
   - Timestamps and nicknames are displayed accurately.
3. **Command Functionality**:
   - The `/search` command successfully calls OpenAI GPT-4 API and broadcasts the result.
   - Commands like `/users`, `/nick`, and `/help` work as expected.
4. **Stable Connection Termination**:
   - Clients disconnect using the `/exit` command, and resources are safely released.
   - The server and other clients are notified of disconnections.
   - The system remains stable even during abnormal disconnections.
