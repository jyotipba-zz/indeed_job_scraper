import requests  # to send http request to website
from bs4 import BeautifulSoup  # to parse the website
from collections import Counter # Keep track of term counts
import nltk                      #  # text processing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import sys

#nltk.download()
nltk.data.path.append('./nltk_data/')  # set the path

def get_job_link(job_search_url):
    """
    Given the url for specific job search, this function returns the
     url for all the open position for job search

      Returns:
        urls: a python list of all job posting links
    """
    try:
        source = requests.get(job_search_url).text  # returns the source object
        soup = BeautifulSoup(source, "lxml")
        job_count_div = soup.find(id="searchCount").text # this id tag gives the total number of job published
        job_count_string = job_count_div.split()
        total_job_count = job_count_string[3]  # total number of job posted as this number is needed to find out how many pages are there
        number_of_pages = int(int(total_job_count)/10 ) # as there are 10 job post per page
        main_url = 'https://www.indeed.fi'
        #print(number_of_pages)
        complete_url = []
        partial_url = ''
        for link in soup.find_all('h2', {'class': 'jobtitle'}):
                partial_url = link.a.get('href')   # extract href i.e link to individual job posting
                complete_url.append( main_url+partial_url)

        if number_of_pages > 1:   # if there are more than one pages if job advertising
            start = 10
            for i in range(2, number_of_pages+1):
                #print("https://www.indeed.fi/jobs?q=python+&l=Tampere&start="+str(start))
                source = requests.get(job_search_url+str(start)).text
                soup = BeautifulSoup(source, "lxml")
                for link in soup.find_all('h2', {'class': 'jobtitle'}):
                    partial_url = link.a.get('href')   # extract href i.e limk to individual job posting
                    #print(partial_url)
                    complete_url.append( main_url+partial_url)
                start = 10*i
        return complete_url
    except:
        print("Something wrong with URL. Please check again")
        sys.exit()



def count_words(job_urls):
    """
    Given the list of links to all the job, this function returns the number of occurance of
    key job skill (skill count) in those vacancy.
    """
    word_counter = Counter()  # declaring an empty countet
    for url in job_urls:
        source_each_job = requests.get(url).text
        soup_each_job = BeautifulSoup(source_each_job, "lxml")
        job_description = soup_each_job.find('div', class_ = 'jobsearch-JobComponent-description').get_text()
        stop_words_english = (stopwords.words("english"))
        text = word_tokenize(job_description)
        text = set(text)  # remove the duplicate words
        word_filter = re.compile('^[A-Za-z].*') ## remove punctuation
        #text = ["Mä5", "," ,"D3", "C++" ,"olen", "3", "Jyoti", "@", ".com"]
        raw_words = [word for word in text if word_filter.match(word)]   #returns list of words excluding punctuation
        raw_words = [word.lower() for word in raw_words]
        # remove the stop words
        final_words = [word for word in raw_words if word not in stop_words_english]
        word_counter.update(final_words)  # updating the counter with list of new final words
    skill_counter = Counter({"Angular":word_counter["angular"], "AWS":word_counter["aws"], "JavaScript":word_counter["javascript"],
                        "C++":word_counter["c++"],"HTML":word_counter["html5"] ,"CSS":word_counter["css"],
                        "Azure":word_counter["azure"], "Java":word_counter["java"], "Scala":word_counter["scala"],
                        "Python":word_counter["python"], "Node.js":word_counter["node.js"],"React":word_counter["react"],
                        "Ruby":word_counter["ruby"], "R":word_counter["r"],"Postgres":word_counter["postgresql"],
                        "C":word_counter["c"], "angualar.js":word_counter["angular.js"]} )
    return dict(skill_counter)


def generate_url():
    """
        this function takes the job title and location as user request and
        return the indeed url to search for all the open position for given job.

        returns : job search url as string
    """
    title = input("Please enter job you are looking for e.x software developer \n ")
    location = input ("Enter the location e.x tampere \n ")
    job_title = title.split()
    query_param_job = '+'.join(job_title)
    job_search_url = 'https://www.indeed.fi/jobs?q={}&l={}'.format(query_param_job, location)
    return job_search_url

if __name__ == "__main__":
    job_search_url = generate_url()
    job_urls = get_job_link(job_search_url)
    print(count_words(job_urls))
