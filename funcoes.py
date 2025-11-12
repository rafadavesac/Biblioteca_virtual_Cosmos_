# Função Cosmos 
import os, csv
from datetime import datetime, timedelta

BASE_DIR = os.path.join(os.path.dirname(__file__), "dados")
LIVROS_CSV = os.path.join(BASE_DIR, "livros.csv")
USUARIOS_CSV = os.path.join(BASE_DIR, "usuarios.csv")
EMPR_CSV = os.path.join(BASE_DIR, "emprestimos.csv")
LOG_TXT = os.path.join(BASE_DIR, "log.txt")
DATE_FMT = "%d/%m/%Y"

GENERO_LIST = ["Romance", "Fantasia", "Terror"]
MAX_POR_USUARIO = 2  # limite de livros por usuário

def garantir_arquivos():
    os.makedirs(BASE_DIR, exist_ok=True)
    if not os.path.exists(LIVROS_CSV):
        with open(LIVROS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id","titulo","autor","genero","status","due_date","borrower_ra"])
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ra","nome","senha"])
    if not os.path.exists(EMPR_CSV):
        with open(EMPR_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["loan_id","book_id","ra","loan_date","due_date","returned"])
    if not os.path.exists(LOG_TXT):
        open(LOG_TXT, "a", encoding="utf-8").close()

def iniciar_sistema():
    garantir_arquivos()
    livros=[]; usuarios=[]; emprestimos=[]
    try:
        with open(LIVROS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader: livros.append(r)
    except Exception as e:
        print("Erro ao ler livros:", e)
    try:
        with open(USUARIOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader: usuarios.append(r)
    except Exception as e:
        print("Erro ao ler usuarios:", e)
    try:
        with open(EMPR_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader: emprestimos.append(r)
    except Exception as e:
        print("Erro ao ler emprestimos:", e)
    return livros, usuarios, emprestimos

def salvar_todos(livros, usuarios, emprestimos):
    try:
        with open(LIVROS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id","titulo","autor","genero","status","due_date","borrower_ra"])
            writer.writeheader(); writer.writerows(livros)
    except Exception as e:
        print("Erro ao salvar livros:", e)
    try:
        with open(USUARIOS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["ra","nome","senha"])
            writer.writeheader(); writer.writerows(usuarios)
    except Exception as e:
        print("Erro ao salvar usuarios:", e)
    try:
        with open(EMPR_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["loan_id","book_id","ra","loan_date","due_date","returned"])
            writer.writeheader(); writer.writerows(emprestimos)
    except Exception as e:
        print("Erro ao salvar emprestimos:", e)

def registrar_log(txt):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open(LOG_TXT, "a", encoding="utf-8") as f:
            f.write(f"[{now}] {txt}\n")
    except Exception:
        pass

def login_ou_cadastro(usuarios):
    print("\nBem-vindo ao Cosmos! Faça login ou cadastre-se.")
    # carregar usuarios existentes na lista passada
    while True:
        opc = input("Digite 'l' para login, 'c' para cadastrar, ou 's' para sair: ").strip().lower()
        if opc == 's':
            return None
        if opc == 'c':
            ra = input("RA (apenas números): ").strip()
            if any(u['ra']==ra for u in usuarios):
                print("RA já cadastrado. Use outro RA.")
                continue
            nome = input("Nome completo: ").strip()
            senha = input("Senha (visível): ").strip()
            usuarios.append({'ra':ra,'nome':nome,'senha':senha})
            salvar_todos([], usuarios, [])  # salva só usuarios
            registrar_log(f"Cadastro: {nome} (RA {ra})")
            print("Cadastro realizado! Faça login agora.")
            continue
        if opc == 'l':
            ra = input("RA: ").strip(); senha = input("Senha: ").strip()
            user = next((u for u in usuarios if u['ra']==ra and u['senha']==senha), None)
            if user:
                registrar_log(f"Login: RA {ra}")
                print(f"Bem-vindo, {user['nome']}!")
                return user
            else:
                print("RA ou senha incorretos. Tente novamente ou cadastre-se.")
                continue
        print("Opção inválida. Digite 'l', 'c' ou 's'.")

def listar_generos():
    print("\nGêneros disponíveis:")
    for g in GENERO_LIST: print("-", g)

def listar_livros_por_genero(livros, genero):
    if genero.strip() == "":
        disponiveis = [l for l in livros if l.get('status','') != 'emprestado']
        print("\nLivros disponíveis:")
        for l in disponiveis:
            print(f"ID:{l['id']} - {l['titulo']} — {l['autor']} ({l['genero']})")
        return
    genero = genero.capitalize()
    encontrados = [l for l in livros if l.get('genero','').lower() == genero.lower()]
    print(f"\nLivros no gênero {genero}:")
    ok = False
    for l in encontrados:
        if l.get('status','') != 'emprestado':
            print(f"ID:{l['id']} - {l['titulo']} — {l['autor']}"); ok = True
    if not ok: print("Nenhum livro disponível neste gênero.")

def contar_emprestimos_do_usuario(emprestimos, ra):
    return sum(1 for e in emprestimos if e.get('ra')==ra and e.get('returned')=='no')

def retirar_livro_por_id(livros, usuarios, emprestimos, ra, book_id):
    # checar limite
    qtd = contar_emprestimos_do_usuario(emprestimos, ra)
    if qtd >= MAX_POR_USUARIO:
        print(f"Você já atingiu o limite de {MAX_POR_USUARIO} livros emprestados.")
        return
    for l in livros:
        if l['id'] == book_id:
            if l.get('status') == 'emprestado':
                print("Livro já emprestado.")
                return
            # efetivar empréstimo
            l['status'] = 'emprestado'
            l['borrower_ra'] = ra
            due = datetime.now() + timedelta(days=7)
            l['due_date'] = due.strftime(DATE_FMT)
            loan_id = str(len(emprestimos) + 1)
            emprestimos.append({'loan_id':loan_id,'book_id':book_id,'ra':ra,'loan_date':datetime.now().strftime(DATE_FMT),'due_date':l['due_date'],'returned':'no'})
            registrar_log(f"Empréstimo: livro {l['titulo']} (ID {book_id}) para RA {ra}")
            print(f"Empréstimo realizado! Devolva até {l['due_date']}")
            # avisar se chegou ao limite agora
            qtd2 = contar_emprestimos_do_usuario(emprestimos, ra)
            if qtd2 >= MAX_POR_USUARIO:
                print(f"Atenção: você atingiu o limite de {MAX_POR_USUARIO} livros emprestados.")
            return
    print("Livro não encontrado.")

def devolver_antecipado(livros, emprestimos, ra):
    listar_meus_livros(livros, ra)
    book_id = input("Digite o ID do livro que vai devolver (ou 0 para voltar): ").strip()
    if book_id == '0' or book_id == '':
        return
    for l in livros:
        if l['id'] == book_id and l.get('borrower_ra')==ra and l.get('status')=='emprestado':
            l['status'] = 'disponivel'; l['borrower_ra'] = ''; l['due_date'] = ''
            for e in emprestimos:
                if e['book_id'] == book_id and e['ra']==ra and e.get('returned')=='no':
                    e['returned'] = 'yes'; registrar_log(f"Devolução: livro {l['titulo']} (ID {book_id}) por RA {ra}")
                    print("Livro devolvido com sucesso!")
                    return
    print("Empréstimo não encontrado para esse RA e livro.")

def renovar_emprestimo(emprestimos, ra):
    ativos = [e for e in emprestimos if e.get('ra')==ra and e.get('returned')=='no']
    if not ativos:
        print("Você não tem empréstimos para renovar."); return
    for e in ativos:
        print(f"Loan ID:{e['loan_id']} - Livro ID:{e['book_id']} - Vence em {e['due_date']}")
    loan_id = input("Digite o Loan ID que deseja renovar (ou 0 para voltar): ").strip()
    if loan_id == '0' or loan_id == '':
        return
    for e in emprestimos:
        if e['loan_id']==loan_id and e['ra']==ra and e.get('returned')=='no':
            try:
                due = datetime.strptime(e['due_date'], DATE_FMT)
            except Exception:
                print("Data inválida no registro."); return
            novo = due + timedelta(days=7); e['due_date'] = novo.strftime(DATE_FMT)
            # atualizar também em livros
            registrar_log(f"Renovação: loan {loan_id} por RA {ra} até {e['due_date']}")
            print(f"Renovado até {e['due_date']}"); return
    print("Empréstimo não encontrado.")

def listar_meus_livros(livros, ra):
    print(f"\nSeus livros (RA {ra}):")
    meus = [l for l in livros if l.get('borrower_ra')==ra and l.get('status')=='emprestado']
    if meus:
        for l in meus:
            print(f"ID:{l['id']} - {l['titulo']} — devolve até {l.get('due_date','-')}")
    else:
        print("Você não tem livros emprestados.")