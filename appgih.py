import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import vlc
import validators
import json
import os

class LiveStreamPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Transmissão ao Vivo")
        self.streams = []
        self.config_file = "config.json"

        self.load_config()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.add_button = tk.Button(self.frame, text="Adicionar URL", command=self.add_stream)
        self.add_button.grid(row=0, column=0, padx=5)

        self.save_button = tk.Button(self.frame, text="Salvar Lista", command=self.save_playlist)
        self.save_button.grid(row=0, column=1, padx=5)

        self.load_button = tk.Button(self.frame, text="Carregar Lista", command=self.load_playlist)
        self.load_button.grid(row=0, column=2, padx=5)

        self.stream_listbox = tk.Listbox(root, width=50, height=10)
        self.stream_listbox.pack(pady=10)
        self.stream_listbox.bind('<Double-1>', self.play_stream)

        self.remove_button = tk.Button(self.frame, text="Remover URL", command=self.remove_stream)
        self.remove_button.grid(row=1, column=0, padx=5)

        self.edit_button = tk.Button(self.frame, text="Editar URL", command=self.edit_stream)
        self.edit_button.grid(row=1, column=1, padx=5)

        self.sort_button = tk.Button(self.frame, text="Ordenar URLS", command=self.sort_streams)
        self.sort_button.grid(row=1, column=2, padx=5)

        self.player = None

        # Adicionando os novos módulos
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.menu_bar.add_command(label="Quem Somos Nós", command=self.quem_somos)
        self.menu_bar.add_command(label="Fale Conosco", command=self.fale_conosco)
        self.menu_bar.add_command(label="Página Web", command=self.pagina_web)
        self.menu_bar.add_command(label="Chat", command=self.chat)
        self.menu_bar.add_command(label="Ajuda e Suporte", command=self.ajuda_suporte)

        # Tema Escuro
        self.dark_mode = tk.BooleanVar(value=False)
        self.menu_bar.add_checkbutton(label="Tema Escuro", onvalue=True, offvalue=False, variable=self.dark_mode, command=self.toggle_theme)

    def add_stream(self):
        url = simpledialog.askstring("Adicionar URL", "Digite a URL da transmissão:")
        if url and validators.url(url):
            cover = filedialog.askopenfilename(title="Selecione a capa", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
            if cover:
                self.streams.append((url, cover))
                self.stream_listbox.insert(tk.END, f"URL: {url} | Capa: {cover}")
        else:
            messagebox.showerror("Erro", "URL inválida. Por favor, insira uma URL válida.")

    def save_playlist(self):
        if not self.streams:
            messagebox.showwarning("Aviso", "Nenhuma URL adicionada!")
            return

        playlist_name = filedialog.asksaveasfilename(defaultextension=".m3u", filetypes=[("M3U Playlist", "*.m3u")])
        if playlist_name:
            with open(playlist_name, 'w') as f:
                for url, cover in self.streams:
                    f.write(f"#EXTINF:-1, cover={cover}\n{url}\n")
            messagebox.showinfo("Sucesso", "Lista salva com sucesso!")
            self.save_config()

    def load_playlist(self):
        playlist_name = filedialog.askopenfilename(filetypes=[("M3U Playlist", "*.m3u")])
        if playlist_name:
            with open(playlist_name, 'r') as f:
                self.streams = []
                self.stream_listbox.delete(0, tk.END)
                lines = f.readlines()
                for i in range(0, len(lines), 2):
                    cover = lines[i].split("cover=")[-1].strip()
                    url = lines[i+1].strip()
                    self.streams.append((url, cover))
                    self.stream_listbox.insert(tk.END, f"URL: {url} | Capa: {cover}")
            messagebox.showinfo("Sucesso", "Lista carregada com sucesso!")

    def play_stream(self, event):
        selection = self.stream_listbox.curselection()
        if selection:
            index = selection[0]
            url, cover = self.streams[index]
            if self.player:
                self.player.stop()
            instance = vlc.Instance()
            self.player = instance.media_player_new()
            media = instance.media_new(url)
            self.player.set_media(media)
            self.player.play()
            messagebox.showinfo("Reproduzindo", f"Reproduzindo stream: {url}")

    def stop_stream(self):
        if self.player:
            self.player.stop()
            messagebox.showinfo("Parado", "Transmissão parada.")

    def remove_stream(self):
        selection = self.stream_listbox.curselection()
        if selection:
            index = selection[0]
            self.stream_listbox.delete(index)
            del self.streams[index]
            messagebox.showinfo("Removido", "URL removida com sucesso!")

    def edit_stream(self):
        selection = self.stream_listbox.curselection()
        if selection:
            index = selection[0]
            url, cover = self.streams[index]
            new_url = simpledialog.askstring("Editar URL", "Digite a nova URL da transmissão:", initialvalue=url)
            if new_url and validators.url(new_url):
                new_cover = filedialog.askopenfilename(title="Selecione a nova capa", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")], initialdir=os.path.dirname(cover))
                if new_cover:
                    self.streams[index] = (new_url, new_cover)
                    self.stream_listbox.delete(index)
                    self.stream_listbox.insert(index, f"URL: {new_url} | Capa: {new_cover}")
                    messagebox.showinfo("Editado", "URL editada com sucesso!")
            else:
                messagebox.showerror("Erro", "URL inválida. Por favor, insira uma URL válida.")

    def sort_streams(self):
        self.streams.sort(key=lambda x: x[0])
        self.stream_listbox.delete(0, tk.END)
        for url, cover in self.streams:
            self.stream_listbox.insert(tk.END, f"URL: {url} | Capa: {cover}")
        messagebox.showinfo("Ordenado", "URLs ordenadas com sucesso!")

    def quem_somos(self):
        messagebox.showinfo("Quem Somos Nós", " olá , me chamo Giovani Santos ; sou o fundador desta plataforma, fico muito feliz por está aqui. ")

    def fale_conosco(self):
        messagebox.showinfo("Fale Conosco", "Informações de contato...")

    def pagina_web(self):
        messagebox.showinfo("Página Web", "Informações sobre a página web...")

    def chat(self):
        messagebox.showinfo("Chat", "Funcionalidade de chat...")

    def ajuda_suporte(self):
        messagebox.showinfo("Ajuda e Suporte", "Seção de ajuda e suporte...")

    def toggle_theme(self):
        if self.dark_mode.get():
            self.root.configure(bg="#2e2e2e")
            self.frame.configure(bg="#2e2e2e")
            self.stream_listbox.configure(bg="#3e3e3e", fg="white")
        else:
            self.root.configure(bg="#f0f0f0")
            self.frame.configure(bg="#f0f0f0")
            self.stream_listbox.configure(bg="white", fg="black")

    def save_config(self):
        config = {
            "streams": self.streams,
            "dark_mode": self.dark_mode.get()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.streams = config.get("streams", [])
                self.dark_mode.set(config.get("dark_mode", False))
                for url, cover in self.streams:
                    self.stream_listbox.insert(tk.END, f"URL: {url} | Capa: {cover}")
                self.toggle_theme()

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveStreamPanel(root)
    root.mainloop()
