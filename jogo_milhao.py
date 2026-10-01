import customtkinter as ctk
import random
import perguntas_150
import nomes

#Configuração visual 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DARK    = "#05091a"
BG_CARD    = "#0a1840"
BLUE_MID   = "#1a3a90"
BLUE_LIGHT = "#4a7aff"
GOLD       = "#FFD700"
GOLD_DIM   = "#b8960a"
GREEN_HIT  = "#00c864"
RED_MISS   = "#dc3232"
ORANGE_SEL = "#FFB300"
TEXT_MAIN  = "#eeeeff"
TEXT_MUTED = "#7788aa"
SAFE_COLOR = "#4aaaff"

PRIZES = [
    "R$ 100", "R$ 200", "R$ 300", "R$ 500", "R$ 1.000",
    "R$ 2.000", "R$ 4.000", "R$ 8.000", "R$ 16.000", "R$ 32.000",
    "R$ 64.000", "R$ 125.000", "R$ 250.000", "R$ 500.000", "R$ 1.000.000",
]
SAFE_LEVELS = {7, 11}


class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Show do Milhão")
        self.geometry("980x680")
        self.minsize(880, 600)
        self.configure(fg_color=BG_DARK)

        # ── Estado (espelha as variáveis do main.py) ─────────────────
        self.ranking          = nomes.carregar_ranking()
        self.pontos           = 0
        self.continua         = False
        self.perguntas        = []
        self.pergunta_atual   = None
        self.selected_opt     = None
        self.confirmed        = False
        self.help50_used      = False
        self.helpskip_used    = False
        self.hidden_opts      = []
        self.opt_buttons      = []
        self.prize_labels     = []
        self.q_index          = 0

        self._tela_nome()

    
    #tela de nome

    def _tela_nome(self):
        self._limpar()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="SHOW DO MILHÃO",
                     font=ctk.CTkFont(size=36, weight="bold"),
                     text_color=GOLD).pack(pady=(0, 6))
        ctk.CTkLabel(frame, text="Digite seu nome para começar",
                     font=ctk.CTkFont(size=14),
                     text_color=TEXT_MUTED).pack(pady=(0, 24))

        self.entry_nome = ctk.CTkEntry(
            frame, width=320, height=48,
            font=ctk.CTkFont(size=18),
            placeholder_text="Seu nome...",
            fg_color=BG_CARD, border_color=BLUE_LIGHT,
            text_color=TEXT_MAIN, corner_radius=10
        )
        self.entry_nome.pack(pady=(0, 14))
        self.entry_nome.bind("<Return>", lambda e: self._nome())

        ctk.CTkButton(
            frame, text="COMEÇAR", width=320, height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=BLUE_MID, hover_color=BLUE_LIGHT,
            text_color=TEXT_MAIN, corner_radius=10,
            command=self._nome
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            frame, text="Ver Ranking", width=200, height=36,
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=BG_CARD,
            border_color=TEXT_MUTED, border_width=1,
            text_color=TEXT_MUTED, corner_radius=8,
            command=self._rank
        ).pack()

    def _nome(self):
        """def nome() do main.py"""
        nick = self.entry_nome.get().strip()
        if not nick:
            self.entry_nome.configure(border_color=RED_MISS)
            return

        #reseta estado
        self.pontos        = 0
        self.continua      = False
        self.q_index       = 0
        self.help50_used   = False
        self.helpskip_used = False
        self.perguntas     = list(perguntas_150.perguntas)

        self.ranking.append({'nickname': nick, 'record': 0})

        self._tela_jogo()


    #tela do jogo

    def _tela_jogo(self):
        self._limpar()

        root = ctk.CTkFrame(self, fg_color="transparent")
        root.pack(fill="both", expand=True, padx=16, pady=12)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        
        ladder = ctk.CTkScrollableFrame(
            root, width=160, fg_color=BG_CARD,
            border_color=BLUE_LIGHT, border_width=1, corner_radius=10
        )
        ladder.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        self.prize_labels = []
        for i in range(len(PRIZES) - 1, -1, -1):
            lbl = ctk.CTkLabel(
                ladder,
                text=f"    {i+1:02d}  {PRIZES[i]}",
                font=ctk.CTkFont(size=11),
                text_color=SAFE_COLOR if i in SAFE_LEVELS else TEXT_MUTED,
                anchor="w", width=148
            )
            lbl.pack(anchor="w", padx=6, pady=2)
            self.prize_labels.append((i, lbl))

        #painel central 
        center = ctk.CTkFrame(root, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew")
        center.columnconfigure(0, weight=1)

        #jogador e os seus pontos
        header = ctk.CTkFrame(center, fg_color=BG_CARD, corner_radius=10,
                               border_width=1, border_color=BLUE_LIGHT)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(0, weight=1)

        self.lbl_jogador = ctk.CTkLabel(
            header, text=f"👤  {self.ranking[-1]['nickname']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_MAIN, anchor="w"
        )
        self.lbl_jogador.grid(row=0, column=0, padx=16, pady=8, sticky="w")

        self.lbl_pontos = ctk.CTkLabel(
            header, text="0 pt(s)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=GOLD, anchor="e"
        )
        self.lbl_pontos.grid(row=0, column=1, padx=16, pady=8, sticky="e")

        #caixas de pergunta
        q_frame = ctk.CTkFrame(center, fg_color=BG_CARD, corner_radius=12,
                                border_width=1, border_color=BLUE_LIGHT)
        q_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        q_frame.columnconfigure(0, weight=1)

        self.lbl_q_num = ctk.CTkLabel(
            q_frame, text="",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=BLUE_LIGHT
        )
        self.lbl_q_num.grid(row=0, column=0, pady=(10, 4))

        self.lbl_q_texto = ctk.CTkLabel(
            q_frame, text="", wraplength=560,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_MAIN, justify="center"
        )
        self.lbl_q_texto.grid(row=1, column=0, padx=24, pady=(0, 12))

        # 5 opções
        opts_frame = ctk.CTkFrame(center, fg_color="transparent")
        opts_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        opts_frame.columnconfigure(0, weight=1)
        opts_frame.columnconfigure(1, weight=1)

        self.opt_buttons = []
        letras = ["A", "B", "C", "D", "E"]
        for i in range(5):
            
            if i < 4:
                linha, coluna = i // 2, i % 2
            else:
                linha, coluna = 2, 0   

            btn = ctk.CTkButton(
                opts_frame, text="", height=48, corner_radius=10,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=BG_CARD, hover_color="#152050",
                border_color=BLUE_LIGHT, border_width=1,
                text_color=TEXT_MAIN, anchor="w",
                command=lambda idx=i: self._selecionar(idx)
            )
            if i == 4:
                btn.grid(row=linha, column=0, columnspan=2,
                         padx=6, pady=4, sticky="ew")
            else:
                btn.grid(row=linha, column=coluna, padx=6, pady=4, sticky="ew")

            self.opt_buttons.append(btn)

        #ajudas
        helps = ctk.CTkFrame(center, fg_color="transparent")
        helps.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        helps.columnconfigure((0, 1, 2), weight=1)

        self.btn_50 = ctk.CTkButton(
            helps, text="50 / 50", height=38, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=BG_CARD, hover_color=BG_DARK,
            border_color=GOLD_DIM, border_width=1,
            text_color=GOLD, command=self._ajuda_50
        )
        self.btn_50.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_pular = ctk.CTkButton(
            helps, text="⏩  Pular", height=38, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=BG_CARD, hover_color=BG_DARK,
            border_color=GOLD_DIM, border_width=1,
            text_color=GOLD, command=self._ajuda_pular
        )
        self.btn_pular.grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(
            helps, text="🏆  Ranking", height=38, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=BG_CARD, hover_color=BG_DARK,
            border_color=TEXT_MUTED, border_width=1,
            text_color=TEXT_MUTED, command=self._rank
        ).grid(row=0, column=2, padx=5, sticky="ew")

        #confirmar
        self.btn_confirmar = ctk.CTkButton(
            center, text="CONFIRMAR RESPOSTA", height=46, corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=BLUE_MID, hover_color=BLUE_LIGHT,
            text_color=TEXT_MAIN, state="disabled",
            command=self._confirmar
        )
        self.btn_confirmar.grid(row=4, column=0, sticky="ew", pady=(0, 4))

        self.lbl_status = ctk.CTkLabel(
            center, text="",
            font=ctk.CTkFont(size=12), text_color=BLUE_LIGHT
        )
        self.lbl_status.grid(row=5, column=0)

        self._escolha()

    #codigo
    
    def _escolha(self):
        """def escolha() do main.py"""
        if not self.perguntas:
            self._fim_de_jogo(vitoria=True)
            return

        # pergunta = random.choice(perguntas_150.perguntas)
        # perguntas_150.perguntas.remove(pergunta)
        self.pergunta_atual = random.choice(self.perguntas)
        self.perguntas.remove(self.pergunta_atual)

        self.selected_opt = None
        self.confirmed    = False
        self.hidden_opts  = []

        self.lbl_q_num.configure(text=f"PERGUNTA {self.q_index + 1}")
        self.lbl_q_texto.configure(text=self.pergunta_atual['pergunta'])
        self.lbl_status.configure(text="")
        self.btn_confirmar.configure(state="disabled")

        letras = ["A", "B", "C", "D", "E"]
        for i, btn in enumerate(self.opt_buttons):
            btn.configure(
                text=f"  {letras[i]}.   {self.pergunta_atual['opcoes'][i]}",
                fg_color=BG_CARD, border_color=BLUE_LIGHT,
                text_color=TEXT_MAIN, state="normal"
            )

        if not self.help50_used:
            self.btn_50.configure(state="normal", text_color=GOLD,
                                  border_color=GOLD_DIM)
        if not self.helpskip_used:
            self.btn_pular.configure(state="normal", text_color=GOLD,
                                     border_color=GOLD_DIM)

        self._atualizar_escada()

    def _selecionar(self, idx):
        if self.confirmed or idx in self.hidden_opts:
            return
        self.selected_opt = idx
        for i, btn in enumerate(self.opt_buttons):
            if i in self.hidden_opts:
                continue
            btn.configure(
                fg_color="#2a1a00" if i == idx else BG_CARD,
                border_color=ORANGE_SEL if i == idx else BLUE_LIGHT,
                text_color=ORANGE_SEL if i == idx else TEXT_MAIN
            )
        self.btn_confirmar.configure(state="normal")

    def _confirmar(self):
        """
        Equivale ao bloco if/else de escolha() + def pontuação() do main.py
        """
        if self.selected_opt is None or self.confirmed:
            return
        self.confirmed = True
        self.btn_confirmar.configure(state="disabled")

        pergunta      = self.pergunta_atual
        correta       = pergunta['correta']              # ex: 'C'
        idx_correta   = ord(correta) - 65               # 'C' → 2
        idx_escolhida = self.selected_opt
        letra_escolhida = chr(65 + idx_escolhida)

        self.opt_buttons[idx_correta].configure(
            fg_color="#002810", border_color=GREEN_HIT, text_color=GREEN_HIT
        )
        if idx_escolhida != idx_correta:
            self.opt_buttons[idx_escolhida].configure(
                fg_color="#280000", border_color=RED_MISS, text_color=RED_MISS
            )
        for btn in self.opt_buttons:
            btn.configure(state="disabled")

        if letra_escolhida == correta:
            self.continua = True
            self.pontos  += 1
            self.lbl_pontos.configure(text=f"{self.pontos} pt(s)")
            self.lbl_status.configure(
                text=f"✔  Parabéns! Você acertou!  —  {self.pontos} ponto(s)",
                text_color=GREEN_HIT
            )
        else:
            self.continua = False
            resp_certa = pergunta['opcoes'][idx_correta]
            self.lbl_status.configure(
                text=f"✘  A resposta correta era: {correta}. {resp_certa}",
                text_color=RED_MISS
            )
            self.pontos = 0

        self.ranking[-1]["record"] = self.pontos
        nomes.salvar_ranking(self.ranking)
        self.q_index += 1

        if self.continua:
            self.after(1200, self._perguntar_continuar)
        else:
            self.after(1500, lambda: self._fim_de_jogo(vitoria=False))

    def _perguntar_continuar(self):
        """input('Deseja jogar novamente? (s/n)') do main.py"""
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Continuar?")
        dialogo.geometry("340x180")
        dialogo.configure(fg_color=BG_DARK)
        dialogo.grab_set()
        dialogo.resizable(False, False)

        ctk.CTkLabel(dialogo, text="Deseja continuar jogando?",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=TEXT_MAIN).pack(pady=(28, 6))
        ctk.CTkLabel(dialogo,
                     text=f"Pontuação atual: {self.pontos} pt(s)",
                     font=ctk.CTkFont(size=13),
                     text_color=GOLD).pack(pady=(0, 20))

        btns = ctk.CTkFrame(dialogo, fg_color="transparent")
        btns.pack()

        def sim():
            dialogo.destroy()
            self._escolha()

        def nao():
            dialogo.destroy()
            self._fim_de_jogo(vitoria=False)

        ctk.CTkButton(btns, text="Sim, continuar", width=140, height=40,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color=BLUE_MID, hover_color=BLUE_LIGHT,
                      text_color=TEXT_MAIN, corner_radius=8,
                      command=sim).pack(side="left", padx=6)

        ctk.CTkButton(btns, text="Não, sair", width=140, height=40,
                      font=ctk.CTkFont(size=13),
                      fg_color="transparent", hover_color=BG_CARD,
                      border_color=RED_MISS, border_width=1,
                      text_color=RED_MISS, corner_radius=8,
                      command=nao).pack(side="left", padx=6)

    def _ajuda_50(self):
        """50/50: elimina 2 das 4 opções erradas (sobram 3 visíveis + correta)"""
        if self.help50_used or self.confirmed:
            return
        self.help50_used = True
        self.btn_50.configure(state="disabled", text_color=TEXT_MUTED,
                               border_color="#333")

        correta = ord(self.pergunta_atual['correta']) - 65
        erradas = [i for i in range(5) if i != correta]
        esconder = random.sample(erradas, 2)

        for i in esconder:
            self.opt_buttons[i].configure(
                state="disabled", text_color="#222",
                border_color="#1a1a2a", fg_color=BG_DARK
            )
            self.hidden_opts.append(i)
            if self.selected_opt == i:
                self.selected_opt = None
                self.btn_confirmar.configure(state="disabled")

    def _ajuda_pular(self):
        if self.helpskip_used or self.confirmed:
            return
        self.helpskip_used = True
        self.btn_pular.configure(state="disabled", text_color=TEXT_MUTED,
                                  border_color="#333")
        self.q_index += 1
        self._escolha()

    def _fim_de_jogo(self, vitoria):
        self._limpar()
        nick   = self.ranking[-1]['nickname']
        pontos = self.ranking[-1]['record']

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        emoji  = "🏆" if vitoria else "💔"
        titulo = "VOCÊ GANHOU!" if vitoria else "FIM DE JOGO!"
        cor    = GOLD if vitoria else RED_MISS

        ctk.CTkLabel(frame, text=emoji,
                     font=ctk.CTkFont(size=52)).pack(pady=(0, 4))
        ctk.CTkLabel(frame, text=titulo,
                     font=ctk.CTkFont(size=32, weight="bold"),
                     text_color=cor).pack(pady=(0, 6))
        ctk.CTkLabel(frame,
                     text=f"{nick} — {pontos} ponto(s) garantido(s).",
                     font=ctk.CTkFont(size=15),
                     text_color=TEXT_MUTED).pack(pady=(0, 28))

        ctk.CTkButton(frame, text="JOGAR NOVAMENTE", width=280, height=48,
                      font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=BLUE_MID, hover_color=BLUE_LIGHT,
                      text_color=TEXT_MAIN, corner_radius=10,
                      command=self._reiniciar).pack(pady=(0, 10))

        ctk.CTkButton(frame, text="Ver Ranking", width=280, height=40,
                      font=ctk.CTkFont(size=13),
                      fg_color="transparent", hover_color=BG_CARD,
                      border_color=TEXT_MUTED, border_width=1,
                      text_color=TEXT_MUTED, corner_radius=8,
                      command=self._rank).pack()

    def _reiniciar(self):
        import importlib
        importlib.reload(perguntas_150)
        self._tela_nome()

    def _rank(self):
        """def rank() do main.py em janela popup"""
        win = ctk.CTkToplevel(self)
        win.title("Ranking")
        win.geometry("400x500")
        win.configure(fg_color=BG_DARK)
        win.grab_set()

        ctk.CTkLabel(win, text="🏆  RANKING",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=GOLD).pack(pady=(24, 14))

        scroll = ctk.CTkScrollableFrame(
            win, fg_color=BG_CARD, corner_radius=10,
            border_width=1, border_color=BLUE_LIGHT
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        ranking_ordenado = sorted(
            self.ranking, key=lambda x: x['record'], reverse=True
        )

        if not ranking_ordenado:
            ctk.CTkLabel(scroll, text="Nenhum jogo registrado ainda.",
                         font=ctk.CTkFont(size=13),
                         text_color=TEXT_MUTED).pack(pady=20)
        else:
            medals = ["🥇", "🥈", "🥉"]
            for i, jogador in enumerate(ranking_ordenado):
                row = ctk.CTkFrame(scroll, fg_color=BG_DARK, corner_radius=8,
                                   border_width=1, border_color="#1a2a50")
                row.pack(fill="x", padx=8, pady=4)
                row.columnconfigure(1, weight=1)

                pos = medals[i] if i < 3 else f"#{i+1}"
                ctk.CTkLabel(row, text=pos,
                             font=ctk.CTkFont(size=16),
                             width=36).grid(row=0, column=0, padx=8, pady=10)
                ctk.CTkLabel(row, text=jogador['nickname'],
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=TEXT_MAIN,
                             anchor="w").grid(row=0, column=1, sticky="w", padx=4)
                ctk.CTkLabel(row, text=f"{jogador['record']} pontos",
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=SAFE_COLOR
                             ).grid(row=0, column=2, padx=12)

        ctk.CTkButton(win, text="Fechar", width=160, height=38,
                      font=ctk.CTkFont(size=13),
                      fg_color=BLUE_MID, hover_color=BLUE_LIGHT,
                      text_color=TEXT_MAIN, corner_radius=8,
                      command=win.destroy).pack(pady=(0, 20))

    def _atualizar_escada(self):
        for (idx, lbl) in self.prize_labels:
            if idx == self.q_index:
                lbl.configure(
                    text=f"▶  {idx+1:02d}  {PRIZES[idx]}",
                    text_color=GOLD,
                    font=ctk.CTkFont(size=12, weight="bold")
                )
            elif idx < self.q_index:
                lbl.configure(
                    text=f"✓  {idx+1:02d}  {PRIZES[idx]}",
                    text_color="#334",
                    font=ctk.CTkFont(size=11)
                )
            else:
                lbl.configure(
                    text=f"    {idx+1:02d}  {PRIZES[idx]}",
                    text_color=SAFE_COLOR if idx in SAFE_LEVELS else TEXT_MUTED,
                    font=ctk.CTkFont(size=11)
                )

    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
