import random  # Para gerar um número único para a conta

# Representação básica de uma conta bancária
class Conta:
    def _init_(self, nome_titular, senha_acesso):
        self.titular = nome_titular
        self.numero_conta = random.randint(100, 999)  # Número aleatório pra identificar a conta
        self.__senha = senha_acesso
        self.__saldo_corrente = 0.0
        self.__saldo_poupanca = 0.0
        self.conta_bloqueada = False  # Começa desbloqueada, normal né?

    # Pega o saldo da conta corrente
    def consultar_saldo_corrente(self):
        return self.__saldo_corrente

    # Altera o saldo da conta corrente
    def atualizar_saldo_corrente(self, valor):
        self.__saldo_corrente += valor

    # Mostra o saldo da poupança
    def consultar_saldo_poupanca(self):
        return self.__saldo_poupanca

    # Modifica o saldo da poupança
    def atualizar_saldo_poupanca(self, valor):
        self.__saldo_poupanca += valor

    # Confere se a senha está certa antes de fazer algo importante
    def autenticar_senha(self):
        if self.conta_bloqueada:
            print("Sua conta foi bloqueada. Procure atendimento.")
            return False

        tentativas = 3
        while tentativas > 0:
            senha_informada = input("Digite sua senha (4 números): ")
            if senha_informada == self.__senha:
                return True  # Senha correta
            else:
                tentativas -= 1
                print(f"Senha incorreta. Você ainda tem {tentativas} tentativa(s).")

        # Bloqueia a conta se errar 3 vezes
        self.conta_bloqueada = True
        print("Sua conta foi bloqueada por segurança.")
        return False

    # Mostra o extrato bancário
    def exibir_extrato(self):
        if self.autenticar_senha():
            print("\n=== Resumo da Conta ===")
            print(f"Titular: {self.titular}")
            print(f"Número da Conta: {self.numero_conta}")
            print(f"Saldo Corrente: R$ {self.consultar_saldo_corrente():.2f}")
            print(f"Saldo Poupança: R$ {self.consultar_saldo_poupanca():.2f}")
            print("========================")


# Conta Corrente
class ContaCorrente(Conta):
    def realizar_saque(self, valor):
        if self.autenticar_senha():
            if self.consultar_saldo_corrente() >= valor:
                self.atualizar_saldo_corrente(-valor)
                print(f"Saque de R$ {valor:.2f} feito com sucesso.")
            else:
                print("Saldo insuficiente. Tente um valor menor.")

    def realizar_deposito(self, valor):
        if valor > 0:
            self.atualizar_saldo_corrente(valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("O valor do depósito deve ser maior que zero.")

    def transferir_para_poupanca(self, valor, conta_poupanca):
        if self.autenticar_senha():
            if self.consultar_saldo_corrente() >= valor:
                self.atualizar_saldo_corrente(-valor)
                conta_poupanca.atualizar_saldo_poupanca(valor)
                print(f"Transferência de R$ {valor:.2f} para a poupança concluída.")
            else:
                print("Saldo insuficiente para realizar a transferência.")


# Conta Poupança
class ContaPoupanca(Conta):
    def realizar_resgate(self, valor, conta_corrente):
        if self.autenticar_senha():
            if self.consultar_saldo_poupanca() >= valor:
                self.atualizar_saldo_poupanca(-valor)
                conta_corrente.atualizar_saldo_corrente(valor)
                print(f"Resgate de R$ {valor:.2f} da poupança realizado.")
            else:
                print("Saldo insuficiente na poupança.")


# Controle principal do sistema
def principal():
    print("Bem-vindo ao Sistema do Banco!")

    nome_titular = input("Informe seu nome completo: ")
    while True:
        senha_acesso = input("Crie uma senha (4 dígitos): ")
        if senha_acesso.isdigit() and len(senha_acesso) == 4:
            break
        print("A senha deve conter exatamente 4 números.")

    conta_corrente = ContaCorrente(nome_titular, senha_acesso)
    conta_poupanca = ContaPoupanca(nome_titular, senha_acesso)

    print(f"\nConta criada com sucesso! Número: {conta_corrente.numero_conta}")

    while True:
        try:
            deposito_inicial = float(input("Depósito inicial (mínimo R$ 10,00): "))
            if deposito_inicial >= 10:
                conta_corrente.realizar_deposito(deposito_inicial)
                break
            else:
                print("O valor mínimo para depósito é R$ 10,00.")
        except ValueError:
            print("Por favor, informe um valor numérico válido.")

    while True:
        if conta_corrente.conta_bloqueada or conta_poupanca.conta_bloqueada:
            print("Operações encerradas devido ao bloqueio da conta.")
            break

        print("\n=== Menu de Operações ===")
        print("1. Saque")
        print("2. Depósito")
        print("3. Transferir para poupança")
        print("4. Resgatar da poupança")
        print("5. Consultar extrato")
        print("6. Encerrar")
        print("=========================")

        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 1:
                valor = float(input("Informe o valor do saque: "))
                conta_corrente.realizar_saque(valor)
            elif opcao == 2:
                valor = float(input("Informe o valor do depósito: "))
                conta_corrente.realizar_deposito(valor)
            elif opcao == 3:
                valor = float(input("Quanto deseja transferir para a poupança? "))
                conta_corrente.transferir_para_poupanca(valor, conta_poupanca)
            elif opcao == 4:
                valor = float(input("Quanto deseja resgatar da poupança? "))
                conta_poupanca.realizar_resgate(valor, conta_corrente)
            elif opcao == 5:
                conta_corrente.exibir_extrato()
            elif opcao == 6:
                print("Obrigado por usar nosso sistema. Até breve!")
                break
            else:
                print("Opção inválida. Escolha novamente.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")

# Executa o programa
if _name_ == "_main_":
    principal()