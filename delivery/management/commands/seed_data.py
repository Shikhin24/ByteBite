from django.core.management.base import BaseCommand
from delivery.models import Restaurant, Item

class Command(BaseCommand):
    help = "Seed initial restaurant and menu data"

    def handle(self, *args, **kwargs):

        restaurants = [
            # 🍕 Pizza / Italian
            ("Domino's Pizza", "Indiranagar", "Pizza", 4.1),
            ("Pizza Hut", "Whitefield", "Pizza", 4.0),
            ("La Pino'z Pizza", "BTM", "Pizza", 4.2),
            ("Onesta", "JP Nagar", "Italian", 4.3),
            ("Little Italy", "Indiranagar", "Italian (Veg)", 4.4),

            # 🍔 Burgers & Fast Food
            ("Truffles", "Koramangala", "American", 4.5),
            ("Burger King", "MG Road", "Burgers", 4.0),
            ("McDonald's", "Brigade Road", "Fast Food", 3.9),
            ("Leon Grill", "HSR Layout", "Fast Food", 4.3),
            ("California Burrito", "Indiranagar", "Mexican", 4.4),

            # 🍗 Chicken / Non-Veg
            ("KFC", "Jayanagar", "Fried Chicken", 4.0),
            ("Empire Restaurant", "Church Street", "North Indian", 4.2),
            ("Meghana Foods", "Residency Road", "Andhra", 4.6),
            ("Nandhana Palace", "Marathahalli", "Andhra", 4.3),
            ("Chicken County", "Rajajinagar", "Grill & BBQ", 4.1),

            # 🍛 South Indian
            ("Vidyarthi Bhavan", "Basavanagudi", "South Indian", 4.6),
            ("CTR", "Malleshwaram", "South Indian", 4.5),
            ("MTR", "Lalbagh", "South Indian", 4.4),
            ("Nagarjuna", "Residency Road", "South Indian", 4.3),
            ("Taaza Thindi", "Jayanagar", "South Indian", 4.5),

            # 🥗 Pure Veg
            ("Sukh Sagar", "Gandhi Bazaar", "Pure Veg", 4.1),
            ("Adiga's", "Majestic", "Pure Veg", 4.0),
            ("SLV", "Yelahanka", "Pure Veg", 4.2),
            ("Udupi Upahar", "Indiranagar", "Pure Veg", 4.3),
            ("Veena Stores", "Malleshwaram", "Pure Veg", 4.6),

            # 🍜 Asian / Chinese
            ("Mainland China", "Whitefield", "Chinese", 4.2),
            ("Beijing Bites", "Electronic City", "Chinese", 4.0),
            ("Chung Wah", "Richmond Road", "Chinese", 4.1),
            ("Mamagoto", "Forum Mall", "Pan Asian", 4.4),
            ("Wow! China", "BTM", "Chinese", 4.0),

            # 🍖 BBQ / Grill
            ("Barbeque Nation", "Indiranagar", "BBQ", 4.3),
            ("Absolute Barbeques", "Marathahalli", "BBQ", 4.4),
            ("Smoke House Deli", "UB City", "Continental", 4.2),
            ("The Black Pearl", "Whitefield", "BBQ", 4.3),
            ("Punjabi Rasoi", "Yelahanka", "North Indian", 4.1),

            # 🌮 Street / Casual
            ("EatFit", "HSR Layout", "Healthy", 4.1),
            ("FreshMenu", "Koramangala", "Multi-Cuisine", 4.0),
            ("Biryani Zone", "Bellandur", "Biryani", 4.2),
            ("Paradise Biryani", "Electronic City", "Biryani", 4.1),
            ("Hyderabadi Biryani House", "BTM", "Biryani", 4.3),
        ]

        for name, area, cuisine, rating in restaurants:
            restaurant, created = Restaurant.objects.get_or_create(
                name=name,
                area=area,
                defaults={
                    "cuisine": cuisine,
                    "rating": rating,
                    "picture": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
                    "location_url": "https://maps.google.com"
                }
            )

            if created:
                # Default menu items
                Item.objects.get_or_create(
                    restaurant=restaurant,
                    name="Special Dish",
                    defaults={
                        "description": f"Signature {cuisine} dish",
                        "price": 249,
                        "nonVeg": cuisine not in ["Pure Veg", "South Indian", "Healthy", "Italian (Veg)"],
                        "picture": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe"
                    }
                )

        self.stdout.write(self.style.SUCCESS("✅ 50 restaurants seeded successfully"))
