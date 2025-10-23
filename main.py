import datetime
import os

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

class FileRecordImporter:
    """
    Input format example (records separated by blank lines):

    News
    Some news text here
    London

    PrivateAd
    Buy my bike!
    2025-12-01

    WeatherReport
    Paris
    18
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_records(self):
        with open(self.filepath, "r") as f:
            content = f.read().strip()
        raw_records = content.split('\n\n')
        records = []
        for raw in raw_records:
            lines = [line.strip() for line in raw.split('\n') if line.strip()]
            if not lines:
                continue
            record_type = lines[0]
            try:
                if record_type == "News" and len(lines) >= 3:
                    records.append(News(lines[1], lines[2]))
                elif record_type == "PrivateAd" and len(lines) >= 3:
                    records.append(PrivateAd(lines[1], lines[2]))
                elif record_type == "WeatherReport" and len(lines) >= 3:
                    records.append(WeatherReport(lines[1], lines[2]))
                else:
                    print(f"Skipped invalid record: {raw}")
            except Exception as e:
                print(f"Error parsing record: {raw}\nError: {e}")
        return records

    def import_to_feed(self, news_feed):
        records = self.parse_records()
        for record in records:
            news_feed.add_record(record)
        # Remove file after successful import
        os.remove(self.filepath)
        print(f"File '{self.filepath}' processed and removed.")

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
            print("4. Import from file")
            print("5. Exit")
            choice = input("Enter choice (1-5): ")

            if choice == "1":
                text = input("Enter news text: ")
                city = input("Enter city: ")
                record = News(text, city)
                self.add_record(record)
            elif choice == "2":
                text = input("Enter ad text: ")
                expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
                record = PrivateAd(text, expiration_date)
                self.add_record(record)
            elif choice == "3":
                city = input("Enter city: ")
                temperature = input("Enter temperature (°C): ")
                record = WeatherReport(city, temperature)
                self.add_record(record)
            elif choice == "4":
                path = input("Enter file path (leave blank for 'input.txt' in current folder): ").strip()
                if not path:
                    path = "input.txt"
                if os.path.exists(path):
                    importer = FileRecordImporter(path)
                    importer.import_to_feed(self)
                else:
                    print(f"File '{path}' not found.")
            elif choice == "5":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    feed = NewsFeed()
    feed.run()