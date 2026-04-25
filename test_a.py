import json, time, urllib.request, urllib.parse

def send(L, R):
    j = json.dumps({"T": 1, "L": L, "R": R}, separators=(",", ":"))
    url = f"http://192.168.1.56/js?json={urllib.parse.quote(j, safe='')}"
    urllib.request.urlopen(url, timeout=2).read()

def yaw():
    j = json.dumps({"T": 1001}, separators=(",", ":"))
    url = f"http://192.168.1.56/js?json={urllib.parse.quote(j, safe='')}"
    with urllib.request.urlopen(url, timeout=2) as r:
        return json.loads(r.read().decode()).get("y", float("nan"))

y1 = yaw()
print(f"Before: {y1:.1f} deg")
send(-0.3, 0.3)
time.sleep(1.0)
send(0, 0)
time.sleep(0.3)
y2 = yaw()
print(f"After:  {y2:.1f} deg")
print(f"Delta:  {y2-y1:.1f} deg")
