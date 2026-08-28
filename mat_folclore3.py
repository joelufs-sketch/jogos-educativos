import tkinter as tk
import random
import math


class JogoAssociacao:
    def __init__(self, root):
        self.root = root
        root.title("Matemática do Folclore - Arraste e Solte")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=900, height=600, bg="#87CEEB", highlightthickness=0)
        self.canvas.pack()

        self.tipos = ["pipa", "peao", "amarelinha", "peteca"]
        self.cores = {
            "pipa": "#E74C3C",
            "peao": "#3498DB",
            "amarelinha": "#27AE60",
            "peteca": "#F39C12"
        }

        self.tempo = 0
        self.score = 0
        self.lives = 3
        self.level = 1
        self.combo = 0
        self.pares = []
        self.arrastando = None
        self.offset_x = 0
        self.offset_y = 0
        self.raio = 35
        self.alvo_raio = 35
        self.game_over = False
        self.overlay = None

        self.criar_hud()
        self.gerar_nivel()

        self.canvas.bind("<Button-1>", self.iniciar_arraste)
        self.canvas.bind("<B1-Motion>", self.mover_arraste)
        self.canvas.bind("<ButtonRelease-1>", self.soltar_arraste)
        self.root.bind_all("<KeyPress-r>", self.reiniciar)
        self.root.bind_all("<KeyPress-R>", self.reiniciar)

        self.atualizar_hud()
        self.animar()

    # ------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------
    def criar_hud(self):
        self.canvas.create_rectangle(0, 0, 900, 50, fill="#FDF5E6", outline="", tags="hud")
        self.score_text = self.canvas.create_text(70, 25, text="Pontos: 0", font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud")
        self.lives_text = self.canvas.create_text(200, 25, text="Vidas: 3", font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud")
        self.level_text = self.canvas.create_text(330, 25, text="Nível: 1", font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud")
        self.combo_text = self.canvas.create_text(460, 25, text="Combo: x1", font=("Arial", 14, "bold"), fill="#E67E22", tags="hud")
        self.canvas.create_text(650, 25, text="Arraste cada brinquedo para a forma certa!", font=("Arial", 11), fill="#7F8C8D", tags="hud")

    def atualizar_hud(self):
        self.canvas.itemconfig(self.score_text, text=f"Pontos: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Vidas: {self.lives}")
        self.canvas.itemconfig(self.level_text, text=f"Nível: {self.level}")
        self.canvas.itemconfig(self.combo_text, text=f"Combo: x{max(1, self.combo)}")
        self.canvas.tag_raise("hud")

    # ------------------------------------------------------------
    # Formas geométricas
    # ------------------------------------------------------------
    def coords_forma(self, tipo, cx, cy, r):
        if tipo == "pipa":
            return [cx, cy - r, cx + r * 0.8, cy, cx, cy + r, cx - r * 0.8, cy]
        elif tipo == "peao":
            return [cx - r, cy - r, cx + r, cy + r]
        elif tipo == "amarelinha":
            return [cx - r, cy - r, cx + r, cy - r, cx + r, cy + r, cx - r, cy + r]
        elif tipo == "peteca":
            return [cx, cy - r, cx + r, cy + r, cx - r, cy + r]
        elif tipo == "estrela":
            pts = []
            for i in range(10):
                ang = math.pi / 2 + i * math.pi / 5
                raio = r if i % 2 == 0 else r * 0.4
                pts.extend([cx + raio * math.cos(ang), cy - raio * math.sin(ang)])
            return pts
        elif tipo == "hexagono":
            pts = []
            for i in range(6):
                ang = math.pi / 6 + i * 2 * math.pi / 6
                pts.extend([cx + r * math.cos(ang), cy + r * math.sin(ang)])
            return pts

    def desenhar_forma(self, tipo, cx, cy, r, fill, outline, dash=None):
        coords = self.coords_forma(tipo, cx, cy, r)
        if tipo == "peao":
            return self.canvas.create_oval(*coords, fill=fill, outline=outline, width=3, dash=dash)
        else:
            return self.canvas.create_polygon(*coords, fill=fill, outline=outline, width=3, dash=dash)

    # ------------------------------------------------------------
    # Geração de níveis
    # ------------------------------------------------------------
    def gerar_nivel(self):
        # Limpa itens antigos
        for par in self.pares:
            self.canvas.delete(par["alvo_id"])
            self.canvas.delete(par["forma_id"])
            self.canvas.delete(par["nome_id"])

        self.pares.clear()

        # Número de pares por nível
        n_pares = min(2 + self.level - 1, len(self.tipos))

        # Escolhe tipos aleatórios
        tipos_escolhidos = random.sample(self.tipos, n_pares)

        # Raio diminui nos níveis altos
        self.raio = max(22, 35 - (self.level - 1) * 2)
        self.alvo_raio = max(22, 35 - (self.level - 1) * 2)

        # Posições dos alvos no topo
        alvo_positions = []
        for i in range(n_pares):
            x = 900 // (n_pares + 1) * (i + 1)
            y = 120
            alvo_positions.append((x, y))

        # Posições dos brinquedos embaixo, embaralhadas
        brinquedo_positions = []
        ordem = list(range(n_pares))
        random.shuffle(ordem)
        for i, indice in enumerate(ordem):
            x = 900 // (n_pares + 1) * (i + 1)
            y = 500
            brinquedo_positions.append((x, y, indice))

        # Cria os pares
        for i, tipo in enumerate(tipos_escolhidos):
            ax, ay = alvo_positions[i]
            bx, by, _ = brinquedo_positions[i]

            alvo_id = self.desenhar_forma(
                tipo, ax, ay, self.alvo_raio,
                fill="", outline="#7F8C8D", dash=(5, 3)
            )

            forma_id = self.desenhar_forma(
                tipo, bx, by, self.raio,
                fill=self.cores[tipo], outline="#2C3E50"
            )

            nome_id = self.canvas.create_text(
                bx, by + self.raio + 15,
                text=tipo.capitalize(),
                font=("Arial", 11, "bold"),
                fill="#2C3E50"
            )

            self.pares.append({
                "tipo": tipo,
                "alvo_id": alvo_id,
                "alvo_x": ax,
                "alvo_y": ay,
                "forma_id": forma_id,
                "nome_id": nome_id,
                "orig_x": bx,
                "orig_y": by,
                "fase": random.uniform(0, math.pi * 2)
            })

        # Altera a cor do fundo a cada nível
        cores_fundo = ["#87CEEB", "#AED6F1", "#F9E79F", "#D7BDE2", "#F5CBA7"]
        novo_fundo = random.choice(cores_fundo)
        self.canvas.configure(bg=novo_fundo)

    # ------------------------------------------------------------
    # Eventos do mouse
    # ------------------------------------------------------------
    def iniciar_arraste(self, event):
        if self.game_over:
            return

        # Encontra o item clicado que pertence a um brinquedo
        item = self.canvas.find_withtag("current")
        if not item:
            return

        item = item[0]
        for par in self.pares:
            if par["forma_id"] == item or par["nome_id"] == item:
                self.arrastando = par
                # Calcula o offset para o brinquedo não "pular"
                self.offset_x = event.x - par["orig_x"]
                self.offset_y = event.y - par["orig_y"]
                return

    def mover_arraste(self, event):
        if self.arrastando is None or self.game_over:
            return

        par = self.arrastando
        novo_cx = event.x - self.offset_x
        novo_cy = event.y - self.offset_y

        # Atualiza a posição da forma
        coords = self.coords_forma(par["tipo"], novo_cx, novo_cy, self.raio)
        if par["tipo"] == "peao":
            self.canvas.coords(par["forma_id"], *coords)
        else:
            self.canvas.coords(par["forma_id"], *coords)

        # Atualiza o nome
        self.canvas.coords(par["nome_id"], novo_cx, novo_cy + self.raio + 15)

    def soltar_arraste(self, event):
        if self.arrastando is None or self.game_over:
            return

        par = self.arrastando
        self.arrastando = None

        novo_cx = event.x - self.offset_x
        novo_cy = event.y - self.offset_y

        # Verifica se soltou em cima do alvo correspondente
        distancia = math.hypot(novo_cx - par["alvo_x"], novo_cy - par["alvo_y"])

        if distancia < 70:
            self.acertou(par)
        else:
            self.errou(par)

    # ------------------------------------------------------------
    # Acerto e erro
    # ------------------------------------------------------------
    def acertou(self, par):
        self.combo += 1
        pontos = 10 + 2 * (self.combo - 1)
        self.score += pontos

        # Efeito visual
        self.criar_texto_flutuante(par["alvo_x"], par["alvo_y"], f"+{pontos}", "#27AE60")

        # Remove do canvas
        self.canvas.delete(par["alvo_id"])
        self.canvas.delete(par["forma_id"])
        self.canvas.delete(par["nome_id"])

        # Remove da lista
        self.pares.remove(par)

        self.atualizar_hud()

        # Se não há mais pares, próximo nível
        if not self.pares:
            self.level += 1
            self.combo = 0
            self.gerar_nivel()
            self.atualizar_hud()
            self.criar_texto_flutuante(450, 300, f"NÍVEL {self.level}!", "#E67E22")

    def errou(self, par):
        self.lives -= 1
        self.combo = 0

        # Retorna o brinquedo à posição original
        coords = self.coords_forma(par["tipo"], par["orig_x"], par["orig_y"], self.raio)
        if par["tipo"] == "peao":
            self.canvas.coords(par["forma_id"], *coords)
        else:
            self.canvas.coords(par["forma_id"], *coords)
        self.canvas.coords(par["nome_id"], par["orig_x"], par["orig_y"] + self.raio + 15)

        self.criar_texto_flutuante(par["orig_x"], par["orig_y"], "-1 vida", "#E74C3C")

        self.atualizar_hud()

        if self.lives <= 0:
            self.fim_de_jogo()

    # ------------------------------------------------------------
    # Efeitos
    # ------------------------------------------------------------
    def criar_texto_flutuante(self, x, y, texto, cor):
        tid = self.canvas.create_text(x, y, text=texto, font=("Arial", 18, "bold"), fill=cor)
        self.canvas.after(1000, lambda: self.canvas.delete(tid))  # simples

    # ------------------------------------------------------------
    # Animação dos brinquedos (flutuação)
    # ------------------------------------------------------------
    def animar(self):
        if self.game_over:
            return

        self.tempo += 1

        # Faz os brinquedos "flutuarem"
        for par in self.pares:
            if self.arrastando is par:
                continue

            desvio = math.sin(self.tempo * 0.05 + par["fase"]) * 5
            novo_y = par["orig_y"] + desvio

            coords = self.coords_forma(par["tipo"], par["orig_x"], novo_y, self.raio)
            if par["tipo"] == "peao":
                self.canvas.coords(par["forma_id"], *coords)
            else:
                self.canvas.coords(par["forma_id"], *coords)

            self.canvas.coords(par["nome_id"], par["orig_x"], novo_y + self.raio + 15)

        self.canvas.tag_raise("hud")
        self.root.after(30, self.animar)

    # ------------------------------------------------------------
    # Fim de jogo e reinício
    # ------------------------------------------------------------
    def fim_de_jogo(self):
        self.game_over = True

        self.overlay = self.canvas.create_text(
            450, 300,
            text=f"FIM DE JOGO!\n\nPontos: {self.score}\nNível: {self.level}\n\nPressione R para reiniciar",
            font=("Arial", 26, "bold"),
            fill="#C0392B",
            justify="center"
        )

    def reiniciar(self, event=None):
        self.game_over = False

        # Limpa tudo
        for par in self.pares:
            self.canvas.delete(par["alvo_id"])
            self.canvas.delete(par["forma_id"])
            self.canvas.delete(par["nome_id"])
        self.pares.clear()

        if self.overlay:
            self.canvas.delete(self.overlay)
            self.overlay = None

        self.score = 0
        self.lives = 3
        self.level = 1
        self.combo = 0
        self.tempo = 0
        self.raio = 35
        self.alvo_raio = 35

        self.canvas.configure(bg="#87CEEB")
        self.gerar_nivel()
        self.atualizar_hud()


if __name__ == "__main__":
    root = tk.Tk()
    JogoAssociacao(root)
    root.mainloop()