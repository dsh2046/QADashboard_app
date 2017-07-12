import csv
class csvLibrary(object):

    def read_csv_file(self, filename):
        data = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        return data