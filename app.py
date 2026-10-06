from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

app.secret_key = "TWAGAGASAA"

class Banco:
    def __init__(self, banco):
        self.banco = banco
    def entrarBanco(self):
        self.conn = sqlite3.connect(self.banco)
        cursor = self.conn.cursor()
        return cursor
    def fecharSalvarBanco(self):
        self.conn.commit()
        self.conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not "@" in email:
            return render_template("login.html")

        banco = Banco("bancodados.db")
        cursor = banco.entrarBanco()

        cursor.execute("""
            SELECT * FROM usuarios WHERE email = ?
        """, (email,))

        resultado = cursor.fetchone()

        if resultado and check_password_hash(resultado[3], password):
            session["ID"] = resultado[0]
            banco.fecharSalvarBanco()
            return redirect(url_for("main"))
        banco.fecharSalvarBanco()
        return render_template("login.html", error="Email ou senha Incorreta")

    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        confirm_password = request.form.get("confirm_password")

        if not email or not password or not name or not confirm_password:
            return render_template("register.html", error="OS ESPAÇOS NÃO PODEM ESTAR VAZIOS")

        if len(password) < 6 or not "@" in email:
            return render_template("register.html")


        if password != confirm_password:
            return render_template("register.html", error="A SENHA NÃO ESTÁ IGUAL!")
        
        banco = Banco("bancodados.db")
        cursor = banco.entrarBanco()

        cursor.execute("""
            SELECT * FROM usuarios WHERE email = ?
""", (email,))

        email_clone = cursor.fetchone()

        if email_clone:
            banco.fecharSalvarBanco()
            return render_template("register.html", error="Email ja em uso!")

        hash_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)
        """, (name, email, hash_password))

        banco.fecharSalvarBanco()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/main")
def main():
    if not "ID" in session:
        return redirect(url_for("login"))

    banco = Banco("bancodados.db")
    cursor = banco.entrarBanco()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (session["ID"],))

    usuario = cursor.fetchone()

    nome = usuario[1].split(" ")

    return render_template("main.html", nome=nome[0])

@app.route("/main/materias")
def materias():
    if not "ID" in session:
        return redirect(url_for("login"))

    return render_template("materias.html")

@app.route("/main/perfil", methods=["GET", "POST"])
def perfil():
    if not "ID" in session:
        return redirect(url_for("login"))

    banco = Banco("bancodados.db")
    cursor = banco.entrarBanco()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (session["ID"],))

    usuario = cursor.fetchone()

    email = usuario[2]
    nome = usuario[1].split(" ")
    nomeCompleto = usuario[1]

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        cursor.execute("SELECT * FROM usuarios WHERE email != ?", (email,))

        email_Dupe = cursor.fetchone()

        if email_Dupe:
            return render_template("perfil.html", error="Email duplicado", nome=nome[0], email=email, nomeCompleto=nomeCompleto)

        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (name, session["ID"]))
        cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (email, session["ID"]))  
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (session["ID"],))

        usuario = cursor.fetchone()

        email = usuario[2]
        nome = usuario[1].split(" ")
        nomeCompleto = usuario[1]

        banco.fecharSalvarBanco()

        return render_template("perfil.html", nome=nome[0], email=email, nomeCompleto=nomeCompleto)


    return render_template("perfil.html", nome=nome[0], email=email, nomeCompleto=nomeCompleto)

@app.route("/main/progresso")
def progresso():
    if not "ID" in session:
        return redirect(url_for("login"))

    return render_template("progresso.html")

@app.route("/main/ia")
def ia():
    if not "ID" in session:
        return redirect(url_for("login"))

    return render_template("ia.html")

@app.route("/main/simulados")
def simulados():
    if not "ID" in session:
        return redirect(url_for("login"))

    return render_template("simulados.html")

@app.route("/main/logout")
def logout():
    session.pop("ID")
    return redirect(url_for("login"))

@app.route("/main/exercicios")
def exercicios():
    if "ID" not in session:
        return redirect(url_for("login"))

    lista_exercicios = [
    {
        "materia": "Matemática",
        "pergunta": "Quanto é 8 × 7?",
        "resposta": "56",
    },
    {
        "materia": "Matemática",
        "pergunta": "Quanto é 144 ÷ 12?",
        "resposta": "12",
    },
    {
        "materia": "Matemática",
        "pergunta": "Qual é a raiz quadrada de 81?",
        "resposta": "9",
    },
    {
        "materia": "Matemática",
        "pergunta": "Quanto é 15% de 200?",
        "resposta": "30",
    },
    {
        "materia": "Matemática",
        "pergunta": "Qual é a área de um quadrado com lado de 5 cm?",
        "resposta": "25 cm²",
    },

    {
        "materia": "Biologia",
        "pergunta": "Qual organela participa da produção de energia?",
        "resposta": "Mitocôndria",
    },
    {
        "materia": "Biologia",
        "pergunta": "Qual é a molécula responsável por armazenar informações genéticas?",
        "resposta": "DNA",
    },
    {
        "materia": "Biologia",
        "pergunta": "Qual órgão é responsável por bombear o sangue?",
        "resposta": "Coração",
    },
    {
        "materia": "Biologia",
        "pergunta": "Qual é a unidade básica dos seres vivos?",
        "resposta": "Célula",
    },
    {
        "materia": "Biologia",
        "pergunta": "Qual sistema é responsável pela respiração?",
        "resposta": "Sistema respiratório",
    },

    {
        "materia": "História",
        "pergunta": "Em que ano ocorreu a Independência do Brasil?",
        "resposta": "1822",
    },
    {
        "materia": "História",
        "pergunta": "Quem proclamou a Independência do Brasil?",
        "resposta": "Dom Pedro I",
    },
    {
        "materia": "História",
        "pergunta": "Em que ano começou a Segunda Guerra Mundial?",
        "resposta": "1939",
    },
    {
        "materia": "História",
        "pergunta": "Qual civilização construiu as pirâmides de Gizé?",
        "resposta": "Egípcia",
    },
    {
        "materia": "História",
        "pergunta": "Quem foi o primeiro presidente do Brasil?",
        "resposta": "Deodoro da Fonseca",
    },

    {
        "materia": "Geografia",
        "pergunta": "Qual é o maior país da América do Sul?",
        "resposta": "Brasil",
    },
    {
        "materia": "Geografia",
        "pergunta": "Qual é o maior oceano do planeta?",
        "resposta": "Oceano Pacífico",
    },
    {
        "materia": "Geografia",
        "pergunta": "Qual é a capital do Brasil?",
        "resposta": "Brasília",
    },
    {
        "materia": "Geografia",
        "pergunta": "Em qual continente fica o Egito?",
        "resposta": "África",
    },
    {
        "materia": "Geografia",
        "pergunta": "Qual é o maior bioma brasileiro?",
        "resposta": "Amazônia",
    },

    {
        "materia": "Português",
        "pergunta": "Qual é o plural de 'cidadão'?",
        "resposta": "Cidadãos",
    },
    {
        "materia": "Português",
        "pergunta": "Qual é o antônimo de 'rápido'?",
        "resposta": "Lento",
    },
    {
        "materia": "Português",
        "pergunta": "Qual é o sinônimo de 'feliz'?",
        "resposta": "Alegre",
    },
    {
        "materia": "Português",
        "pergunta": "Qual é a classe gramatical da palavra 'rapidamente'?",
        "resposta": "Advérbio",
    },
    {
        "materia": "Português",
        "pergunta": "Qual é o verbo na frase 'João estudou para a prova'?",
        "resposta": "Estudou",
    },

    {
        "materia": "Física",
        "pergunta": "Qual é a unidade de medida da força no SI?",
        "resposta": "Newton",
    },
    {
        "materia": "Física",
        "pergunta": "Qual é a velocidade da luz aproximadamente?",
        "resposta": "300.000 km/s",
    },
    {
        "materia": "Física",
        "pergunta": "Qual força atrai os objetos em direção à Terra?",
        "resposta": "Gravidade",
    },
    {
        "materia": "Física",
        "pergunta": "Qual é a unidade de medida da energia?",
        "resposta": "Joule",
    },
    {
        "materia": "Física",
        "pergunta": "Qual instrumento mede a temperatura?",
        "resposta": "Termômetro",
    },

    {
        "materia": "Química",
        "pergunta": "Qual é o símbolo químico do oxigênio?",
        "resposta": "O",
    },
    {
        "materia": "Química",
        "pergunta": "Qual é a fórmula química da água?",
        "resposta": "H₂O",
    },
    {
        "materia": "Química",
        "pergunta": "Qual é o símbolo químico do ouro?",
        "resposta": "Au",
    },
    {
        "materia": "Química",
        "pergunta": "Qual é o número atômico do hidrogênio?",
        "resposta": "1",
    },
    {
        "materia": "Química",
        "pergunta": "Qual é o pH de uma substância neutra?",
        "resposta": "7",
    },

    {
        "materia": "Inglês",
        "pergunta": "O que significa 'Hello' em português?",
        "resposta": "Olá",
    },
    {
        "materia": "Inglês",
        "pergunta": "O que significa 'House' em português?",
        "resposta": "Casa",
    },
    {
        "materia": "Inglês",
        "pergunta": "Qual é o passado de 'go'?",
        "resposta": "Went",
    },
    {
        "materia": "Inglês",
        "pergunta": "O que significa 'Book' em português?",
        "resposta": "Livro",
    },
    {
        "materia": "Inglês",
        "pergunta": "Como se diz 'obrigado' em inglês?",
        "resposta": "Thank you",
    },
]

    return render_template(
        "exercicios.html",
        exercicios=lista_exercicios,
    )

if __name__ == "__main__":
    app.run(debug=True)
