import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem

class ListaDeTarefasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tarefas")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Descrição da Tarefa:")
        self.layout.addWidget(self.label)

        self.descricao_input = QLineEdit()
        self.layout.addWidget(self.descricao_input)

        self.adicionar_button = QPushButton("Adicionar Tarefa")
        self.adicionar_button.clicked.connect(self.adicionar_tarefa)
        self.layout.addWidget(self.adicionar_button)

        self.tarefas_list = QListWidget()
        self.layout.addWidget(self.tarefas_list)

        self.hbox = QHBoxLayout()
        self.layout.addLayout(self.hbox)

        self.label_id = QLabel("ID da Tarefa:")
        self.hbox.addWidget(self.label_id)

        self.entrada_id = QLineEdit()
        self.hbox.addWidget(self.entrada_id)

        self.botao_marcar_concluida = QPushButton("Marcar como Concluída")
        self.botao_marcar_concluida.clicked.connect(self.marcar_tarefa)
        self.hbox.addWidget(self.botao_marcar_concluida)

        self.botao_excluir = QPushButton("Excluir Tarefa")
        self.botao_excluir.clicked.connect(self.excluir_tarefa)
        self.hbox.addWidget(self.botao_excluir)

        self.carregar_tarefas()

    def carregar_tarefas(self):
        self.tarefas_list.clear()
        conn = sqlite3.connect("tarefas.db")
        c = conn.cursor()
        c.execute("SELECT * FROM tarefas")
        tarefas = c.fetchall()
        conn.close()
        for tarefa in tarefas:
            descricao = tarefa[1]
            concluida = tarefa[2]
            item = QListWidgetItem(f"{descricao} {'(Concluída)' if concluida else ''}")
            self.tarefas_list.addItem(item)

    def adicionar_tarefa(self):
        descricao = self.descricao_input.text()
        if descricao:
            conn = sqlite3.connect("tarefas.db")
            c = conn.cursor()
            c.execute("INSERT INTO tarefas (descricao, concluida) VALUES (?, 0)", (descricao,))
            conn.commit()
            conn.close()
            self.carregar_tarefas()
            self.descricao_input.clear()

    def marcar_tarefa(self):
        tarefa_id = self.entrada_id.text()
        if tarefa_id.isdigit():
            conn = sqlite3.connect("tarefas.db")
            c = conn.cursor()
            c.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (tarefa_id,))
            conn.commit()
            conn.close()
            self.carregar_tarefas()
            self.entrada_id.clear()

    def excluir_tarefa(self):
        tarefa_id = self.entrada_id.text()
        if tarefa_id.isdigit():
            conn = sqlite3.connect("tarefas.db")
            c = conn.cursor()
            c.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
            conn.commit()
            conn.close()
            self.carregar_tarefas()
            self.entrada_id.clear()

def criar_banco_de_dados():
    conn = sqlite3.connect("tarefas.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT, concluida INTEGER)''')
    conn.commit()
    conn.close()

def main():
    criar_banco_de_dados()
    app = QApplication(sys.argv)
    window = ListaDeTarefasApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
