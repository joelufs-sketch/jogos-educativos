import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import date
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ==================================================================
# 👇 LISTA DE ALUNOS POR TURMA
# ==================================================================
ALUNOS_POR_TURMA = {
    "Turma 01 (6º Ano)": [
        "Bruniel", "Davi Luiz", "Davi Nascimento", "Dhonatas", "Elison",
        "Fernando", "Jhonata", "João Miguel", "José Clenisson", "José Wesley",
        "Julian", "Lázaro", "Lucyana", "Monaliza", "Pedro",
        "Rayane", "Wadrian", "Wendel", "Wilson", "Luandoson"
    ],
    "Turma 02 (7º Ano)": [
        "Adriel Lianda", "Adriel Coutinho", "Arthur", "Beatriz", "Bianca",
        "Brunieli", "Carlos Fernando", "Enzo", "Evillyn", "Fernando",
        "Italo Souza", "Jullia", "Maria Macedo", "Maria Coutinho", "Matheus",
        "Mirelly", "Nicolas", "Nicolly", "Ueverte", "Weslen",
        "Ysadora", "Ytallo Kauã", "Yuri", "Beatriz"
    ],
    "Turma 03 (Integral)": [
        "Julian", "Bianca", "Ítalo Souza", "Maria Eduarda",
        "Maria Heloísa Leite", "Gabi Terra", "Izadora", "Reinaldo"
    ],
    "Turma 04 (Intensivão)": [
        "Arthur", "Deivid", "Emilly", "Enzo Gabriel", "Felipe",
        "Gabi Terra", "Izadora", "Jhonatas", "José Guilherme", "Jullia",
        "Lucas", "Marcos", "Matheus", "Maria Estefanny", "Maria Vitória",
        "Maysa", "Whellen"
    ],
}

# ==================================================================
# 👇 CONFIGURAÇÃO DO E-MAIL (SÓ COLE A SENHA)
# ==================================================================
EMAIL_REMETENTE = "joel.ufs@gmail.com"
SENHA_REMETENTE = os.getenv("CHAMADA_EMAIL_SENHA", "")
EMAIL_DESTINATARIO = "joel_somaresia@hotmail.com"
# ==================================================================


class ChamadaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chamada Interativa - Frequência por E-mail")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        self.data_hoje = date.today().strftime("%d/%m/%Y")

        self.frame_menu = tk.Frame(self.root, bg="#FDF5E6")
        self.frame_chamada = tk.Frame(self.root, bg="#FDF5E6")

        self.estados = {}
        for turma, nomes in ALUNOS_POR_TURMA.items():
            self.estados[turma] = {
                "indice": 0,
                "status": [None] * len(nomes)
            }

        self.mostrar_menu()

    # ==================================================================
    # TELA INICIAL
    # ==================================================================
    def mostrar_menu(self):
        self.frame_chamada.pack_forget()

        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        self.frame_menu.pack(fill="both", expand=True)

        tk.Label(
            self.frame_menu,
            text="📋 Chamada Interativa",
            font=("Arial", 30, "bold"),
            bg="#FDF5E6",
            fg="#2C3E50"
        ).pack(pady=(50, 10))

        tk.Label(
            self.frame_menu,
            text="Escolha uma turma para iniciar ou continuar:",
            font=("Arial", 14),
            bg="#FDF5E6",
            fg="#7F8C8D"
        ).pack()

        area_botoes = tk.Frame(self.frame_menu, bg="#FDF5E6")
        area_botoes.pack(pady=40)

        for posicao, (turma, nomes) in enumerate(ALUNOS_POR_TURMA.items()):
            estado = self.estados[turma]
            marcados = sum(1 for s in estado["status"] if s is not None)
            total = len(nomes)

            texto = f"{turma}\n{marcados}/{total} alunos"

            if marcados == total and total > 0:
                texto += "\n✔ Concluída"

            btn = tk.Button(
                area_botoes,
                text=texto,
                font=("Arial", 13, "bold"),
                bg="#3498DB",
                fg="white",
                activebackground="#2980B9",
                activeforeground="white",
                width=20,
                height=3,
                relief="flat",
                cursor="hand2",
                command=lambda t=turma: self.abrir_turma(t)
            )

            linha = posicao // 2
            coluna = posicao % 2
            btn.grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")

        area_botoes.grid_columnconfigure(0, weight=1)
        area_botoes.grid_columnconfigure(1, weight=1)

    def abrir_turma(self, turma):
        self.turma = turma
        self.frame_menu.pack_forget()
        self.frame_chamada.pack(fill="both", expand=True)
        self.atualizar_tela()

    def voltar_menu(self):
        self.frame_chamada.pack_forget()
        self.mostrar_menu()

    # ==================================================================
    # TELA DE CHAMADA
    # ==================================================================
    def atualizar_tela(self):
        for widget in self.frame_chamada.winfo_children():
            widget.destroy()

        estado = self.estados[self.turma]
        total = len(ALUNOS_POR_TURMA[self.turma])

        if estado["indice"] >= total:
            self.montar_resumo()
        else:
            self.montar_chamada()

    def montar_chamada(self):
        estado = self.estados[self.turma]
        alunos = ALUNOS_POR_TURMA[self.turma]
        indice = estado["indice"]
        nome = alunos[indice]

        topo = tk.Frame(self.frame_chamada, bg="#FDF5E6")
        topo.pack(fill="x", padx=15, pady=15)

        tk.Button(
            topo,
            text="← Turmas",
            font=("Arial", 11, "bold"),
            bg="#BDC3C7",
            fg="#2C3E50",
            activebackground="#95A5A6",
            relief="flat",
            cursor="hand2",
            command=self.voltar_menu
        ).pack(side="left")

        tk.Label(
            topo,
            text=f"Turma: {self.turma}",
            font=("Arial", 16, "bold"),
            bg="#FDF5E6",
            fg="#2C3E50"
        ).pack(side="left", padx=30)

        tk.Label(
            topo,
            text=f"Data: {self.data_hoje}",
            font=("Arial", 12),
            bg="#FDF5E6",
            fg="#7F8C8D"
        ).pack(side="right")

        area_central = tk.Frame(self.frame_chamada, bg="#ECF0F1")
        area_central.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(
            area_central,
            text=f"Aluno {indice + 1} de {len(alunos)}",
            font=("Arial", 14, "bold"),
            bg="#ECF0F1",
            fg="#7F8C8D"
        ).pack(pady=(30, 10))

        tk.Label(
            area_central,
            text=nome,
            font=("Arial", 50, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=(10, 20))

        tk.Label(
            area_central,
            text="Clique em um botão para marcar e ir para o próximo aluno:",
            font=("Arial", 12),
            bg="#ECF0F1",
            fg="#95A5A6"
        ).pack(pady=(0, 30))

        botoes = tk.Frame(area_central, bg="#ECF0F1")
        botoes.pack(pady=20)

        btn_presente = tk.Button(
            botoes,
            text="PRESENTE\n(Avançar)",
            font=("Arial", 13, "bold"),
            bg="#2ECC71",
            fg="white",
            activebackground="#27AE60",
            activeforeground="white",
            width=16,
            height=3,
            relief="flat",
            cursor="hand2",
            command=lambda: self.marcar("P")
        )
        btn_presente.pack(side="left", padx=12)

        btn_justificar = tk.Button(
            botoes,
            text="JUSTIFICAR\n(Avançar)",
            font=("Arial", 13, "bold"),
            bg="#F39C12",
            fg="white",
            activebackground="#E67E22",
            activeforeground="white",
            width=16,
            height=3,
            relief="flat",
            cursor="hand2",
            command=lambda: self.marcar("J")
        )
        btn_justificar.pack(side="left", padx=12)

        btn_falta = tk.Button(
            botoes,
            text="FALTA (F)\n(Avançar)",
            font=("Arial", 13, "bold"),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            width=16,
            height=3,
            relief="flat",
            cursor="hand2",
            command=lambda: self.marcar("F")
        )
        btn_falta.pack(side="left", padx=12)

    def marcar(self, status):
        estado = self.estados[self.turma]
        indice = estado["indice"]
        estado["status"][indice] = status
        estado["indice"] += 1
        self.atualizar_tela()

    # ==================================================================
    # RESUMO FINAL
    # ==================================================================
    def montar_resumo(self):
        estado = self.estados[self.turma]
        alunos = ALUNOS_POR_TURMA[self.turma]

        presentes = []
        justificados = []
        faltosos = []

        for i, aluno in enumerate(alunos):
            if estado["status"][i] == "P":
                presentes.append(aluno)
            elif estado["status"][i] == "J":
                justificados.append(aluno)
            elif estado["status"][i] == "F":
                faltosos.append(aluno)

        barra = tk.Frame(self.frame_chamada, bg="#FDF5E6")
        barra.pack(side="bottom", fill="x", padx=15, pady=15)

        tk.Button(
            barra,
            text="← Turmas",
            font=("Arial", 11, "bold"),
            bg="#BDC3C7",
            fg="#2C3E50",
            activebackground="#95A5A6",
            relief="flat",
            cursor="hand2",
            command=self.voltar_menu
        ).pack(side="left", padx=5)

        tk.Button(
            barra,
            text="↻ Reiniciar chamada",
            font=("Arial", 11, "bold"),
            bg="#F5B041",
            fg="white",
            activebackground="#D68910",
            relief="flat",
            cursor="hand2",
            command=self.reiniciar_turma
        ).pack(side="right", padx=5)

        tk.Button(
            barra,
            text="💾 Salvar CSV",
            font=("Arial", 11, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="flat",
            cursor="hand2",
            command=self.salvar_csv
        ).pack(side="right", padx=5)

        tk.Button(
            barra,
            text="📧 Enviar e-mail",
            font=("Arial", 11, "bold"),
            bg="#8E44AD",
            fg="white",
            activebackground="#7D3C98",
            relief="flat",
            cursor="hand2",
            command=self.enviar_email
        ).pack(side="right", padx=5)

        central = tk.Frame(self.frame_chamada, bg="#FDF5E6")
        central.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(
            central,
            text="✅ Chamada concluída!",
            font=("Arial", 22, "bold"),
            bg="#FDF5E6",
            fg="#27AE60"
        ).pack(pady=(10, 5))

        tk.Label(
            central,
            text=f"Frequência da turma {self.turma} concluída em {self.data_hoje}",
            font=("Arial", 15, "bold"),
            bg="#FDF5E6",
            fg="#2C3E50"
        ).pack(pady=(5, 10))

        tk.Label(
            central,
            text=f"Presentes: {len(presentes)}   •   Justificados: {len(justificados)}   •   Faltosos: {len(faltosos)}",
            font=("Arial", 13),
            bg="#FDF5E6",
            fg="#7F8C8D"
        ).pack(pady=(0, 10))

        lista_area = tk.Frame(central, bg="#FDF5E6")
        lista_area.pack(fill="both", expand=True, pady=15)

        coluna_faltosos = self.criar_coluna_lista(
            lista_area,
            "FALTOSOS (F)",
            faltosos,
            "#E74C3C",
            "#FDEDEC"
        )
        coluna_faltosos.pack(side="left", fill="both", expand=True, padx=10)

        coluna_justificados = self.criar_coluna_lista(
            lista_area,
            "JUSTIFICADOS",
            justificados,
            "#F39C12",
            "#FEF5E7"
        )
        coluna_justificados.pack(side="left", fill="both", expand=True, padx=10)

    def criar_coluna_lista(self, pai, titulo, itens, cor_titulo, cor_fundo):
        frame = tk.Frame(pai, bg="#FDF5E6")

        tk.Label(
            frame,
            text=f"{titulo} ({len(itens)})",
            font=("Arial", 15, "bold"),
            bg="#FDF5E6",
            fg=cor_titulo
        ).pack(pady=(0, 5))

        texto_widget = tk.Text(
            frame,
            width=35,
            height=10,
            font=("Arial", 12),
            bg=cor_fundo,
            fg="#2C3E50",
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=texto_widget.yview)
        texto_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        texto_widget.pack(side="left", fill="both", expand=True)

        if itens:
            texto = "\n".join(f"• {nome}" for nome in itens)
            texto_widget.insert("1.0", texto)
        else:
            texto_widget.insert("1.0", "Nenhum aluno")

        texto_widget.config(state="disabled")

        return frame

    def reiniciar_turma(self):
        resposta = messagebox.askyesno(
            "Reiniciar",
            f"Reiniciar a chamada da {self.turma}?"
        )

        if resposta:
            estado = self.estados[self.turma]
            estado["indice"] = 0
            estado["status"] = [None] * len(ALUNOS_POR_TURMA[self.turma])
            self.atualizar_tela()

    # ==================================================================
    # GERAR CSV
    # ==================================================================
    def gerar_csv(self):
        estado = self.estados[self.turma]
        alunos = ALUNOS_POR_TURMA[self.turma]

        nome_arquivo = f"frequencia_{self.turma.replace(' ', '_').replace('/', '-')}_{self.data_hoje.replace('/', '-')}.csv"

        with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["Turma", self.turma])
            writer.writerow(["Data", self.data_hoje])
            writer.writerow([])
            writer.writerow(["Aluno", "Status"])

            for i, aluno in enumerate(alunos):
                status = estado["status"][i]
                if status == "P":
                    status_texto = "PRESENTE"
                elif status == "J":
                    status_texto = "JUSTIFICADO"
                elif status == "F":
                    status_texto = "FALTA"
                else:
                    status_texto = "NÃO MARCADO"

                writer.writerow([aluno, status_texto])

        return nome_arquivo

    def salvar_csv(self):
        nome_arquivo = self.gerar_csv()
        messagebox.showinfo(
            "CSV gerado",
            f"Planilha salva como:\n{nome_arquivo}\n\nAbra no Excel ou em um editor de texto."
        )

    # ==================================================================
    # ENVIAR E-MAIL
    # ==================================================================
    def enviar_email(self):
        if not SENHA_REMETENTE:
            messagebox.showerror(
                "Configuração necessária",
                "Defina a variável de ambiente CHAMADA_EMAIL_SENHA com sua senha de app do Gmail."
            )
            return

        try:
            nome_arquivo = self.gerar_csv()

            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = EMAIL_DESTINATARIO
            msg["Subject"] = f"Frequência {self.turma} - {self.data_hoje}"

            corpo = f"Olá!\n\nSegue em anexo a frequência da turma {self.turma} do dia {self.data_hoje}.\n\nAtenciosamente."
            msg.attach(MIMEText(corpo, "plain", "utf-8"))

            with open(nome_arquivo, "rb") as anexo:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(anexo.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {nome_arquivo}"
                )
                msg.attach(part)

            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
            servidor.quit()

            messagebox.showinfo(
                "E-mail enviado",
                f"Planilha enviada com sucesso para:\n{EMAIL_DESTINATARIO}"
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro ao enviar e-mail",
                f"Não foi possível enviar o e-mail.\n\nErro:\n{erro}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = ChamadaApp(root)
    root.mainloop()