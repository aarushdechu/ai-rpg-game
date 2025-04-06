from game_logic.inventory import add_item, drop_item, get_inventory
from game_logic.memory import save_progress

SHOP_ITEMS = {
    "Health Potion": {"price": 10, "effect": "Restores 20 HP"},
    "Torch": {"price": 5, "effect": "Lights up dark places"},
    "Magic Sword": {"price": 50, "effect": "Stronger attacks"},
    "Shield": {"price": 30, "effect": "Reduces enemy damage"},
}

def visit_shop(game_state):
    print("\n\U0001F6D2 Welcome to the Merchant's Shop!\n")
    print(f"💰 You have {game_state['gold']} gold.\n")

    print("Items for sale:")
    for item, details in SHOP_ITEMS.items():
        print(f"- {item}: {details['price']} gold ({details['effect']})")

    action = input("\nDo you want to [buy] an item, [sell] an item, or [leave] the shop? ").strip().lower()

    if action == "buy":
        item_to_buy = input("Enter the name of the item you want to buy: ").strip()
        if item_to_buy in SHOP_ITEMS:
            price = SHOP_ITEMS[item_to_buy]["price"]
            if game_state["gold"] >= price:
                game_state["gold"] -= price
                add_item(game_state, item_to_buy)
                print(f"\n✅ You bought {item_to_buy} for {price} gold!")
            else:
                print("\n❌ You don't have enough gold.")
        else:
            print("\n❌ That item is not available in the shop.")

    elif action == "sell":
        get_inventory(game_state)
        item_to_sell = input("Enter the name of the item you want to sell: ").strip()
        if item_to_sell in game_state["inventory"]:
            sell_price = SHOP_ITEMS.get(item_to_sell, {"price": 5})["price"] // 2
            game_state["gold"] += sell_price
            drop_item(game_state, item_to_sell)
            print(f"\n✅ You sold {item_to_sell} for {sell_price} gold!")
        else:
            print("\n❌ You don't have that item to sell.")

    elif action == "leave":
        print("\n🚪 You leave the shop and continue your adventure.")

    save_progress(game_state)