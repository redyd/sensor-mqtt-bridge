def score_humidity(humidity: float) -> float:
    if 70 < humidity < 80:
        return 80 - humidity
    if 30 <= humidity <= 70:
        return 10
    if 20 < humidity < 30:
        return humidity - 20
    return 0


def score_co2(co2: float) -> float:
    if 0 <= co2 < 2500:
        return 10
    if 2500 <= co2 <= 4500:
        return (co2 - 4500) / -200
    return 0


def score_temperature(temperature: float) -> float:
    if 20 <= temperature <= 25:
        return 10
    if 15 < temperature < 20:
        return 2 * (temperature - 15)
    if 25 < temperature < 35:
        return 35 - temperature
    return 0


def score_particulate_matter(particulate_matter: float) -> float:
    if 0 <= particulate_matter < 25:
        return 10
    if 25 <= particulate_matter < 35:
        return 35 - particulate_matter
    return 0


def score_global(
    temperature_score: float,
    humidity_score: float,
    co2_score: float,
    particulate_matter_score: float,
) -> float:
    return (
        temperature_score * 0.8
        + co2_score
        + particulate_matter_score
        + humidity_score * 0.8
    ) / 3.6


def calculate_scores(
    temperature: float,
    humidity: float,
    co2: float,
    particulate_matter: float,
) -> dict[str, float]:
    scores = {
        "temperature": score_temperature(temperature),
        "humidity": score_humidity(humidity),
        "co2": score_co2(co2),
        "particulate_matter": score_particulate_matter(particulate_matter),
    }
    scores["global"] = score_global(
        scores["temperature"],
        scores["humidity"],
        scores["co2"],
        scores["particulate_matter"],
    )
    return scores
