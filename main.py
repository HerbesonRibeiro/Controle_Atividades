import tkinter as tk
from screens.login_view import LoginView

def main():
    try:
        root = tk.Tk()
        root.geometry("400x300")
        LoginView(root) # Só irá funcionar se a classe LoginView existir
        root.mainloop()
    except Exception as e:
        print(f'Erro crítico: {e}')

if __name__ == "__main__":
    main()