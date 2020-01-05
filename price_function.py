# price functions corresponding to different zones and durations based on different pricing policies
# prase a document that describes the pricing policies

# default 
pricing_policy_default = [1/6000, 1/6000, 1/6000, 1/3000, 1/1500, 1/1000, 1/1000, 1/750, 1/600, 5/12]
pricing_policy = pricing_policy_default

price_one_low = pricing_policy[0]
price_one_medium = pricing_policy[1]
price_one_high = pricing_policy[2]
price_two_low = pricing_policy[3]
price_two_medium = pricing_policy[4]
price_two_high = pricing_policy[5]
price_three_low = pricing_policy[6]
price_three_medium = pricing_policy[7]
price_three_high = pricing_policy[8]
price_four = pricing_policy[9]

def penalty():
    total_penalty = 0
    
    # apply price function to each row and sum it up
    return total_penalty

def price_function(zone, duration):
    if zone == 1:
        price = price_function_one(duration)
    elif zone == 2:
        price = price_function_two(duration)
    elif zone == 3:
        price = price_function_three(duration)
    elif zone == 4:
        price = price_function_four(duration)
    return price

def price_function_one(duration):
    if duration <= 30:
        return 0
    elif duration <= 90:
        return (duration - 30) * price_one_low
    elif duration <= 150:
        return 60 * price_one_low + (duration - 90) * price_one_medium
    else:
        return 60 * price_one_low + 60 * price_one_medium + (duration - 150) * price_one_high

def price_function_two(duration):
    if duration <= 30:
        return 0
    elif duration <= 90:
        return (duration - 30) * price_two_low
    elif duration <= 150:
        return 60 * price_two_low + (duration - 90) * price_two_medium
    else:
        return 60 * price_two_low + 60 * price_two_medium + (duration - 150) * price_two_high

def price_function_three(duration):
    if duration <= 30:
        return 0
    elif duration <= 90:
        return (duration - 30) * price_three_low # which is a parameter
    elif duration <= 150:
        return 60 * price_three_low + (duration - 90) * price_three_medium
    else:
        return 60 * price_three_low + 60 * price_three_medium + (duration - 150) * price_three_high 

def price_function_four(duration):
    if duration <= 120:
        return 0
    else:
        return (duration - 120) * price_four