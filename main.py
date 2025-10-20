import datetime

class Record:
    def format(self):
        raise NotImplementedError("Subclasses must implement format method.")

class News(Record):
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def format(self):
        return f"News -------------------------\n{self.text}\n{self.city}, {self.date}\n"

class PrivateAd(Record):
    def __init__(self, text, expiration_date_str):
        self.text = text
        self.expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def format(self):
        return f"Private Ad ------------------\n{self.text}\nActual until: {self.expiration_date.strftime('%Y-%m-%d')}, {self.days_left} days left\n"

class WeatherReport(Record):  # Unique type
    def __init__(self, city, temperature):
        self.city = city
        self.temperature = temperature
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def format(self):
        return f"Weather Report --------------\nCity: {self.city}\nTemperature: {self.temperature}°C\nReported at: {self.date}\n"

class NewsFeed:
    def __init__(self, filename="news_feed.txt"):
        self.filename = filename

    def add_record(self, record: Record):
        with open(self.filename, "a") as f:
            f.write(record.format() + "\n")
        print("Record published!\n")

    def run(self):
        while True:
            print("\nSelect record type to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Weather Report")
            print("4. Exit")
            choice = input("Enter choice (1-4): ")

            if choice == "1":
                text = input("Enter news text: ")
                city = input("Enter city: ")
                record = News(text, city)
            elif choice == "2":
                text = input("Enter ad text: ")
                expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
                record = PrivateAd(text, expiration_date)
            elif choice == "3":
                city = input("Enter city: ")
                temperature = input("Enter temperature (°C): ")
                record = WeatherReport(city, temperature)
            elif choice == "4":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Try again.")
                continue

            self.add_record(record)

if __name__ == "__main__":
    feed = NewsFeed()
    feed.run()