from flask import Flask,jsonify,render_template,request
from newsapi import NewsApiClient


application=Flask(__name__)
application.config["DEBUG"]=True

newsapi = NewsApiClient(api_key='e598866b388f4780a2a1006f9d58602c')

@application.route('/',methods=['GET'])
def index():
	return app.send_static_file("index.html")

@application.route('/pg1', methods=['GET'])
def getNews():
	top_headlines=newsapi.get_top_headlines(language='en',page_size=30)
	top_cnn=newsapi.get_top_headlines(sources='cnn',language='en')
	top_fox=newsapi.get_top_headlines(sources='fox-news',language='en')
	response={}
	response['top_headlines']=top_headlines
	response['cnn']=top_cnn
	response['fox']=top_fox
	#print(top_headlines)
	return response

@application.route('/stopwords')
def stopwords():
	words={}
	mywordss={}

	stop=set(line.strip() for line in open('stopwords_en.txt'))
	top_headlines=newsapi.get_top_headlines(language='en',page_size=30)
	for ele in top_headlines["articles"]:
		w=ele["title"].split()
		for we in w:
			we.lower()
			if we not in stop:
				words[we]=words.get(we,0)+1
	#print (words)
	res=[[k,v] for k,v in words.items()]
	res.sort(key=lambda x: x[1], reverse=True)
	for i in range(0,30):
		mywordss[res[i][0]]=res[i][1]
	#print(mywordss)
	#p=sorted(words.items(),key=lambda x: x[1], reverse=True)
	return mywordss		

@application.route('/cnn',methods=['GET'])
def getcnn():
	top_cnn=newsapi.get_top_headlines(sources='cnn',language='en')
	#print(top_cnn)
	return top_cnn
@application.route('/fox',methods=['GET'])
def getfox():
	top_fox=newsapi.get_top_headlines(sources='fox-news',language='en')
	#print(top_fox)
	return top_fox

@application.route('/sources/')
def getsource():
	#print("hello boy")
	category=request.args.get('category')
	#print(category)
	if category=="all" or category=="All":
		#print("In IF all")
		top_sources=newsapi.get_sources()
	else:
		#print("In else")
		top_sources=newsapi.get_sources(category=category,language='en')
	return top_sources

@application.route('/everything')
def geteverything():
	category=request.args.get('category')
	source=request.args.get('source')
	from1=request.args.get('from')
	to=request.args.get('to')
	keyword1=request.args.get('keyword')
	#print("In everything")
	if source=="all" or source=="All":
		top_everything=newsapi.get_everything(q=keyword1,from_param=from1,to=to,language='en',sort_by='publishedAt',page_size=30)		
	else:
		top_everything=newsapi.get_everything(q=keyword1,sources=source,from_param=from1,to=to,language='en',sort_by='publishedAt',page_size=30) 
	return top_everything

if __name__=='__main__':
	application.run(debug=True)
	
