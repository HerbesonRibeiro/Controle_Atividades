class AuthController:
    def autenticar(self, email, senha):
        # Simulação - substitua por sua lógica real
        if email == "admin@exemplo.com" and senha == "123":
            return {"nome": "Admin", "email": email}
        raise ValueError("Login falhou!")