import urllib.parse


def get_google_maps_link(location_name: str, city: str):
    base_url = "https://www.google.com/maps/search/"
    query = f"{location_name}, {city}"
    encoded_query = urllib.parse.quote(query)
    return f"{base_url}{encoded_query}"


if __name__ == "__main__":
    print(get_google_maps_link("Cluj-Napoca Old Town", "Cluj-Napoca"))
