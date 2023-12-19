from core.domain.pairing_model import Pairing
from core.domain.combination_model import Combination


def fetch_combination_ranking(order_by_popular: bool) -> list:
    result_list = list()
    for record in (
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
    ).tuples():
        (
            id,
            count,
            description,
            alcohol_id,
            alcohol_type,
            alcohol_subtype,
            alcohol_name,
            alcohol_image,
            alcohol_description,
            food_id,
            food_type,
            food_subtype,
            food_name,
            food_image,
            food_description,
        ) = record
        result_list.append(
            {
                "id": id,
                "count": count,
                "description": description,
                "alcohol": {
                    "id": alcohol_id,
                    "type": alcohol_type,
                    "subtype": alcohol_subtype,
                    "name": alcohol_name,
                    "image": alcohol_image,
                    "description": alcohol_description
                },
                "food": {
                    "id": food_id,
                    "type": food_type,
                    "subtype": food_subtype,
                    "name": food_name,
                    "image": food_image,
                    "description": food_description
                }
            }
        )
    return result_list
