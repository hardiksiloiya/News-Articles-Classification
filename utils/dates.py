def get_dates(text,algo):
    '''
    Function for getting dates in a string
    Currently supports use of two modules
    returns a datetime object if it finds a valid date else 'N/A'.
    algo = 'date extractor' or 'datefinder'
    Example:
    string='this is a test string.'
    date=get_dates(string,algo='datefinder')
    '''
    if algo == 'date extractor':
        dates=extract_dates(text,return_precision=True)
        for date in dates:
            if date == None:
                continue
            if date[1]=='day':
                if date[0].year<2000 or date[0].year>datetime.datetime.now().year:
                    continue
                return date[0]
        return 'N/A'
    elif algo == 'datefinder':
        x = datetime.datetime(9996,12,31)
        matches = datefinder.find_dates(text,source=True,base_date=x)
        dates=[]
        ans=[]
        while True:
            try:
                m = next(matches)
            except TypeError as e:
                continue
            except StopIteration as e:
                break
            except Exception as e:
                raise e
            dates.append(m)
        for date in dates:
            tt=date[0]
            if tt.year<2000 or tt.year>datetime.datetime.now().year:
                continue
            if tt.year==datetime.datetime.now().year:
                if tt.month>datetime.datetime.now().month:
                    continue
                elif tt.month==datetime.datetime.now().month:
                    if tt.day>datetime.datetime.now().day:
                        continue

            if tt.month==12 and tt.day==31:
                continue
            return tt
        return "N/A"