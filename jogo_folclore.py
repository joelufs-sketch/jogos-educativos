import tkinter as tk
import random
import math


class JogoFolclore:
    def __init__(self, root):
        self.root = root
        root.title("Matemática do Folclore - Pega-Pipa")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="#87CEEB", highlightthickness=0)
        self.canvas.pack()

        # Cenário simples
        self.canvas.create_oval(700, 50, 790, 140, fill="#F4D03F", outline="")
        self.canvas.create_oval(80, 80, 180, 130, fill="white", outline="")
        self.canvas.create_oval(120, 65, 220, 115, fill="white", outline="")
        self.canvas.create_oval(600, 120, 700, 170, fill="white", outline="")

        # Cesta do jogador
        self.player_x = 400
        self.player_y = 535
        self.player_id = self.canvas.create_polygon(
            400 - 55, 535 - 25,
            400 + 55, 535 - 25,
            400 + 55, 535 + 20,
            400 - 55, 535 + 20,
            fill="#D2691E",
            outline="#8B4513",
            width=3
        )
        self.player_label = self.canvas.create_text(
            self.player_x, self.player_y - 40,
            text="CESTA",
            font=("Arial", 12, "bold"),
            fill="#8B4513"
        )

        self.keys = {"Left": False, "Right": False, "a": False, "d": False}
        self.items = []
        self.floating = []

        self.score = 0
        self.lives = 3
        self.level = 1
        self.level_up_score = 100
        self.speed = 2.0
        self.spawn_interval = 1000

        self.paused = False
        self.game_over = False
        self.overlay = None

        self.criar_hud()
        self.bind_events()

        self.root.after(800, self.spawn_item)
        self.root.after(40, self.update)
        self.root.mainloop()

    def criar_hud(self):
        self.canvas.create_rectangle(0, 0, 800, 45, fill="#FDF5E6", outline="", tags="hud")
        self.score_text = self.canvas.create_text(
            80, 22, text="Pontos: 0",
            font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud"
        )
        self.lives_text = self.canvas.create_text(
            220, 22, text="Vidas: 3",
            font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud"
        )
        self.level_text = self.canvas.create_text(
            360, 22, text="Nível: 1",
            font=("Arial", 14, "bold"), fill="#2C3E50", tags="hud"
        )
        self.canvas.create_text(
            600, 22,
            text="← → ou A/D | Mouse | Espaço pausa | R reinicia",
            font=("Arial", 10), fill="#7F8C8D", tags="hud"
        )

    def bind_events(self):
        self.root.bind("<KeyPress>", self.press)
        self.root.bind("<KeyRelease>", self.release)
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<p>", self.toggle_pause)
        self.root.bind("<r>", self.restart)
        self.root.bind("<Motion>", self.mouse_move)

    def press(self, event):
        k = event.keysym
        if k == "Left":
            self.keys["Left"] = True
        elif k == "Right":
            self.keys["Right"] = True
        elif k.lower() == "a":
            self.keys["a"] = True
        elif k.lower() == "d":
            self.keys["d"] = True

    def release(self, event):
        k = event.keysym
        if k == "Left":
            self.keys["Left"] = False
        elif k == "Right":
            self.keys["Right"] = False
        elif k.lower() == "a":
            self.keys["a"] = False
        elif k.lower() == "d":
            self.keys["d"] = False

    def mouse_move(self, event):
        if not self.game_over and not self.paused:
            if 40 <= event.x <= 760:
                self.player_x = event.x

    def update(self):
        if not self.game_over and not self.paused:
            self.move_player()
            self.update_items()

            if self.game_over:
                self.root.after(40, self.update)
                return

            self.update_floating()
            self.update_hud()
            self.canvas.tag_raise("hud")

            if self.score >= self.level_up_score:
                self.level_up()

        self.root.after(40, self.update)

    def move_player(self):
        dx = 0
        if self.keys["Left"] or self.keys["a"]:
            dx -= 8
        if self.keys["Right"] or self.keys["d"]:
            dx += 8

        self.player_x = max(60, min(740, self.player_x + dx))
        self.update_player()

    def update_player(self):
        x = self.player_x
        y = self.player_y
        self.canvas.coords(
            self.player_id,
            x - 55, y - 25,
            x + 55, y - 25,
            x + 55, y + 20,
            x - 55, y + 20
        )
        self.canvas.coords(self.player_label, x, y - 40)

    def pontos_pipa(self, cx, cy, r):
        return [
            cx, cy - r,
            cx + r * 0.7, cy,
            cx, cy + r,
            cx - r * 0.7, cy
        ]

    def pontos_estrela(self, cx, cy, r):
        pontos = []
        for i in range(10):
            angulo = math.pi / 2 + i * math.pi / 5
            raio = r if i % 2 == 0 else r * 0.5
            pontos.append(cx + raio * math.cos(angulo))
            pontos.append(cy - raio * math.sin(angulo))
        return pontos

    def spawn_item(self):
        if self.paused or self.game_over:
            self.root.after(200, self.spawn_item)
            return

        roll = random.random()

        if roll < 0.30:
            kind = "pipa"
            score = 20
            r = 25
            cor = random.choice(["#E74C3C", "#3498DB", "#9B59B6", "#E67E22"])
        elif roll < 0.65:
            kind = "milho"
            score = 10
            r = 12
            cor = "#F1C40F"
        elif roll < 0.85:
            kind = "pedra"
            score = -1
            r = 12
            cor = "#95A5A6"
        else:
            kind = "estrela"
            score = 50
            r = 20
            cor = "#F7DC6F"

        x = random.randint(60, 740)
        y = -30
        vy = random.uniform(self.speed, self.speed + 1.2)

        item = {
            "id": None,
            "kind": kind,
            "score": score,
            "r": r,
            "cor": cor,
            "x": x,
            "y": y,
            "vy": vy,
            "angle": random.uniform(0, math.pi * 2)
        }

        if kind == "pipa":
            item["id"] = self.canvas.create_polygon(
                *self.pontos_pipa(x, y, r),
                fill=cor, outline="#2C3E50", width=2
            )
        elif kind == "estrela":
            item["id"] = self.canvas.create_polygon(
                *self.pontos_estrela(x, y, r),
                fill=cor, outline="#F39C12", width=2
            )
        else:
            item["id"] = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=cor, outline="#7F8C8D", width=2
            )

        self.items.append(item)
        self.root.after(self.spawn_interval, self.spawn_item)

    def update_items(self):
        for item in self.items[:]:
            item["y"] += item["vy"]

            if item["kind"] in ("pipa", "estrela"):
                item["angle"] += 0.05
                item["x"] += math.sin(item["angle"]) * 0.4
                item["x"] = max(40, min(760, item["x"]))

            if item["kind"] in ("milho", "pedra"):
                r = item["r"]
                self.canvas.coords(
                    item["id"],
                    item["x"] - r,
                    item["y"] - r,
                    item["x"] + r,
                    item["y"] + r
                )
            elif item["kind"] == "pipa":
                self.canvas.coords(
                    item["id"],
                    *self.pontos_pipa(item["x"], item["y"], item["r"])
                )
            elif item["kind"] == "estrela":
                self.canvas.coords(
                    item["id"],
                    *self.pontos_estrela(item["x"], item["y"], item["r"])
                )

            if item["y"] - item["r"] > 620:
                self.canvas.delete(item["id"])
                self.items.remove(item)
                continue

            if self.colidiu(item):
                self.pegar_item(item)

    def colidiu(self, item):
        x1 = self.player_x - 55
        x2 = self.player_x + 55
        y1 = self.player_y - 25
        y2 = self.player_y + 20
        r = item["r"]
        return (x1 - r < item["x"] < x2 + r) and (y1 - r < item["y"] < y2 + r)

    def pegar_item(self, item):
        if item["score"] >= 0:
            self.score += item["score"]
            self.add_floating(item["x"], item["y"], f"+{item['score']}", "#27AE60")
            if item["kind"] == "estrela":
                self.add_floating(item["x"], item["y"] - 30, "BÔNUS!", "#F39C12")
        else:
            self.lives -= 1
            self.add_floating(item["x"], item["y"], "-1 vida", "#E74C3C")
            self.canvas.itemconfig(self.player_id, fill="#E74C3C")
            self.root.after(
                120,
                lambda: self.canvas.itemconfig(self.player_id, fill="#D2691E")
            )

        self.canvas.delete(item["id"])
        if item in self.items:
            self.items.remove(item)

        if self.lives <= 0:
            self.fim_de_jogo()

    def add_floating(self, x, y, texto, cor):
        fid = self.canvas.create_text(
            x, y, text=texto,
            font=("Arial", 16, "bold"), fill=cor
        )
        self.floating.append({"id": fid, "x": x, "y": y, "life": 30})

    def update_floating(self):
        for f in self.floating[:]:
            f["life"] -= 1
            f["y"] -= 1.5
            self.canvas.coords(f["id"], f["x"], f["y"])
            if f["life"] <= 0:
                self.canvas.delete(f["id"])
                self.floating.remove(f)

    def update_hud(self):
        self.canvas.itemconfig(self.score_text, text=f"Pontos: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Vidas: {self.lives}")
        self.canvas.itemconfig(self.level_text, text=f"Nível: {self.level}")

    def level_up(self):
        if self.game_over:
            return

        self.level += 1
        self.level_up_score += 100 * self.level
        self.speed += 0.35
        self.spawn_interval = max(450, self.spawn_interval - 80)

        if self.level % 3 == 0:
            self.lives += 1
            self.add_floating(400, 300, "Vida extra!", "#2ECC71")

        self.canvas.configure(bg=random.choice([
            "#A9DFBF", "#AED6F1", "#F9E79F", "#D7BDE2", "#F5CBA7"
        ]))

        self.add_floating(400, 280, f"SUBINDO PARA O NÍVEL {self.level}!", "#E67E22")
        self.update_hud()

    def toggle_pause(self, _event=None):
        if self.game_over:
            return

        self.paused = not self.paused

        if self.paused:
            self.overlay = self.canvas.create_text(
                400, 300,
                text="PAUSADO\n\nPressione Espaço para continuar",
                font=("Arial", 30, "bold"),
                fill="#2C3E50",
                justify="center"
            )
        else:
            if self.overlay:
                self.canvas.delete(self.overlay)
                self.overlay = None

    def fim_de_jogo(self):
        self.game_over = True

        if self.overlay:
            self.canvas.delete(self.overlay)
            self.overlay = None

        self.overlay = self.canvas.create_text(
            400, 300,
            text=f"FIM DE JOGO!\n\nPontos: {self.score}  |  Nível: {self.level}\n\nPressione R para reiniciar",
            font=("Arial", 28, "bold"),
            fill="#C0392B",
            justify="center"
        )

    def restart(self, _event=None):
        for item in self.items:
            self.canvas.delete(item["id"])
        for f in self.floating:
            self.canvas.delete(f["id"])

        self.items.clear()
        self.floating.clear()

        if self.overlay:
            self.canvas.delete(self.overlay)
            self.overlay = None

        self.score = 0
        self.lives = 3
        self.level = 1
        self.level_up_score = 100
        self.speed = 2.0
        self.spawn_interval = 1000
        self.paused = False
        self.game_over = False
        self.player_x = 400
        self.keys = {"Left": False, "Right": False, "a": False, "d": False}

        self.update_player()
        self.canvas.configure(bg="#87CEEB")
        self.update_hud()
        self.add_floating(400, 400, "Bora jogar!", "#16A085")


if __name__ == "__main__":
    raiz = tk.Tk()
    JogoFolclore(raiz)