import web_crawler


def main():
    URL = input("Enter URL to mapping: ")
    dictionary = web_crawler.site_map(URL)
    print("\n")
    for rec in dictionary:
        print(rec)
        print(dictionary[rec])
        print("\n")


if __name__ == '__main__':
    main()
