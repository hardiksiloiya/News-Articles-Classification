def get_links(keywords):
    '''Function for getting top links from the Google News API
    Usage: keywords:string that you want the news links to be related to
    Example: get_links('google cloud anthos')
    '''
    links=[]
    news=GoogleNews()
    news.get_news(keywords)
    for i in news.results()[:20]:   #max number of links to process can be set here
        try:
                   
            if i['link'].startswith('https'):
                res=requests.get(i['link'])   
            else:
                res=requests.get('https://'+i['link'])
            links.append(res.url)
        except:
            pass
    return links