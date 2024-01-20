from bs4 import BeautifulSoup
import requests

URL = "https://www.imdb.com/list/ls062613827/"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6"
}

response = requests.get(url=URL, headers=header)
content = response.text


class DramaData:
    def __init__(self):
        """scrap dramas data from imdb"""
        soup = BeautifulSoup(content, "html.parser")

        all_container = soup.find_all(name="div", class_="lister-item mode-detail")

        self.__data = []
        serial_num = 0
        for single_container in all_container:
            serial_num += 1
            name = (single_container.select_one(selector=".lister-item-header a")).getText()
            year = ((single_container.find(name="span", class_="lister-item-year")).getText()).strip("-")
            genres = ((single_container.find(name="span", class_="genre")).getText()).strip()
            rating = ((single_container.find(name="div", class_="ipl-rating-star")).getText()).strip()
            try:
                story = (single_container.find(name="div", class_="list-description")).find("p").getText().strip()
            except:
                story = "unavailable"
            self.__data.append({"id": serial_num, "title": name, "subtitle": genres, "date": year, "rating": rating, "body": story})

    def get_data(self):
        return self.__data


full_data = DramaData()
drama_data = full_data.get_data()
print(drama_data)
