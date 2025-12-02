# RPG com nível, classes, inventário e mapa (corrigido e compatível com ambientes não interativos)

import random
import sys

# --- Configurações para execução não interativa ---
# Se o ambiente não suportar input(), o jogo usará valores padrão para executar sem travar.
DEFAULT_PLAYER_NAME = "Jogador"
DEFAULT_CLASS_CHOICE = "1"  # 1=guerreiro, 2=mago, 3=arqueiro
NON_INTERACTIVE_ACTION = "1"  # ação padrão durante batalhas (1 = atacar)
NON_INTERACTIVE_CONTINUE = "n"  # não continuar por padrão

# --- Classes de Personagem ---
classes = {
    "guerreiro": {"hp": 40, "attack": (5, 9)},
    "mago": {"hp": 25, "attack": (7, 12)},
    "arqueiro": {"hp": 30, "attack": (4, 10)}
}

# --- Jogador ---
player = {
    "name": "",
    "class": "",
    "hp": 0,
    "attack": (0, 0),
    "level": 1,
    "xp": 0,
    "xp_next": 20,
    "inventory": []
}

# --- Inimigos ---
enemies = [
    {"name": "Goblin", "hp": 12, "attack": (2, 5), "xp": 10},
    {"name": "Lobo", "hp": 15, "attack": (3, 6), "xp": 14},
    {"name": "Esqueleto", "hp": 18, "attack": (4, 7), "xp": 18}
]

# --- Itens ---
itens_disponiveis = ["Poção de Cura", "Flechas", "Grimório Antigo", "Escudo Pequeno"]

# --- Mapa Simples ---
mapa = [
    "Floresta Misteriosa",
    "Caverna Sombria",
    "Vilarejo Abandonado",
    "Montanha Congelada"
]

# --- Função de entrada compatível ---
def get_input(prompt: str, default: str = "") -> str:
    """Tenta usar input(); se não for possível (sandbox), retorna o valor padrão.

    Também imprime o prompt e a escolha utilizada para que o usuário veja o fluxo.
    """
    try:
        return input(prompt)
    except (EOFError, OSError):
        # Ambiente não interativo – usar valor padrão
        if default is None:
            default = ""
        print(f"{prompt}{default} (padrão usado)")
        return default


def safe_print(msg: str):
    """Print seguro: evita problemas se stdout estiver parcialmente restrito."""
    try:
        print(msg)
    except (OSError, IOError):
        # Em ambientes muito restritos, simplesmente ignore falha de print
        pass


# --- Inicialização do jogador ---
safe_print("Bem-vindo ao RPG Avançado!")
player_name = get_input("Digite o nome do seu personagem: ", DEFAULT_PLAYER_NAME).strip()
if player_name == "":
    player_name = DEFAULT_PLAYER_NAME
player["name"] = player_name

safe_print("\nEscolha uma classe:")
safe_print("1 - Guerreiro | 2 - Mago | 3 - Arqueiro")
class_choice = get_input("> ", DEFAULT_CLASS_CHOICE).strip()
if class_choice not in ("1", "2", "3"):
    class_choice = DEFAULT_CLASS_CHOICE

if class_choice == "1":
    classe = "guerreiro"
elif class_choice == "2":
    classe = "mago"
else:
    classe = "arqueiro"

player["class"] = classe
player["hp"] = classes[classe]["hp"]
player["attack"] = classes[classe]["attack"]

safe_print(f"\nVocê escolheu: {classe.title()} - HP: {player['hp']} | Ataque: {player['attack']}")


# --- Função de level up ---
def level_up():
    leveled = False
    while player["xp"] >= player["xp_next"]:
        player["level"] += 1
        player["xp"] -= player["xp_next"]
        player["xp_next"] += 20
        player["hp"] += 5
        leveled = True
        safe_print(f"\n✨ LEVEL UP! Agora você é nível {player['level']}! HP aumentado! ✨")
    return leveled


# --- Loop principal ---
while True:
    local = random.choice(mapa)
    safe_print(f"\nVocê entrou em: {local}")

    # Chance de achar item
    if random.random() < 0.3:
        item = random.choice(itens_disponiveis)
        player["inventory"].append(item)
        safe_print(f"📦 Você encontrou um item: {item}!")

    # Encontro com inimigo
    enemy = random.choice(enemies).copy()
    safe_print(f"\n⚔️ Um {enemy['name']} apareceu!")

    # Faça uma cópia do HP do jogador para permitir mortes e continuar testes
    # (em jogos reais você manteria o HP real)
    while enemy["hp"] > 0 and player["hp"] > 0:
        safe_print(f"\nSeu HP: {player['hp']} | Nível: {player['level']} | XP: {player['xp']}/{player['xp_next']}")
        safe_print(f"Inventário: {player['inventory']}")

        action_prompt = "\n[1] Atacar  [2] Item  [3] Fugir\nEscolha: "
        action = get_input(action_prompt, NON_INTERACTIVE_ACTION).strip()

        if action == "1":
            dano = random.randint(*player["attack"])
            enemy["hp"] -= dano
            safe_print(f"Você causou {dano} de dano! HP do inimigo: {max(enemy['hp'], 0)}")

            if enemy["hp"] <= 0:
                safe_print(f"\nVocê derrotou o {enemy['name']}! Ganhou {enemy['xp']} XP.")
                player["xp"] += enemy["xp"]
                level_up()
                break

            dano_inimigo = random.randint(*enemy["attack"])
            player["hp"] -= dano_inimigo
            safe_print(f"O {enemy['name']} atacou! Você perdeu {dano_inimigo}.")

        elif action == "2":
            if "Poção de Cura" in player["inventory"]:
                player["hp"] += 10
                player["inventory"].remove("Poção de Cura")
                safe_print("Você usou uma Poção de Cura! +10 HP.")
            else:
                safe_print("Você não tem itens utilizáveis!")

        elif action == "3":
            safe_print("Você fugiu!")
            break

        else:
            safe_print("Opção inválida. Usando ação padrão: atacar.")
            # Comportamento de fallback: atacar
            dano = random.randint(*player["attack"])
            enemy["hp"] -= dano
            safe_print(f"Você causou {dano} de dano! HP do inimigo: {max(enemy['hp'], 0)}")
            if enemy["hp"] <= 0:
                safe_print(f"\nVocê derrotou o {enemy['name']}! Ganhou {enemy['xp']} XP.")
                player["xp"] += enemy["xp"]
                level_up()
                break

            dano_inimigo = random.randint(*enemy["attack"])
            player["hp"] -= dano_inimigo
            safe_print(f"O {enemy['name']} atacou! Você perdeu {dano_inimigo}.")

    if player["hp"] <= 0:
        safe_print("\n💀 Você morreu! Fim do jogo.")
        break

    continuar = get_input("\nDeseja viajar para outro local? (s/n): ", NON_INTERACTIVE_CONTINUE).strip().lower()
    if continuar != "s":
        safe_print("\nObrigado por jogar!")
        break

# Fim do jogo
safe_print("(Sessão finalizada)")


    