from flask import Flask, session, render_template, request, redirect
from requests_oauthlib import OAuth1Session
import requests, json, re

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0')


app.secret_key = '\xe4x\xaf\x7f2\xdbD\xf1t\x8e$5\xb9)\xeb\x93T\xa6D<b\xaa\xe8\x11'

key = 'RxIcW4caInkTyCp8UHrdCDnpuzcan9Qt941WHGU6fAbsPuWWsB'
secret = 'bXtW3zfGdWaJxfioqJsaA4TcnYOvSYflBIobuYqlLvyUpP0kew'

# OAuth URLs given on the application page
request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorization_base_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

def getAuthUrl(callback):
	tumblr = OAuth1Session(key, client_secret=secret, callback_uri=callback)
	tokens = tumblr.fetch_request_token(request_token_url)
	authorization_url = tumblr.authorization_url(authorization_base_url)
	session['prelim_oauth_token'] = tokens['oauth_token']
	session['prelim_oauth_token_secret'] = tokens['oauth_token_secret']
	return authorization_url

# Get the verifier code from the URL
def completeAuth(url):
	print(url)
	tumblr = OAuth1Session(key, client_secret=secret,
		resource_owner_key=session['prelim_oauth_token'],
		resource_owner_secret=session['prelim_oauth_token_secret'])
	tumblr.parse_authorization_response(url)
	tokens = tumblr.fetch_access_token(access_token_url)
	session['oauth_token'] = tokens.get('oauth_token')
	session['oauth_token_secret'] = tokens.get('oauth_token_secret')

def getProtectedResource(url):
	tumblr = OAuth1Session(key, client_secret=secret,
		resource_owner_key=session['oauth_token'],
		resource_owner_secret=session['oauth_token_secret'])
	return json.loads(tumblr.get(url).text)

def getUnprotectedResource(url):
	r = requests.get(url)
	return json.loads(r.text)

@app.route('/search')
@app.route('/')
def index():
	blog=request.args.get('blog','')
	tag=request.args.get('tag','')
	if 'auth' in session and session['auth']:
		name = getProtectedResource('https://api.tumblr.com/v2/user/info')['response']['user']['name']
		return render_template('rumblr.html', auth=session['auth'], name=name, blog=blog, tag=tag)
	return render_template('rumblr.html', authurl=getAuthUrl('http://rumblr.brandonksides.com/auth'), auth=False, blog=blog, tag=tag)

@app.route('/auth')
def auth():
	completeAuth(request.url)
	session['auth'] = True;
	return redirect('/', code=303)

@app.route('/logout')
def logout():
	if 'auth' in session and session['auth']:
		session['auth'] = False;
	return redirect('/', code=303)

@app.route('/query/search')
def searchQuery():
	offset = 0
	allresults=[]
	blog=request.args.get('blog','')
	tag=request.args.get('tag','')
	if blog:
		if tag:
			results=getUnprotectedResource('https://api.tumblr.com/v2/blog/'+blog+'.tumblr.com/posts/audio?api_key='+key+'&tag='+tag)['response']['posts']
		else:
			results=getUnprotectedResource('https://api.tumblr.com/v2/blog/'+blog+'.tumblr.com/posts/audio?api_key='+key)['response']['posts']
	else:
		results = None
	allresults += results
	offset = len(allresults)
	while results:	
		if blog:
			if tag:
				results=getUnprotectedResource('https://api.tumblr.com/v2/blog/'+blog+'.tumblr.com/posts/audio?api_key='+key+'&tag='+tag+"&offset="+str(offset))['response']['posts']
			else:
				results=getUnprotectedResource('https://api.tumblr.com/v2/blog/'+blog+'.tumblr.com/posts/audio?api_key='+key+"&offset="+str(offset))['response']['posts']
		else:
			results = None
		allresults += results
		offset = len(allresults)
	tumblr_pattern=re.compile('https://www.tumblr.com.*')
	if allresults:
		for result in allresults:
			if 'audio_url' in result and result['audio_url'] and tumblr_pattern.match(result['audio_url']):
				result['audio_url'] = "http://a.tumblr.com/"+ result['audio_url'].split('/')[len(result['audio_source_url'].split('/'))-1] + "o1.mp3"
			if not 'album_art' in result or not result['album_art']:
				result['album_art'] = "/static/assets/coverartnotfound.png"
	return json.dumps(allresults)