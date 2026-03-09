import aiohttp


class FoodService:
    """Интеграция с OpenFoodFacts"""

    URL = "https://world.openfoodfacts.org/cgi/search.pl"

    @staticmethod
    async def search_product(product_name):

        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(FoodService.URL, params=params) as resp:

                data = await resp.json()
                products = data.get("products", [])

                if not products:
                    return None
                
                product = products[0]
                name = product.get("product_name", product_name)

                nutriments = product.get("nutriments", {})
                calories = nutriments.get("energy-kcal_100g")

                if calories is None:
                    return None
                
                return {
                    "name": name,
                    "calories_100g": float(calories)
                }