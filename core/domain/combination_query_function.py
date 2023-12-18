from core.domain.pairing_model import Pairing
from core.domain.combination_model import Combination


def fetch_combination_ranking(order_by_popular: bool):
    return (
        Combination.select(
            Combination.id,
            Combination.count,
            Combination.description,
            Pairing.alias("alcohol_pairing").id,
            Pairing.alias("alcohol_pairing").type,
            Pairing.alias("alcohol_pairing").subtype,
            Pairing.alias("alcohol_pairing").name,
            Pairing.alias("alcohol_pairing").image,
            Pairing.alias("alcohol_pairing").description,
            Pairing.alias("food_pairing").id,
            Pairing.alias("food_pairing").type,
            Pairing.alias("food_pairing").subtype,
            Pairing.alias("food_pairing").name,
            Pairing.alias("food_pairing").image,
            Pairing.alias("food_pairing").description,
        )
        .where(Combination.is_deleted == False)
        .join(
            Pairing.alias("alcohol_pairing"),
            on=(Combination.alcohol == Pairing.alias("alcohol_pairing").id),
        )
        .join(
            Pairing.alias("food_pairing"),
            on=(Combination.food == Pairing.alias("food_pairing").id),
        )
        .order_by(Combination.count.desc() if order_by_popular else Combination.count)
    ).tuples()
