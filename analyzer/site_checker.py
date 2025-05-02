```python
   import requests
   from bs4 import BeautifulSoup
   
   class SiteAnalyzer:
       def analyze_site(self, url):
           try:
               response = requests.get(url)
               soup = BeautifulSoup(response.text, 'html.parser')
               
               analysis = {
                   'load_time': response.elapsed.total_seconds(),
                   'has_ssl': url.startswith('https'),
                   'has_meta': bool(soup.find('meta', attrs={'name': 'description'})),
                   'mobile_friendly': self._check_mobile_friendly(soup),
                   'score': 0
               }
               
               analysis['score'] = self._calculate_score(analysis)
               return analysis
           
           except Exception as e:
               return {'error': str(e)}
   
       def _check_mobile_friendly(self, soup):
           viewport = soup.find('meta', attrs={'name': 'viewport'})
           return bool(viewport)
   
│   │       def _calculate_score(self, analysis):
│   │           score = 0
│   │           if analysis['has_ssl']: score += 25
│   │           if analysis['has_meta']: score += 25
│   │           if analysis['mobile_friendly']: score += 25
│   │           if analysis['load_time'] < 2: score += 25
│   │           return score
