import sqlite3
from pathlib import Path


class Livraria:
    """Camada de regras de negócio e acesso ao banco SQLite."""

    def __init__(self, caminho_banco=None):
        if caminho_banco is None:
            raiz = Path(__file__).resolve().parent.parent
            pasta = raiz / "database"
            pasta.mkdir(parents=True, exist_ok=True)
            caminho_banco = pasta / "livraria.db"
        self.conexao = sqlite3.connect(str(caminho_banco)
        )
        self.conexao.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        with self.conexao:
            self.conexao.executescript("""
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    telefone TEXT,
                    email TEXT
                );

                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    telefone TEXT,
                    email TEXT,
                    matricula TEXT NOT NULL UNIQUE,
                    cargo TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT NOT NULL UNIQUE,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    preco REAL NOT NULL CHECK (preco >= 0),
                    estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0)
                );

                CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    funcionario_id INTEGER NOT NULL,
                    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    total REAL NOT NULL CHECK (total >= 0),
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
                );

                CREATE TABLE IF NOT EXISTS itens_compra (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compra_id INTEGER NOT NULL,
                    livro_id INTEGER NOT NULL,
                    titulo_livro TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
                    FOREIGN KEY (compra_id) REFERENCES compras(id),
                    FOREIGN KEY (livro_id) REFERENCES livros(id)
                );
            """)

    @staticmethod
    def _validar_textos(*valores):
        if any(not str(valor).strip() for valor in valores):
            raise ValueError("Os campos obrigatórios precisam ser preenchidos.")

    def cadastrar_cliente(self, nome, cpf, telefone="", email=""):
        self._validar_textos(nome, cpf)
        try:
            with self.conexao:
                cursor = self.conexao.execute(
                    "INSERT INTO clientes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
                    (nome.strip(), cpf.strip(), telefone.strip(), email.strip())
                )
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError("Já existe um cliente com esse CPF.") from erro

    def cadastrar_funcionario(self, nome, cpf, telefone, email, matricula, cargo):
        self._validar_textos(nome, cpf, matricula, cargo)
        try:
            with self.conexao:
                cursor = self.conexao.execute(
                    """INSERT INTO funcionarios
                    (nome, cpf, telefone, email, matricula, cargo)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (nome.strip(), cpf.strip(), telefone.strip(), email.strip(),
                     matricula.strip(), cargo.strip())
                )
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError("CPF ou matrícula já cadastrado.") from erro

    def cadastrar_livro(self, isbn, titulo, autor, preco, estoque):
        self._validar_textos(isbn, titulo, autor)
        if float(preco) < 0 or int(estoque) < 0:
            raise ValueError("Preço e estoque não podem ser negativos.")
        try:
            with self.conexao:
                cursor = self.conexao.execute(
                    """INSERT INTO livros (isbn, titulo, autor, preco, estoque)
                    VALUES (?, ?, ?, ?, ?)""",
                    (isbn.strip(), titulo.strip(), autor.strip(), float(preco), int(estoque))
                )
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError("Já existe um livro com esse ISBN/código.") from erro

    def listar_clientes(self):
        return [dict(r) for r in self.conexao.execute(
            "SELECT * FROM clientes ORDER BY nome"
        ).fetchall()]

    def listar_funcionarios(self):
        return [dict(r) for r in self.conexao.execute(
            "SELECT * FROM funcionarios ORDER BY nome"
        ).fetchall()]

    def listar_livros(self):
        return [dict(r) for r in self.conexao.execute(
            "SELECT * FROM livros ORDER BY titulo"
        ).fetchall()]

    def buscar_livros(self, termo):
        termo = f"%{termo.strip()}%"
        return [dict(r) for r in self.conexao.execute(
            """SELECT * FROM livros
            WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ?
            ORDER BY titulo""", (termo, termo, termo)
        ).fetchall()]

    def registrar_compra(self, cliente_id, funcionario_id, itens):
        """Registra todos os itens e baixa o estoque em uma única transação."""
        if not itens:
            raise ValueError("A compra precisa ter pelo menos um item.")

        agregados = {}
        for livro_id, quantidade in itens:
            if int(quantidade) <= 0:
                raise ValueError("A quantidade precisa ser maior que zero.")
            agregados[int(livro_id)] = agregados.get(int(livro_id), 0) + int(quantidade)

        try:
            with self.conexao:
                cliente = self.conexao.execute(
                    "SELECT id FROM clientes WHERE id = ?", (int(cliente_id),)
                ).fetchone()
                funcionario = self.conexao.execute(
                    "SELECT id FROM funcionarios WHERE id = ?", (int(funcionario_id),)
                ).fetchone()
                if not cliente:
                    raise ValueError("Cliente não encontrado.")
                if not funcionario:
                    raise ValueError("Funcionário não encontrado.")

                itens_processados = []
                total = 0.0
                for livro_id, quantidade in agregados.items():
                    livro = self.conexao.execute(
                        "SELECT * FROM livros WHERE id = ?", (livro_id,)
                    ).fetchone()
                    if not livro:
                        raise ValueError(f"Livro de ID {livro_id} não encontrado.")
                    if livro["estoque"] < quantidade:
                        raise ValueError(
                            f"Estoque insuficiente para '{livro['titulo']}'. "
                            f"Disponível: {livro['estoque']}."
                        )
                    preco = float(livro["preco"])
                    subtotal = preco * quantidade
                    total += subtotal
                    itens_processados.append({
                        "livro_id": livro_id,
                        "titulo": livro["titulo"],
                        "quantidade": quantidade,
                        "preco_unitario": preco,
                        "subtotal": subtotal
                    })

                cursor = self.conexao.execute(
                    """INSERT INTO compras (cliente_id, funcionario_id, total)
                    VALUES (?, ?, ?)""",
                    (int(cliente_id), int(funcionario_id), round(total, 2))
                )
                compra_id = cursor.lastrowid

                for item in itens_processados:
                    self.conexao.execute(
                        """INSERT INTO itens_compra
                        (compra_id, livro_id, titulo_livro, quantidade, preco_unitario)
                        VALUES (?, ?, ?, ?, ?)""",
                        (compra_id, item["livro_id"], item["titulo"],
                         item["quantidade"], item["preco_unitario"])
                    )
                    self.conexao.execute(
                        "UPDATE livros SET estoque = estoque - ? WHERE id = ?",
                        (item["quantidade"], item["livro_id"])
                    )

            return compra_id, round(total, 2)
        except sqlite3.IntegrityError as erro:
            raise ValueError("Não foi possível registrar a compra. Verifique os dados.") from erro

    def historico_cliente(self, cliente_id):
        cliente = self.conexao.execute(
            "SELECT id FROM clientes WHERE id = ?", (int(cliente_id),)
        ).fetchone()
        if not cliente:
            raise ValueError("Cliente não encontrado.")

        compras = self.conexao.execute(
            """SELECT c.id, c.data, c.total, f.nome AS funcionario
            FROM compras c
            JOIN funcionarios f ON f.id = c.funcionario_id
            WHERE c.cliente_id = ?
            ORDER BY c.id DESC""", (int(cliente_id),)
        ).fetchall()

        resultado = []
        for compra in compras:
            dados = dict(compra)
            dados["itens"] = [
                dict(item) for item in self.conexao.execute(
                    """SELECT titulo_livro AS titulo, quantidade, preco_unitario,
                    quantidade * preco_unitario AS subtotal
                    FROM itens_compra WHERE compra_id = ? ORDER BY id""",
                    (compra["id"],)
                ).fetchall()
            ]
            resultado.append(dados)
        return resultado

    def fechar(self):
        self.conexao.close()
