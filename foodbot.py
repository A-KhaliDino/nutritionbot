import requests

def get_food_data(product_name):
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": product_name,
        "json": 1,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])

        if products:
            return products[0]  # Return the first product found
        else:
            return None
    else:
        return None

def get_nutrition_data(product_id):
    base_url = f"https://world.openfoodfacts.org/api/v0/product/{product_id}.json"

    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data.get("product", {}).get("nutriments", {})
    else:
        return None

def calculate_nutritional_values(nutrition_data, amount_in_g):
    if nutrition_data and amount_in_g > 0:
        factor = amount_in_g / 100.0
        nutrition_values = {
            "Calories": round(nutrition_data.get("energy-kcal_100g", "N/A") * factor, 2),
            "Proteins": round(nutrition_data.get("proteins_100g", "N/A") * factor, 2),
            "Carbohydrates": round(nutrition_data.get("carbohydrates_100g", "N/A") * factor, 2),
            "Fats": round(nutrition_data.get("fat_100g", "N/A") * factor, 2)
        }
        return nutrition_values
    else:
        return None

def display_food_data(product_data, nutrition_data):
    if product_data:
        print("product found")
        if nutrition_data:
            print("Nutrition facts found")
        else:
            print("Nutrition facts not available for this product.")
    else:
        print("Product not found sorry :3 ~Khalid.")

if __name__ == "__main__":
    products_nutrition = []  # List to store nutrition data of all products

    while True:
        user_input = input("Enter a food product name (or 'done' to finish): ")
        if user_input.lower() == "done":
            break

        food_data = get_food_data(user_input)

        if food_data:
            product_id = food_data.get("code", None)
            nutrition_data = get_nutrition_data(product_id)
        else:
            print("Product not found sorry :3 ~Khalid.")
            continue

        display_food_data(food_data, nutrition_data)

        if nutrition_data:
            valid_amount = False
            while not valid_amount:
                amount_input = input("Enter the amount (in grams or ml) you would like to measure (numbers only): ")
                try:
                    amount_in_g = float(amount_input)
                    if amount_in_g > 0:
                        valid_amount = True
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("NUMBERS ONLY YA MONKEY, try again numbers only this time.")

            calculated_nutrition = calculate_nutritional_values(nutrition_data, amount_in_g)

            if calculated_nutrition:
                products_nutrition.append(calculated_nutrition)

    if products_nutrition:
        final_nutrition = {
            "Calories": sum(nutrition.get("Calories", 0) for nutrition in products_nutrition),
            "Proteins": sum(nutrition.get("Proteins", 0) for nutrition in products_nutrition),
            "Carbohydrates": sum(nutrition.get("Carbohydrates", 0) for nutrition in products_nutrition),
            "Fats": sum(nutrition.get("Fats", 0) for nutrition in products_nutrition)
        }

        print("\nFinal Nutritional Values:")
        for key, value in final_nutrition.items():
            print(key + ":", round(value, 2))
    else:
        print("No nutritional data available. Please enter at least one valid product.")
