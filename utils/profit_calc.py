def calculate_profit(product, shipping_cost):
    price = float(product.get('price', 0))
    target_profit_margin = 0.2  # 20% profit margin
    total_cost = price + shipping_cost
    return total_cost * (1 + target_profit_margin) <= price
