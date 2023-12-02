import requests


class Article:
    def __init__(self, headline, year, month, url, keywords):
        self.headline = headline
        self.year = year
        self.month = month
        self.url = url
        self.keywords = keywords


def getArticles(arr, startYear, endYear):  # Returns arr of article objects
    api_key = 'CqAGNdgXrh1N2aDKZhnF7tWLeAKrDYwj'

    # iterating through entire new york times archive api
    for i in range(startYear, endYear):
        for j in range(13):
            year = i
            month = j

            url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={api_key}'

            # API call
            response = requests.get(url)

            # checking success code
            if response.status_code == 200:
                # parsing json file
                data = response.json()

                # checking for response and docs inside the data
                if 'response' in data and 'docs' in data['response']:

                    for article_data in data['response']['docs']:
                        # checking for publish dates aka checking if the month of articles is empty
                        if 'pub_date' not in article_data:
                            continue

                        # titles, url, time 
                        title = article_data['headline']['main']
                        url = article_data['web_url']
                        # time structure is "year-month-day-hours:minutes:seconds+0000"
                        # ex: 2019-01-01T05:00:00+0000"
                        # T is just a string to represent time

                        time = article_data['pub_date']
                        yearPub = time[0:4]
                        monthPub = time[6:7]

                        # extracting  keywords
                        keywords = [keyword['value'] for keyword in article_data.get('keywords', [])]

                        arr.append(Article(title, yearPub, monthPub, url, keywords))

                    for article_info in arr:
                        print("Title:", article_info.headline)
                        print("URL:", article_info.url)
                        print("Date Published:", article_info.year, "-", article_info.month)
                        print("Keywords:", ", ".join(article_info.keywords))
                        print("\n" + "=" * 50 + "\n")
                else:
                    print("Error: 'response' or 'docs' keys not found in the API response.")
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}, {response.text}")

            return arr
