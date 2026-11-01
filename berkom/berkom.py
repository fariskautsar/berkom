
def main():
    GREEN = "\033[92m"
    W = 56
    line = "+" + "-" * W + "+"

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

    name = input("| Name      : ")
    print(line)
    print(f"| {'Choose train':<{W - 2}} |")
    print(f"| {'[1] MRT   [2] KRL   [3] LRT':<{W - 2}} |")
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
        print(line)
        print(f"| {'Train not available, sir ' + name:<{W - 2}} |")
        print(line)
        return

    print(line)
    print(f"|{train + ' STATIONS':^{W}}|")
    print(line)
    for i in range(len(station)):
        print(f"| {'[' + str(i + 1) + '] ' + station[i]:<{W - 2}} |")
    print(line)

    start_input = input("| From (no.) : ")
    end_input = input("| To   (no.) : ")

    if not start_input.isdigit() or not end_input.isdigit():
        print(line)
        print(f"| {'Please enter station numbers, sir ' + name:<{W - 2}} |")
        print(line)
        return

    start = int(start_input) - 1
    end = int(end_input) - 1

    if start < 0 or start >= len(station) or end < 0 or end >= len(station):
        print(line)
        print(f"| {'Station not found, sir ' + name:<{W - 2}} |")
        print(line)
        return

    distance = end - start
    if distance < 0:
        distance = distance * -1

    price = 0
    for i in range(distance):
        if i < 2:
            price += first_price
        else:
            price += next_price

    ticket = str(abs(hash(name + station[start] + station[end])) % 100000).zfill(5)

    print(line)
    print(f"|{'TICKET':^{W}}|")
    print(line)
    print(f"| {'Passenger : ' + name:<{W - 2}} |")
    print(f"| {'Train     : ' + train:<{W - 2}} |")
    print(f"| {'From      : ' + station[start]:<{W - 2}} |")
    print(f"| {'To        : ' + station[end]:<{W - 2}} |")
    print(f"| {'Stops     : ' + str(distance):<{W - 2}} |")
    print(f"| {'Price     : Rp' + str(price):<{W - 2}} |")
    print(f"| {'Ticket No : ' + ticket:<{W - 2}} |")
    print(line)
    print(f"|{'Have a safe trip, sir ' + name + '!':^{W}}|")
    print(line)


main()
print("\033[0m", end="")
