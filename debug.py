import settings as s
import random
weapons = []
for key, value in s.weapons.items():
                    if key == 'multiple bullet':
                        continue
                    if value:
                        for i in range(value):
                            weapons.append(key)

print(weapons)

