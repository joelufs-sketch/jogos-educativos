import random
import time
import os
from colorama import Fore, Back, Style, init

# Inicializar colorama
init(autoreset=True)

class FolcloreMath:
    def __init__(self):
        self.pontuacao = 0
        self.nivel = 1
        self.questoes_respondidas = 0
        self.acertos = 0
        self.erros = 0
        self.combo = 0
        self.max_combo = 0
        
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self):
        """Exibe o cabeçalho do jogo"""
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'🎪 FOLCLORE MATH - Matemática e Tradição Popular 🎪'.center(60)}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}\n")
    
    def exibir_status(self):
        """Exibe status do jogador"""
        status = f"""
{Fore.YELLOW}╔════════════════════════════════════════════════════════╗
║ {Fore.CYAN}Pontuação: {self.pontuacao:5d} {Fore.YELLOW}│{Fore.CYAN} Nível: {self.nivel:<2d} {Fore.YELLOW}│{Fore.CYAN} Combo: {self.combo:3d}🔥 {Fore.YELLOW}║
║ {Fore.GREEN}Acertos: {self.acertos:<3d} {Fore.YELLOW}│{Fore.RED} Erros: {self.erros:<3d} {Fore.YELLOW}│{Fore.MAGENTA} Taxa: {self._calcular_taxa():.0f}% {Fore.YELLOW}║
╚════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(status)
    
    def _calcular_taxa(self):
        """Calcula taxa de acerto"""
        if self.questoes_respondidas == 0:
            return 0
        return (self.acertos / self.questoes_respondidas) * 100
    
    def exibir_menu_inicial(self):
        """Menu inicial do jogo"""
        self.limpar_tela()
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{'╔' + '═'*58 + '╗'.center(60)}{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}{'║ BEM-VINDO AO FOLCLORE MATH! '.center(60)}{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}{'║ Teste seus conhecimentos sobre Matemática e Folclore! '.center(60)}{Style.RESET_ALL}")
        print(f"{Back.MAGENTA}{Fore.WHITE}{'╚' + '═'*58 + '╝'.center(60)}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Escolha uma opção:\n")
        print(f"{Fore.YELLOW}[1] {Fore.WHITE}GEOMETRIA - Brinquedos e Brincadeiras")
        print(f"{Fore.YELLOW}[2] {Fore.WHITE}PROBABILIDADE - Jogos Populares")
        print(f"{Fore.YELLOW}[3] {Fore.WHITE}PROPORÇÕES - Receitas Tradicionais")
        print(f"{Fore.YELLOW}[4] {Fore.WHITE}🎯 DESAFIO TOTAL - Todas as Categorias!")
        print(f"{Fore.YELLOW}[5] {Fore.WHITE}📊 Ver Recordes")
        print(f"{Fore.YELLOW}[0] {Fore.WHITE}Sair\n")
        
        return input(f"{Fore.CYAN}Sua escolha: {Style.RESET_ALL}")
    
    def questoes_geometria(self):
        """Questões sobre geometria em brinquedos populares"""
        questoes = [
            {
                "pergunta": f"{Fore.YELLOW}🎡 Uma pipa em forma de losango tem diagonais de 60cm e 40cm.\nQual é a área da pipa?",
                "opcoes": ["1200 cm²", "2400 cm²", "1800 cm²", "900 cm²"],
                "resposta": 0,
                "explicacao": f"{Fore.CYAN}Área do losango = (D × d) / 2 = (60 × 40) / 2 = 1200 cm²",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎡 Um pião tem formato de cone com altura 8cm e raio 3cm.\nQual é o volume aproximado? (use π ≈ 3)",
                "opcoes": ["72 cm³", "24 cm³", "36 cm³", "48 cm³"],
                "resposta": 2,
                "explicacao": f"{Fore.CYAN}V = (1/3) × π × r² × h = (1/3) × 3 × 9 × 8 = 72 cm³",
                "pontos": 15
            },
            {
                "pergunta": f"{Fore.YELLOW}🎡 Uma amarelinha tem 10 quadrados de 30cm × 30cm cada.\nQual é o perímetro de um quadrado?",
                "opcoes": ["60 cm", "120 cm", "90 cm", "900 cm"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Perímetro = 4 × lado = 4 × 30 = 120 cm",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎡 Se desenharmos uma pipa quadrada com lado 50cm,\nqual será sua área?",
                "opcoes": ["2500 cm²", "2000 cm²", "1500 cm²", "3000 cm²"],
                "resposta": 0,
                "explicacao": f"{Fore.CYAN}Área do quadrado = lado² = 50² = 2500 cm²",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎡 Um pião completa 3 rotações por segundo.\nQuantas rotações faz em 5 segundos?",
                "opcoes": ["8 rotações", "15 rotações", "12 rotações", "20 rotações"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}3 rotações/seg × 5 seg = 15 rotações",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎡 A amarelinha tem 2 casas duplas e 8 simples.\nQual a proporção de casas simples?",
                "opcoes": ["1/5", "4/5", "2/5", "3/5"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}8 casas simples em 10 casas totais = 8/10 = 4/5",
                "pontos": 15
            }
        ]
        return questoes
    
    def questoes_probabilidade(self):
        """Questões sobre probabilidade em jogos"""
        questoes = [
            {
                "pergunta": f"{Fore.YELLOW}🎲 Ao lançar uma moeda, qual a probabilidade de sair cara?",
                "opcoes": ["1/4", "1/2", "1/3", "1/5"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Uma moeda tem 2 lados: 1 cara em 2 possibilidades = 1/2",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎲 Em um dado comum, qual a chance de sair número par?",
                "opcoes": ["1/6", "1/3", "1/2", "2/3"],
                "resposta": 2,
                "explicacao": f"{Fore.CYAN}Números pares no dado: 2, 4, 6 → 3 em 6 = 1/2",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎲 Se lançarmos 2 dados, qual a chance de sair dois 6?",
                "opcoes": ["1/36", "1/12", "1/6", "1/18"],
                "resposta": 0,
                "explicacao": f"{Fore.CYAN}(1/6) × (1/6) = 1/36",
                "pontos": 20
            },
            {
                "pergunta": f"{Fore.YELLOW}🎲 No jogo de Pedra, Papel, Tesoura, qual a probabilidade\nde ganhar na primeira rodada?",
                "opcoes": ["1/2", "1/3", "1/4", "0"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Você tem 1 opção vencedora em 3 possíveis = 1/3",
                "pontos": 15
            },
            {
                "pergunta": f"{Fore.YELLOW}🎲 Se um jogo foi jogado 100 vezes e você ganhou 40 vezes,\nqual sua frequência relativa de vitória?",
                "opcoes": ["0.3", "0.4", "0.5", "0.6"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Frequência relativa = 40/100 = 0.4",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🎲 Qual a probabilidade de NÃO sair 6 em um dado?",
                "opcoes": ["1/6", "5/6", "1/2", "2/3"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Números que não são 6: 1,2,3,4,5 → 5 em 6 = 5/6",
                "pontos": 10
            }
        ]
        return questoes
    
    def questoes_proporcoes(self):
        """Questões sobre proporções em receitas"""
        questoes = [
            {
                "pergunta": f"{Fore.YELLOW}🍰 Uma receita de bolo usa 2 xícaras de leite e 1 de fubá.\nSe duplicarmos a receita, quantas xícaras de leite usaremos?",
                "opcoes": ["2 xícaras", "3 xícaras", "4 xícaras", "5 xícaras"],
                "resposta": 2,
                "explicacao": f"{Fore.CYAN}2 xícaras × 2 = 4 xícaras",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🍰 Uma receita para 8 pessoas usa 2 ovos.\nPara 4 pessoas, quantos ovos usaremos?",
                "opcoes": ["1 ovo", "2 ovos", "3 ovos", "4 ovos"],
                "resposta": 0,
                "explicacao": f"{Fore.CYAN}Reduzindo pela metade: 2 ÷ 2 = 1 ovo",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🍰 Se 1 xícara = 240 ml, quanto é 1/2 xícara em ml?",
                "opcoes": ["480 ml", "240 ml", "120 ml", "60 ml"],
                "resposta": 2,
                "explicacao": f"{Fore.CYAN}240 ÷ 2 = 120 ml",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🍰 Uma receita usa 3 xícaras de leite para 1 de açúcar.\nQual a proporção leite:açúcar?",
                "opcoes": ["1:3", "3:1", "2:1", "1:2"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Proporção = 3 partes de leite : 1 parte de açúcar = 3:1",
                "pontos": 15
            },
            {
                "pergunta": f"{Fore.YELLOW}🍰 Se a receita original custa R$ 8,00 para 4 pessoas,\nquanto custará para 8 pessoas?",
                "opcoes": ["R$ 8,00", "R$ 16,00", "R$ 4,00", "R$ 32,00"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}Dobrando o tamanho: R$ 8,00 × 2 = R$ 16,00",
                "pontos": 10
            },
            {
                "pergunta": f"{Fore.YELLOW}🍰 Uma receita triplicada usa 9 ovos.\nQuantos ovos a receita original usava?",
                "opcoes": ["2 ovos", "3 ovos", "4 ovos", "6 ovos"],
                "resposta": 1,
                "explicacao": f"{Fore.CYAN}9 ÷ 3 = 3 ovos na receita original",
                "pontos": 15
            }
        ]
        return questoes
    
    def fazer_pergunta(self, questao_dict, numero):
        """Faz uma pergunta ao jogador"""
        self.exibir_cabecalho()
        self.exibir_status()
        
        print(f"{Fore.LIGHTBLUE_EX}{'─'*60}")
        print(f"{Fore.LIGHTBLUE_EX}Questão {numero}:")
        print(f"{Fore.LIGHTBLUE_EX}{'─'*60}\n")
        
        print(questao_dict["pergunta"])
        print()
        
        for i, opcao in enumerate(questao_dict["opcoes"]):
            print(f"{Fore.LIGHTGREEN_EX}[{i}] {opcao}")
        
        print()
        
        while True:
            try:
                resposta = int(input(f"{Fore.CYAN}Sua resposta (0-3): {Style.RESET_ALL}"))
                if 0 <= resposta <= 3:
                    return resposta
                else:
                    print(f"{Fore.RED}⚠️  Digite um número entre 0 e 3!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}⚠️  Digite um número válido!{Style.RESET_ALL}")
    
    def verificar_resposta(self, resposta, questao_dict):
        """Verifica se a resposta está correta"""
        if resposta == questao_dict["resposta"]:
            self.acertos += 1
            self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            
            pontos = questao_dict["pontos"]
            # Bonus por combo
            bonus = (self.combo - 1) * 5
            total = pontos + bonus
            
            self.pontuacao += total
            
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print(f"{Back.GREEN}{Fore.BLACK}{'✓ ACERTOU!'.center(60)}{Style.RESET_ALL}\n")
            print(f"{Fore.LIGHTGREEN_EX}{questao_dict['explicacao']}\n")
            print(f"{Fore.YELLOW}Pontos: {pontos} + Bonus Combo: {bonus} = {Fore.LIGHTGREEN_EX}{total} pts{Fore.RESET}")
            
            if self.combo > 1:
                print(f"{Fore.LIGHTMAGENTA_EX}🔥 Combo x{self.combo}! Mantenha!{Style.RESET_ALL}")
            
            return True
        else:
            self.erros += 1
            self.combo = 0
            
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print(f"{Back.RED}{Fore.WHITE}{'✗ ERROU!'.center(60)}{Style.RESET_ALL}\n")
            print(f"{Fore.LIGHTGREEN_EX}{questao_dict['explicacao']}\n")
            print(f"{Fore.LIGHTRED_EX}A resposta correta era: {questao_dict['opcoes'][questao_dict['resposta']]}{Style.RESET_ALL}\n")
            
            return False
        
        self.questoes_respondidas += 1
        input(f"{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def exibir_resultado_rodada(self, questoes_totais):
        """Exibe resultado final da rodada"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"{Back.LIGHTYELLOW_EX}{Fore.BLACK}{'RESULTADO FINAL'.center(60)}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Estatísticas da Rodada:")
        print(f"{Fore.YELLOW}{'─'*60}")
        print(f"{Fore.LIGHTGREEN_EX}✓ Acertos: {self.acertos}//{questoes_totais}")
        print(f"{Fore.LIGHTRED_EX}✗ Erros: {self.erros}//{questoes_totais}")
        print(f"{Fore.LIGHTMAGENTA_EX}🔥 Maior Combo: x{self.max_combo}")
        print(f"{Fore.LIGHTYELLOW_EX}⭐ Pontuação Total: {self.pontuacao} pts")
        print(f"{Fore.LIGHTCYAN_EX}📊 Taxa de Acerto: {self._calcular_taxa():.1f}%")
        print(f"{Fore.YELLOW}{'─'*60}\n")
        
        # Feedback baseado na performance
        taxa = self._calcular_taxa()
        if taxa == 100:
            print(f"{Fore.LIGHTGREEN_EX}🏆 PERFEIÇÃO! Você é um mestre do Folclore Math!{Style.RESET_ALL}\n")
        elif taxa >= 80:
            print(f"{Fore.LIGHTGREEN_EX}🌟 Excelente! Parabéns!{Style.RESET_ALL}\n")
        elif taxa >= 60:
            print(f"{Fore.LIGHTYELLOW_EX}👍 Bom! Você está no caminho certo!{Style.RESET_ALL}\n")
        elif taxa >= 40:
            print(f"{Fore.LIGHTYELLOW_EX}💪 Mais um esforço! Você consegue!{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.LIGHTRED_EX}🎓 Estude mais e tente novamente!{Style.RESET_ALL}\n")
        
        input(f"{Fore.CYAN}Pressione Enter para voltar ao menu...{Style.RESET_ALL}")
    
    def jogar_categoria(self, categoria):
        """Executa o jogo de uma categoria"""
        if categoria == "1":
            questoes = self.questoes_geometria()
            nome = "GEOMETRIA"
        elif categoria == "2":
            questoes = self.questoes_probabilidade()
            nome = "PROBABILIDADE"
        elif categoria == "3":
            questoes = self.questoes_proporcoes()
            nome = "PROPORÇÕES"
        else:
            return
        
        random.shuffle(questoes)
        
        for i, questao in enumerate(questoes, 1):
            resposta = self.fazer_pergunta(questao, i)
            self.questoes_respondidas += 1
            self.verificar_resposta(resposta, questao)
            time.sleep(2)
        
        self.exibir_resultado_rodada(len(questoes))
    
    def jogar_desafio_total(self):
        """Modo desafio com todas as categorias"""
        todas_questoes = (
            self.questoes_geometria() + 
            self.questoes_probabilidade() + 
            self.questoes_proporcoes()
        )
        
        random.shuffle(todas_questoes)
        
        for i, questao in enumerate(todas_questoes, 1):
            resposta = self.fazer_pergunta(questao, i)
            self.questoes_respondidas += 1
            self.verificar_resposta(resposta, questao)
            time.sleep(2)
        
        self.exibir_resultado_rodada(len(todas_questoes))
    
    def exibir_recordes(self):
        """Exibe recordes do jogo"""
        self.limpar_tela()
        self.exibir_cabecalho()
        
        print(f"{Back.LIGHTMAGENTA_EX}{Fore.BLACK}{'RECORDES DO JOGO'.center(60)}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Sua Performance:")
        print(f"{Fore.YELLOW}{'─'*60}")
        print(f"{Fore.LIGHTYELLOW_EX}Total de Questões: {self.questoes_respondidas}")
        print(f"{Fore.LIGHTGREEN_EX}Total de Acertos: {self.acertos}")
        print(f"{Fore.LIGHTRED_EX}Total de Erros: {self.erros}")
        print(f"{Fore.LIGHTMAGENTA_EX}Maior Combo: x{self.max_combo}")
        print(f"{Fore.LIGHTCYAN_EX}Melhor Taxa: {self._calcular_taxa():.1f}%")
        print(f"{Fore.LIGHTYELLOW_EX}Pontuação Total: {self.pontuacao} pts")
        print(f"{Fore.YELLOW}{'─'*60}\n")
        
        input(f"{Fore.CYAN}Pressione Enter para voltar...{Style.RESET_ALL}")
    
    def iniciar(self):
        """Inicia o jogo"""
        while True:
            opcao = self.exibir_menu_inicial()
            
            if opcao == "1":
                self.jogar_categoria("1")
            elif opcao == "2":
                self.jogar_categoria("2")
            elif opcao == "3":
                self.jogar_categoria("3")
            elif opcao == "4":
                self.jogar_desafio_total()
            elif opcao == "5":
                self.exibir_recordes()
            elif opcao == "0":
                self.limpar_tela()
                print(f"{Fore.LIGHTGREEN_EX}\n{'Obrigado por jogar FOLCLORE MATH!'.center(60)}\n")
                print(f"{Fore.CYAN}{'Sua Pontuação Final: ' + str(self.pontuacao)+ ' pts'.center(60)}\n")
                print(f"{Fore.YELLOW}{'Até logo! 👋'.center(60)}\n{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}⚠️  Opção inválida! Tente novamente.{Style.RESET_ALL}")
                time.sleep(1)


# ==================== PROGRAMA PRINCIPAL ====================
if __name__ == "__main__":
    jogo = FolcloreMath()
    jogo.iniciar()