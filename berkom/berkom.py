GREEN = "\033[92m"
RESET = "\033[0m"
W = 56
MAX_NAME = 20
line = "+" + "-" * W + "+"


def row(text):
    print(f"| {text:<{W - 2}} |")


def title(text):
    print(f"|{text:^{W}}|")


def error(text):
    print(line)
    row(text)
    print(line)


def make_ticket_no(text):
    total = 0
    for ch in text:
        total = (total * 31 + ord(ch)) % 100000
    return str(total).zfill(5)


def main():
    train_art = r"""
      _______________________________________________
     /  _____    _____    _____    _____    _____    |
    /  |     |  |     |  |     |  |     |  |     |   |
   /   |_____|  |_____|  |_____|  |_____|  |_____|   |
  |   JAKARTA TRAIN TICKET SYSTEM                    |
  |__________________________________________________|
     (O)  (O)                          (O)  (O)
    ==========================================================
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """

    print(GREEN + train_art)
    print(line)

    name = input("| Name      : ").strip()
    if name == "":
        error("Name cannot be empty")
        return
    if len(name) > MAX_NAME:
        name = name[:MAX_NAME]

    print(line)
    row("Choose train")
    row("[1] MRT   [2] KRL   [3] LRT")
    print(line)
    choice = input("| Choice    : ")

    if choice == "1":
        train = "MRT"
        station = ["Lebak Bulus", "Fatmawati", "Cipete Raya", "Haji Nawi", "Blok A",
                   "Blok M", "ASEAN", "Senayan", "Istora", "Bendungan Hilir",
                   "Setiabudi", "Dukuh Atas", "Bundaran HI"]
        first_price = 10000
        next_price = 10000
    elif choice == "2":
        train = "KRL"
        station = ["Jakarta Kota", "Jayakarta", "Mangga Besar", "Sawah Besar", "Juanda",
                   "Gondangdia", "Cikini", "Manggarai", "Tebet", "Cawang",
                   "Duren Kalibata", "Pasar Minggu Baru", "Pasar Minggu"]
        first_price = 3000
        next_price = 5000
    elif choice == "3":
        train = "LRT"
        station = ["Dukuh Atas", "Setiabudi", "Rasuna Said", "Kuningan", "Pancoran",
                   "Cikoko", "Ciliwung", "Cawang", "Taman Mini", "Kampung Rambutan",
                   "Ciracas", "Harjamukti"]
        first_price = 5000
        next_price = 7000
    else:
        error("Train not available, sir " + name)
        return

    print(line)
    title(train + " STATIONS")
    print(line)
    for i in range(len(station)):
        row("[" + str(i + 1) + "] " + station[i])
    print(line)

    start_input = input("| From (no.) : ")
    end_input = input("| To   (no.) : ")

    if not start_input.isdigit() or not end_input.isdigit():
        error("Please enter station numbers, sir " + name)
        return

    start = int(start_input) - 1
    end = int(end_input) - 1

    if start < 0 or start >= len(station) or end < 0 or end >= len(station):
        error("Station not found, sir " + name)
        return

    if start == end:
        error("Departure and destination are the same, sir " + name)
        return

    distance = abs(end - start)

    price = 0
    for i in range(distance):
        if i < 2:
            price += first_price
        else:
            price += next_price

    ticket = make_ticket_no(name + station[start] + station[end])

    print(line)
    title("TICKET")
    print(line)
    row("Passenger : " + name)
    row("Train     : " + train)
    row("From      : " + station[start])
    row("To        : " + station[end])
    row("Stops     : " + str(distance))
    row("Price     : Rp" + str(price))
    row("Ticket No : " + ticket)
    print(line)
    title("Have a safe trip, sir " + name + "!")
    print(line)


main()
print(RESET, end="")
