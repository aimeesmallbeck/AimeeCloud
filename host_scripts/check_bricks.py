import arduino.app_bricks as ab
import os
print("Available bricks:")
for attr in dir(ab):
    if not attr.startswith('_'):
        print(f"  - {attr}")