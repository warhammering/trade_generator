import random
from typing import Union, List, Tuple, Dict, Optional

# Define data structures for cargo and price tables
random_cargo_table: Dict[str, Dict[Tuple[int, int], str]] = {
    "spring": {
        (1, 9): "fish",
        (10, 19): "grain",
        (20, 25): "fabric",
        (26, 30): "pottery",
        (31, 35): "hides",
        (36, 45): "timber",
        (46, 48): "citrus",
        (49, 51): "olives",
        (52, 56): "ores",
        (57, 62): "livestock",
        (63, 67): "tools",
        (68, 72): "herbs",
        (73, 77): "stone",
        (78, 81): "spices",
        (82, 85): "glass",
        (86, 90): "metal",
        (91, 92): "books",
        (93, 94): "armaments",
        (95, 95): "jewelry",
        (96, 100): "alcohol",
    },
    "summer": {
        (1, 10): "fish",
        (11, 20): "grain",
        (21, 25): "fabric",
        (26, 30): "pottery",
        (31, 35): "hides",
        (36, 45): "timber",
        (46, 48): "citrus",
        (49, 51): "olives",
        (52, 56): "ores",
        (57, 62): "livestock",
        (63, 67): "tools",
        (68, 72): "herbs",
        (73, 77): "stone",
        (78, 81): "spices",
        (82, 85): "glass",
        (86, 90): "metal",
        (91, 92): "books",
        (93, 94): "armaments",
        (95, 95): "jewelry",
        (96, 100): "alcohol",
    },
    "autumn": {
        (1, 8): "fish",
        (9, 20): "grain",
        (21, 26): "fabric",
        (27, 30): "pottery",
        (31, 35): "hides",
        (36, 45): "timber",
        (46, 48): "citrus",
        (49, 51): "olives",
        (52, 56): "ores",
        (57, 62): "livestock",
        (63, 67): "tools",
        (68, 72): "herbs",
        (73, 77): "stone",
        (78, 81): "spices",
        (82, 85): "glass",
        (86, 90): "metal",
        (91, 92): "books",
        (93, 94): "armaments",
        (95, 95): "jewelry",
        (96, 100): "alcohol",
    },
    "winter": {
        (1, 8): "fish",
        (9, 18): "grain",
        (19, 23): "fabric",
        (24, 28): "pottery",
        (29, 33): "hides",
        (34, 43): "timber",
        (44, 46): "citrus",
        (47, 49): "olives",
        (50, 54): "ores",
        (55, 60): "livestock",
        (61, 65): "tools",
        (66, 70): "herbs",
        (71, 75): "stone",
        (76, 79): "spices",
        (80, 83): "glass",
        (84, 88): "metal",
        (89, 90): "books",
        (91, 92): "armaments",
        (93, 93): "jewelry",
        (94, 100): "alcohol",
    },
}

base_price_table: Dict[str, Tuple[Union[int, str], ...]] = {
    "fish": (0.5, 0.5, 0.5, 1),
    "grain": (1, 1, 0.25, 0.5),
    "fabric": (1, 1.5, 2, 3),
    "pottery": (2, 1.5, 2, 2.5),
    "hides": (3, 2.5, 3, 3.5),
    "timber": (3, 1.5, 2, 3.5),
    "citrus": (3, 1, 0.5, 1),
    "olives": (3, 2, 2, 3),
    "ores": (3, 3, 3, 3),
    "livestock": (4, 3, 3, 5),
    "tools": (4, 4, 4, 5),
    "herbs": (5, 4, 5, 6),
    "stone": (5, 5, 5, 5),
    "spices": (6, 6, 6, 6),
    "glass": (7, 6.5, 6, 7.5),
    "metal": (8, 8, 8, 8),
    "books": (10, 10, 10, 10),
    "armaments": (12, 10, 8, 10),
    "jewelry": (15, 15, 15, 15),
    "alcohol": ("special", "special", "special", "special"),
}


# Helper functions
def get_season_index(season: str) -> int:
    """Return the index of the season."""
    return {"spring": 0, "summer": 1, "autumn": 2, "winter": 3}[season]


