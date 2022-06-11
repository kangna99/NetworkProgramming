import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def scrapping():
    url = 'https://sites.google.com/view/davidchoi/home/members'
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    elements = soup.select_one(
        '#yDmH0d > div:nth-child(1) > div > div:nth-child(2) > div.QZ3zWd > div > div.UtePc.RCETm.SwuGbc')
    # select img tag
    imgs = elements.select('section > div > div > div > div > div > div > div > div > div > div > img')
    # select description
    contents = elements.select('section > div > div > div > div > div > div > div > div > div > p')
    dataList = []

    # for image index number
    index = 0
    # in for loop if name_flag is False, save as name data
    # if name_flag is True, save as research data
    flag = False

    for content in contents:
        if content.text == '':
            continue

        if not flag:
            name = content.text.split('(')[0].strip()
            bracket = content.text.split('(')[1].split(')')[0]
            job_role = bracket.split(',')[0]
            start_year = bracket.split(',')[1].split('-')[0].strip()
            try:
                end_year = bracket.split(',')[1].split('-')[1]
                if not end_year:
                    end_year = 'NA'
            except IndexError:
                end_year = start_year
            flag = True
            continue
        else:
            body = content.text
            research_interest = 'NA'
            current_job_role = 'NA'
            try:
                # for Current Members
                if "Research Interests" in body:
                    research_interest = body.split(':')[1].strip()
                    if not research_interest:
                        research_interest = 'NA'
                # for Alumnies
                if "@" in body:
                    current_job_role = body.strip()
            except IndexError:
                print("list index out of range")

            # select picture url by index
            profile_pic_url = imgs[index]['src']
            if not profile_pic_url:
                profile_pic_url = 'NA'

            data = [name, job_role, start_year, end_year, research_interest, current_job_role, profile_pic_url]
            dataList.append(data)
            flag = False
            index += 1
            continue

            # make list to dataframe
    df = pd.DataFrame(dataList,
                      columns=['name', 'job_role', 'start_year', 'end_year', 'research_interest', 'current_job_role',
                               'profile_pic_url'])
    # print(df)
    # make dataframe to csv file
    df.to_csv('./problem2_csv.csv', mode='w')


if __name__ == '__main__':
    print('Scraping Data...')
    scrapping()
    print('Complete scrapping in \'problem2_csv.csv\' file')
