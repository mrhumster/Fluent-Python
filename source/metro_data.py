from operator import itemgetter

metro_data = [
    ('Tokyo', 'JP', 36.933, (35, 139)),
    ('Delhi NCR', 'IN', 21.935, (28, 77)),
    ('Mexico City', 'MX', 20.142, (19, -99)),
    ('New York-Newark', 'US', 20.104, (40, -74)),
    ('Sao Paulo', 'BR', 19.649, (-23, -46)),
]

for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
