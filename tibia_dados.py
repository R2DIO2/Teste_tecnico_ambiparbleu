import re

# Definir padrões de expressão regular para extrair os dados desejados
pattern_healing = re.compile(r"You healed yourself for (\d+) hitpoints")
pattern_damage_taken = re.compile(r"You lose (\d+) hitpoints due to an attack by a (\w+)|You lose (\d+) hitpoints\.")
pattern_damage_taken_by_creature = re.compile(r"A (\w+) loses (\d+) hitpoints due to your attack.")
pattern_experience = re.compile(r"You gained (\d+) experience points.")
pattern_items_dropped = re.compile(r"Loot of a (\w+): (\d+) (\w+)")
pattern_black_knight_health = re.compile(r"A Black Knight loses (\d+) hitpoints due to your attack\.")
pattern_unknown_damage = re.compile(r"You lose (\d+) hitpoints")

# Inicializar variáveis para armazenar as informações extraídas
total_healing = 0
total_damage_taken = 0
damage_taken_by_creature = {}
total_experience = 0
items_dropped_by_creature = {}
unknown_damage = 0
total_unknown_damage = 0
black_knight_max_health = 0
black_knight_current_health = 0

# Abrir o arquivo de log
with open("C:\Extração de dados do Tibia/Server Log (1).txt", "r") as log_file:
    # Ler cada linha do arquivo de log
    for line in log_file:
        # Extrair informações de cura
        healing_match = pattern_healing.search(line)
        if healing_match:
            healing = int(healing_match.group(1))
            total_healing += healing

        # Extrair informações de dano sofrido
        damage_taken_match = pattern_damage_taken.search(line)
        if damage_taken_match:
            if damage_taken_match.group(1):
                damage_taken = int(damage_taken_match.group(1))
            else:
                damage_taken = int(damage_taken_match.group(3))
            total_damage_taken += damage_taken

        # Extrair informações de dano sofrido por tipo de criatura
        damage_taken_by_creature_match = pattern_damage_taken_by_creature.search(line)
        if damage_taken_by_creature_match:
            creature = damage_taken_by_creature_match.group(1)
            damage_taken = int(damage_taken_by_creature_match.group(2))
            if creature in damage_taken_by_creature:
                damage_taken_by_creature[creature] += damage_taken
            else:
                damage_taken_by_creature[creature] = damage_taken
            total_damage_taken += damage_taken

        # Extrair informações de experiência recebida
        experience_match = pattern_experience.search(line)
        if experience_match:
            experience = int(experience_match.group(1))
            total_experience += experience

        # Extrair informações de itens dropados por criatura
        items_dropped_match = pattern_items_dropped.search(line)
        if items_dropped_match:
            creature = items_dropped_match.group(1)
            items_dropped = int(items_dropped_match.group(2))
            item = items_dropped_match.group(3)
            if creature in items_dropped_by_creature:
                items_dropped_by_creature[creature][item] = items_dropped
            else:
                items_dropped_by_creature[creature] = {item: items_dropped}

        # Extrair informações do dano desconhecido (Unknown damage)
        unknown_damage_match = pattern_unknown_damage.search(line)
        if unknown_damage_match:
            unknown_damage = int(unknown_damage_match.group(1))
            total_damage_taken += unknown_damage
            total_unknown_damage += unknown_damage

       # ...

        black_knight_health_match = pattern_black_knight_health.search(line)
        if black_knight_health_match:
            black_knight_damage = int(black_knight_health_match.group(1))
            black_knight_current_health -= black_knight_damage

        if abs(black_knight_current_health) > black_knight_max_health:
            black_knight_max_health = abs(black_knight_current_health)

# Imprimir as informações extraídas
print("Dano total curado pelo jogador:", total_healing)
print("Dano total sofrido pelo jogador:", total_damage_taken)
print("Dano total sofrido pelo jogador por tipo de criatura:")
for creature, damage_taken in damage_taken_by_creature.items():
    print(creature + ":", damage_taken)
print("Experiência total recebida:", total_experience)
print("Quantidade de itens dropados por cada criatura:")
for creature, items_dropped in items_dropped_by_creature.items():
    print(creature + ":")
    for item, quantity in items_dropped.items():
        print(item + ":", quantity)

# Imprimir o dano total sofrido por origens desconhecidas
print("Dano total sofrido por origens desconhecidas:", total_unknown_damage)


print("Vida total do Black Knight:", black_knight_max_health)