def get_product(season: str, roll: int) -> Optional[str]:
    """Return the product depending on the season."""
    for range_tuple, product in random_cargo_table[season].items():
        if range_tuple[0] <= roll <= range_tuple[1]:
            return product
    return None


def get_price(product: str, season: str) -> Union[int, str]:
    """Return the price depending on the product and the season."""
    season_index = get_season_index(season)
    return base_price_table[product][season_index]


def check_if_cargo_for_sale(roll: int, loc_size: int, loc_wealth: int) -> bool:
    """Check if cargo is available for sale based on the roll and location properties."""
    availability = (loc_size + loc_wealth) * 10
    return roll <= availability


def calculate_cargo_size(
    size_roll: int, loc_size: int, loc_wealth: int, is_trade_center: bool
) -> int:
    """Calculate the size of the available cargo."""
    combined_value = loc_size + loc_wealth
    if is_trade_center:
        reversed_roll = int(str(size_roll)[::-1])  # Reverse the digits of the roll
        size_roll = max(size_roll, reversed_roll)
    cargo_size = combined_value * size_roll  # Calculate cargo size before rounding
    return (cargo_size + 9) // 10 * 10  # Round up to the nearest 10


def get_random_cargo(
    loc_size: int, loc_wealth: int, is_trade_center: bool, season: str, rolls: dict
) -> List[Tuple[str, Union[int, str], int]]:
    """Generate available cargo and their prices based on location properties."""
    product_d100 = random.randint(1, 100)
    rolls["product_roll"] = product_d100
    product = get_product(season, product_d100)
    price = get_price(product, season)

    size_roll = random.randint(1, 100)
    rolls["size_roll"] = size_roll  # Store size roll
    cargo_size = calculate_cargo_size(size_roll, loc_size, loc_wealth, is_trade_center)

    return [(product, price, cargo_size)]


def get_haggle_multiplier(haggle: str) -> float:
    """Return the haggle multiplier based on the haggle result."""
    haggle_multipliers = {"a": 0.8, "b": 0.9, "c": 1.0, "d": 1.1, "e": 1.2}
    return haggle_multipliers.get(haggle, 1.0)


def adjust_base_price(
    base_price: float, buy_all: bool, partial_units: int = 0, cargo_size: int = 1
) -> float:
    """Adjust the base price based on whether all cargo is being bought or not."""
    if not buy_all and partial_units > 0:
        return base_price * 1.10 * (partial_units / cargo_size)
    return base_price


def calculate_price(
    base_price: float,
    cargo_size: int,
    haggle: str,
    buy_all: bool,
    partial_units: int = 0,
) -> float:
    """Calculate the final price based on base price, cargo size, haggle result, and whether all cargo is being bought."""
    if not buy_all and partial_units > 0:
        base_price = adjust_base_price(base_price, buy_all, partial_units, cargo_size)
    multiplier = get_haggle_multiplier(haggle)
    return round(base_price * (cargo_size / 10) * multiplier, 1)


def calculate_initial_price(
    product: Tuple[str, Union[int, str], int], buy_all: bool, partial_units: int = 0
) -> Union[float, str]:
    """Calculate the initial price before haggling."""
    name, base_price, cargo_size = product
    if isinstance(base_price, (int, float)):
        if not buy_all and partial_units > 0:
            base_price = adjust_base_price(
                base_price, buy_all, partial_units, cargo_size
            )
        return round(base_price * (cargo_size / 10), 1)
    return base_price


def calculate_prices(
    product: Tuple[str, Union[int, str], int],
    buy_all: bool,
    haggle: str,
    partial_units: int = 0,
) -> List[Tuple[str, float]]:
    """Calculate the final prices after haggling."""
    name, base_price, cargo_size = product
    if isinstance(base_price, (int, float)):
        final_price = calculate_price(
            base_price, cargo_size, haggle, buy_all, partial_units
        )
        return [(name, final_price)]
    return []


def display_product_info(products: List[Tuple[str, Union[int, str], int]]) -> None:
    """Display information about the available products."""
    for product, price, cargo_size in products:
        print(
            f"In this town you find {product} with a base price of {price} and a cargo size of {cargo_size}"
        )
        if price == "special":
            print(f"{product.capitalize()} is special")


