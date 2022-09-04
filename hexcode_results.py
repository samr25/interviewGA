import json


class HexCodeResults:
    hexcode_word_results = {}

    def write_to_file(self):
        f = open("HexcodeResults.txt", "a")
        json_str = json.dumps(self.hexcode_word_results)
        f.write(json_str)
        f.close()

    @staticmethod
    def create_file():
        f = open("HexcodeResults.txt", "w")
        f.write("")
        f.close()

