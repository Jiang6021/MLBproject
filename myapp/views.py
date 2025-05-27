from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
#from myapp.models import student


#from datetime import datetime
# Create your views here.
def sayhello(request):
    return HttpResponse("hello!")
def homepage(request):
    return render(request, 'index.html')
'''
def listone(request):
    try:
        unit = student.objects.get(cName="luna") #讀取一筆資料
    except:
        errormessage = "(讀取錯誤！)"
    return render(request, "listone.html", locals())

def listall(request):
    students = student.objects.all().order_by('id')  #讀取
    return render(request, "listall.html", locals())
'''
def index(request):
    return HttpResponse("這是首頁 index")

#%% (爬運彩報馬仔的靜態網頁)

from bs4 import BeautifulSoup

def get_era_from_lottonavi(request):
    url = "https://www.lottonavi.com/player/mlb/808967/yoshinobu-yamamoto/game-logs/"
    headers = {'User-Agent': 'Mozilla/5.0'} 
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select('table tbody tr')[:5]

    labels = []
    values = []

    for row in rows:
        tds = row.find_all('td')
        ths = row.find_all('th')
        if ths and tds:
            date = tds[0].text.strip()  # 日期
            era = ths[-1].text.strip()
            try:
                labels.append(date)
                values.append(float(era))
            except ValueError:
                continue  # 有可能 ERA 是 '-' 代表未出賽或資料缺失

    return JsonResponse({'labels': labels[::-1], 'values': values[::-1]})  # 反轉顯示最新在右
#前端 JavaScript（Chart.js）用 AJAX 抓資料時，只能處理 JSON 格式。
#%% 報馬仔失敗改用mlb api抓近五場era
def get_era_from_mlb(request):
    player_id = 808967  # 山本由伸
    season = 2025
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&group=pitching&season={season}"
    
    response = requests.get(url, timeout=5)
    data = response.json()

    games = data['stats'][0]['splits']
    latest_games = games[-5:]  # 最後五場（若是倒序，則改 games[:5]）
    
    labels = []
    values = []

    for game in latest_games:
        date = game['date']
        era_str = game['stat'].get('era', None)
        try:
            era = float(era_str)
            labels.append(date[5:])  # e.g. "05-08"
            values.append(era)
        except (TypeError, ValueError):
            continue

    return JsonResponse({
        'labels': labels,
        'values': values,
        'latest_era': values[-1] if values else 0.0,
        'latest_whip': float(game['stat'].get('whip', 0.0)),
        'latest_k9': float(game['stat'].get('strikeoutsPer9Inn', 0.0))
    })
#%%
def get_pitcher_win_loss(request):
    player_id = 808967  # 山本由伸
    season = 2025
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&group=pitching&season={season}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        games = data['stats'][0]['splits']
    except Exception as e:
        return JsonResponse({'error': f'資料讀取錯誤：{str(e)}'}, status=500)

    wins = 0
    losses = 0

    for game in games:
        stat = game['stat']
        wins += int(stat.get('wins', 0))
        losses += int(stat.get('losses', 0))

    return JsonResponse({
        'wins': wins,
        'losses': losses,
    })
