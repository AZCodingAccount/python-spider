import requests

url = "https://www.zbj.com/logosjzbj/f.html?fr=zbj.sy.zyyw_1st.lv2&r=2"
response = requests.get(url)
response.text.encoding('utf-8')
print(response.text)
