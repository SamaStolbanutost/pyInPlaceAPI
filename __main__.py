import urllib.request
try:
    from BeutifulSoup import BeutifulSoup
except:
    from bs4 import BeautifulSoup

def getLast():
    articles = {}
    connection = urllib.request.urlopen("https://www.interestingplace.ru")
    if connection.getcode() == 200:
        page = connection.read()
        parsed = BeautifulSoup(page, "lxml")
        for data in parsed.findAll("a", {"class": "block"}):
            for header in data.find_all("h2"):
                articles[header.text] = data["href"]
        return articles
    else:
        return "An error has occured. Errorcode: " + str(connection.getcode())

def getPost(link):
    connection = urllib.request.urlopen("https://www.interestingplace.ru" + link)
    if connection.getcode() == 200:
        page = connection.read()
        parsed = BeautifulSoup(page, "lxml")
        post = str(parsed.body).replace('<body>\n<div class="footer">\n<h1><a class="llogo" href="/">interestingplace.</a></h1>\n<div class="create">\n<a class="button" href="/info.html">создать</a>\n</div>\n</div>\n', "")
        post = post.replace("\n</body>", "")
        return post

    else:
        return "An error has occured. Errorcode: " + str(connection.getcode())

def writePost(article, text, filename):
    try:
        article = str(article).replace(" ", "%20")
        filename = str(filename).replace(" ", "%20")
        text = str(text).replace(" ", "%20")
        if article.replace("%20", "") == "" or filename.replace("%20", "") == "" or text.replace("%20", "") == "":
            error()
        connection = urllib.request.urlopen("https://www.interestingplace.ru/withlovefosssru/" + filename + "/" + text + "/" + article)
        return "Returncode: " + str(connection.getcode()) + "\nReply: " + str(connection.read())
    except:
        return "An error has occured."

while True:
    i = 0
    articles = getLast()
    articles_numered = {}
    for article in articles:
        print("\n", i, article, "\n")
        articles_numered[i] = article
        i += 1

    print("\n", i, "Stop\n")
    articles_numered[i] = "break"
    i += 1

    print("\n", i, "Write Post\n")
    articles_numered[i] = "wpost"

    try:
        article_to_read = int(input(" What to read? "))
        if articles_numered[article_to_read] == "break":
            break
        elif articles_numered[article_to_read] == "wpost":
            article = input("Enter an article: ")
            while article.replace(" ", "") == "":
                article = input("Enter an article: ")

            text = input("Enter the text: ")
            while text.replace(" ", "") == "":
                text = input("Enter the text: ")

            filename = input("Enter a filename (without .html): ")
            while filename.replace(" ", "") == "":
                filename = input("Enter a filename (without .html): ")

            writePost(article, text, filename)

        else:
            try:
                print("\n", getPost(articles[articles_numered[article_to_read]]), "\n")
            except:
                print("An error has occured.")
    except:
        print("Not a number")
