# Trabalho Cris, Carla e Rafaela - Biblioteca Virtual
# Nome do sistema: Cosmos — Universo de Ideias
from funcoes import (
    iniciar_sistema,  # importa dados iniciais
    login_ou_cadastro, # função de login ou cadastro
    listar_generos, # listar gêneros disponíveis
    listar_livros_por_genero, # listar livros por gênero
    listar_meus_livros, # listar livros retirados pelo usuário
    retirar_livro_por_id, # função para retirar livro por ID
    devolver_antecipado, # função para devolução antecipada
    renovar_emprestimo, # função para renovação de empréstimo
    salvar_todos # função para salvar todos os dados
)

def main():
    livros, usuarios, emprestimos = iniciar_sistema()

    usuario = login_ou_cadastro(usuarios)
    if not usuario:
        print("Encerrando o sistema.")
        return
    ra = usuario['ra']

    while True:
        print("\n===== Cosmos — Universo de Ideias =====")
        print("1. Biblioteca por gênero")
        print("2. Meus livros")
        print("3. Retirar livro")
        print("4. Devolução antecipada")
        print("5. Renovação online")
        print("6. Sair")

        try:
            opcao = int(input("Escolha uma opção: ").strip())
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 1:
            listar_generos()
            genero = input("Escolha o gênero (ou ENTER para ver todos): ").strip()
            listar_livros_por_genero(livros, genero)
            # Quando ele Lista, da a opção de voltar ao menu ou retirar livro.
            escolha = input("Digite o ID do livro para ver/retirar ou 0 para voltar: ").strip()
            if escolha == '0' or escolha == '':
                continue
            else:
                retirar_livro_por_id(livros, usuarios, emprestimos, ra, escolha)
                salvar_todos(livros, usuarios, emprestimos)
        elif opcao == 2:
            listar_meus_livros(livros, ra)
        elif opcao == 3:
            # Opção mais direta para retirar livro, mostrando todos os livros.
            listar_livros_por_genero(livros, "")
            book_id = input("Digite o ID do livro que deseja retirar (ou 0 para voltar): ").strip()
            if book_id == '0' or book_id == '':
                continue
            retirar_livro_por_id(livros, usuarios, emprestimos, ra, book_id)
            salvar_todos(livros, usuarios, emprestimos)
        elif opcao == 4:
            devolver_antecipado(livros, emprestimos, ra)
            salvar_todos(livros, usuarios, emprestimos)
        elif opcao == 5:
            renovar_emprestimo(emprestimos, ra)
            salvar_todos(livros, usuarios, emprestimos)
        elif opcao == 6:
            print("Saindo... Obrigado!")
            salvar_todos(livros, usuarios, emprestimos)
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()