def display_rolls(rolls: dict) -> None:
    """Display all the rolls in a presentable way."""
    print("\nRolls Summary:")
    for roll_name, roll_value in rolls.items():
        print(f"{roll_name.replace('_', ' ').capitalize()}: {roll_value}")


# Main function to execute the cargo and price calculation process
def main() -> None:
    """Main function to execute the cargo and price calculation process."""
    loc_size = int(input("What is the location size: "))
    loc_wealth = int(input("What is the location wealth: "))
    is_trade_center = (
        input("Is this a trade center (y/n) [default: n]: ").strip().lower() == "y"
    )
    season = input("Please enter a season: ").strip().lower()

    rolls = {}

    # Roll for availability
    availability_rolls = [random.randint(1, 100)]
    if is_trade_center:
        availability_rolls.append(random.randint(1, 100))

    rolls["availability_rolls"] = availability_rolls

    if not any(
        check_if_cargo_for_sale(roll, loc_size, loc_wealth)
        for roll in availability_rolls
    ):
        print("No cargo available for sale.")
        display_rolls(rolls)
        return

    products_input = input(
        "Enter goods produced in town, separated by commas (or press Enter to use random): "
    ).strip()
    available_products = []

    if products_input:
        products_list = [product.strip() for product in products_input.split(",")]
        if not is_trade_center and len(products_list) > 1:
            products_list = [random.choice(products_list)]

        for product in products_list:
            if product in base_price_table:
                product_d100 = random.randint(1, 100)
                rolls[f"product_roll_{product}"] = product_d100
                price = get_price(product, season)
                size_roll = random.randint(1, 100)
                rolls[f"size_roll_{product}"] = size_roll
                cargo_size = calculate_cargo_size(
                    size_roll, loc_size, loc_wealth, is_trade_center
                )
                available_products.append((product, price, cargo_size))

        if is_trade_center:
            roll = random.randint(1, 100)
            rolls["extra_product_roll"] = roll
            extra_product = get_product(season, roll)
            if extra_product in base_price_table:
                price = get_price(extra_product, season)
                size_roll = random.randint(1, 100)
                rolls["extra_size_roll"] = size_roll
                cargo_size = calculate_cargo_size(
                    size_roll, loc_size, loc_wealth, is_trade_center
                )
                available_products.append((extra_product, price, cargo_size))
    else:
        available_products = get_random_cargo(
            loc_size, loc_wealth, is_trade_center, season, rolls
        )
        if is_trade_center:
            extra_product_data = get_random_cargo(
                loc_size, loc_wealth, is_trade_center, season, rolls
            )
            available_products.extend(extra_product_data)

    # Ensure only 2 items if trade center
    if is_trade_center and len(available_products) > 2:
        available_products = available_products[:2]

    if available_products:
        print(f"Merchant haggle skill is of {30 + random.randint(3, 30)}")
        display_product_info(available_products)

        for product in available_products:
            name, price, cargo_size = product
            if price != "special":
                buying_all = (
                    input(f"Are you buying all the cargo of {name}? (y/n): ")
                    .strip()
                    .lower()
                    == "y"
                )
                partial_units = 0
                if not buying_all:
                    partial_units = int(
                        input(f"How many units of {name} are you buying?: ").strip()
                    )

                initial_price = calculate_initial_price(
                    product, buying_all, partial_units
                )
                print(f"The initial price for {name} is {initial_price}")

                print("What was the result of your Haggle test?")
                print("a) D (-20%)")
                print("b) S (-10%)")
                print("c) N (+0%) [default]")
                print("d) F (+10%)")
                print("e) FS (+20%)")
                haggle_result = (
                    input("Select an option (a/b/c/d/e) [default: c]: ").strip().lower()
                    or "c"
                )

                price_changes = calculate_prices(
                    product, buying_all, haggle_result, partial_units
                )
                for prod, new_price in price_changes:
                    print(f"The new price for {prod} is {new_price}")

        display_rolls(rolls)
    else:
        print("No cargo available for sale.")
        display_rolls(rolls)


if __name__ == "__main__":
    main()
