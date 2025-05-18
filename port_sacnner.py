import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

def threaded_scan():
    target_ip = entry.get()
    if not target_ip:
        messagebox.showwarning("Input Error", "Please enter an IP address or hostname.")
        return

    try:
        resolved_ip = socket.gethostbyname(target_ip)
    except socket.gaierror:
        messagebox.showerror("Invalid Input", "Unable to resolve IP/hostname.")
        return

    result_area.delete(1.0, tk.END)
    result_area.insert(tk.END, f"Scanning {resolved_ip} (Ports 20 to 1024)...\n\n")

    open_ports = []
    for port in range(20, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.3)
        result = sock.connect_ex((resolved_ip, port))
        if result == 0:
            result_area.insert(tk.END, f"Port {port} is OPEN\n")
            open_ports.append(port)
        sock.close()

    if not open_ports:
        result_area.insert(tk.END, "\nNo open ports found.")
    else:
        result_area.insert(tk.END, f"\nOpen ports: {open_ports}")

def scan_ports():
    thread = threading.Thread(target=threaded_scan)
    thread.start()

# GUI
window = tk.Tk()
window.title("Basic Port Scanner")
window.geometry("400x400")
window.configure(bg="#E6E6FA")  

label = tk.Label(window, text="Enter IP / Domain:", bg="#E6E6FA", fg="#a6acff", font=("Times New Roman", 12))
label.pack(pady=10)

entry = tk.Entry(window, width=30, font=("Times New Roman", 11))
entry.pack(pady=5)

button = tk.Button(window, text="Scan Ports", command=scan_ports, bg="#E6E6FA", fg="#a6acff", font=("Times New Roman", 10))
button.pack(pady=10)

result_area = scrolledtext.ScrolledText(window, width=45, height=15, font=("Times New Roman", 10))
result_area.pack(pady=10)

window.mainloop()
