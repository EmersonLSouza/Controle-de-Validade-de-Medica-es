from datetime import datetime, timedelta

class ControleMedicamentos:
    def __init__(self):
        self.estoque = []

    def adicionar_medicamento(self, nome, lote, fabricacao_str, validade_str, quantidade):
        """
        Adiciona um medicamento ao estoque.
        Datas no formato 'YYYY-MM-DD' (Ano-Mês-Dia).
        """
        try:
            # Converte as strings para objetos de data do Python
            fabricacao = datetime.strptime(fabricacao_str, '%Y-%m-%d').date()
            validade = datetime.strptime(validade_str, '%Y-%m-%d').date()
            
            # Trava de segurança lógica
            if fabricacao >= validade:
                print(f"❌ Erro no cadastro de '{nome}': A data de fabricação ({fabricacao_str}) não pode ser igual ou posterior à validade ({validade_str}).")
                return

            medicamento = {
                'nome': nome,
                'lote': lote,
                'fabricacao': fabricacao,
                'validade': validade,
                'quantidade': quantidade
            }
            self.estoque.append(medicamento)
            print(f"✅ Adicionado: {nome} (Lote: {lote}) | Fab: {fabricacao_str} | Val: {validade_str}")
            
        except ValueError:
            print("❌ Erro: Formato de data inválido. Use AAAA-MM-DD.")

    def listar_vencidos(self):
        hoje = datetime.now().date()
        return [med for med in self.estoque if med['validade'] < hoje]

    def listar_vencimento_proximo(self, dias_alerta=90):
        hoje = datetime.now().date()
        data_limite = hoje + timedelta(days=dias_alerta)
        return [med for med in self.estoque if hoje <= med['validade'] <= data_limite]

# ==========================================
# Testando o código na prática
# ==========================================
if __name__ == "__main__":
    sistema = ControleMedicamentos()
    print("--- REGISTRANDO MEDICAMENTOS ---")
    
    # Ordem: Nome, Lote, Fabricação, Validade, Quantidade
    sistema.adicionar_medicamento("Paracetamol 500mg", "L-101", "2025-10-15", "2027-10-15", 50)
    sistema.adicionar_medicamento("Amoxicilina", "L-202", "2024-06-10", "2026-06-10", 20) 
    sistema.adicionar_medicamento("Ibuprofeno", "L-303", "2023-12-01", "2025-12-01", 15) 
    
    # Testando a trava de segurança (Erro intencional: fabricação depois da validade)
    sistema.adicionar_medicamento("Dipirona", "L-404", "2026-01-01", "2024-01-01", 10)
    
    print("\n--- RELATÓRIO DE VALIDADES ---")
    
    # 1. Checar Vencidos
    vencidos = sistema.listar_vencidos()
    if vencidos:
        print("\n🚨 MEDICAMENTOS VENCIDOS:")
        for med in vencidos:
            print(f" - {med['nome']} (Lote {med['lote']}) | Fab: {med['fabricacao']} | Venceu: {med['validade']}")

    # 2. Checar Vencimentos Próximos
    proximos = sistema.listar_vencimento_proximo(dias_alerta=90)
    if proximos:
        print("\n⚠️ VENCENDO NOS PRÓXIMOS 30 DIAS:")
        for med in proximos:
             print(f" - {med['nome']} (Lote {med['lote']}) | Fab: {med['fabricacao']} | Vence: {med['validade']}")