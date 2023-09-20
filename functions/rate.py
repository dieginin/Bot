from models.Player import Player


def rate(pd: Player):
    # Ponderación para cada criterio
    weight_brawlers_count = 0.35
    weight_brawlers_power_11 = 0.2
    weight_brawlers_power_10 = 0.15
    weight_brawlers_power_9 = 0.1
    weight_trophies = 0.2

    brawlers_power_9 = [brawler for brawler in pd.brawlers if brawler.power == 9]
    brawlers_power_10 = [brawler for brawler in pd.brawlers if brawler.power == 10]
    brawlers_power_11 = [brawler for brawler in pd.brawlers if brawler.power == 11]

    brawlers_count = len(pd.brawlers)
    len_11 = len(brawlers_power_11) if brawlers_power_11 else 0
    len_10 = len(brawlers_power_10) if brawlers_power_10 else 0
    len_9 = len(brawlers_power_9) if brawlers_power_9 else 0

    # Calcular calificación en base a los criterios
    score = (
        (brawlers_count * weight_brawlers_count)
        + (len_11 * weight_brawlers_power_11)
        + (len_10 * weight_brawlers_power_10)
        + (len_9 * weight_brawlers_power_9)
        + (pd.trophies * weight_trophies)
    )

    # Si los trofeos son mayores a 25000, mejorar la calificación
    if pd.trophies > 25000:
        score *= 1.2  # Incremento del 20% en la calificación

    # Ajustar la calificación en una escala de 1 a 10
    final_rating = max(1, min(10, score / 1000))

    if isinstance(final_rating, int):
        return final_rating
    else:
        return f"{final_rating:.2f}"
