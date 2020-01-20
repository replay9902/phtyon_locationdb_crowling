from urllib.request import urlopen
from bs4 import BeautifulSoup
import math, csv, os, re, time


# 마지막 페이지 구하기
listUrl = 'http://location.jjfc.or.kr/home/?doc=location/list.php'
html = urlopen(listUrl).read()
soup = BeautifulSoup(html, 'html.parser')

span = soup.select('span.extra02')[1]
total = int(span.text)

page = 1
lastPage = math.ceil(total / 10)


#목록페이지에서 뷰페이지 링크 구하기
linkList = []
while page <= lastPage:
    url = 'http://location.jjfc.or.kr/home/?doc=location/list.php&page=' + str(page)
    # print(url)
    
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    list = soup.select('.lo_content')
    
    for i in list:

        b = i.b
        if b != None:
            
            link = b.a['href']

            if link not in linkList:
                linkList.append(link)

    page += 1


#뷰페이지에서 로케이션 정보와 사진 파일 정보 가져와서 저장하기
DB = []
baseViewUrl = 'http://location.jjfc.or.kr/home/'
imgPath = './jjfc/'

for i in linkList:
    url = baseViewUrl + i
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    data = soup.select('.lo_view_txt3')
   
    temp = []
    
    #url에서 게시물 lo_id값 구하기
    regex = re.compile(r'lo_id=[0-9]+')
    match = regex.search(i)
    if match != None:
        match_text = match.group()
        lo_id = match_text.replace("lo_id=", "")
    else:
        lo_id = 0
         


    #동영상 주소 구하기
    video_data = soup.select_one('#view_3 iframe[src]')
    # print(len(video_data))
    if video_data != None:
        video_src = video_data['src'].strip()
    else:
        video_src = ''

    

    temp.append(lo_id)
    temp.append(data[0].text.strip())
    temp.append(data[1].text.strip())
    temp.append(data[2].text.strip())
    temp.append(data[3].text.strip())
    temp.append(video_src)
    DB.append(temp)
    print(temp)


    ##이미지 정보 저장하기
    # img_data = soup.select('.img_width01>img')
    # if len(img_data) > 0:
    #     try:
    #         os.mkdir(imgPath + lo_id)
    #     except FileExistsError as e:
    #         print(e)

    #     for img in img_data:
    #         imgFileName = os.path.basename(img['src'])
    #         imgUrl = baseViewUrl +img['src']
    #         with urlopen(imgUrl) as f:
    #             with open(imgPath + lo_id + '/' + imgFileName, 'wb' ) as h:
    #                 _img = f.read()
    #                 h.write(_img)
        
    #         print(imgFileName)
    time.sleep(1)
    


#csv 저장
# with  open('jjfc.csv', 'w', encoding='utf-8', newline='') as f:
#     csvWriter = csv.writer(f)
#     csvWriter.writerow(['id', 'title', 'cate', 'location', 'introduce', 'video'])
#     csvWriter.writerows(DB)

    
print('완료되었습니다.')


