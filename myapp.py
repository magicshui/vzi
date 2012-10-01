#coding: utf-8
__author__ = 'Arthur'
__email__ ='shuiyuzhe@gmail.com'

from flask import Flask,render_template

app = Flask(__name__)

# this is the inde page
# in this page
# you can see:
#    1 movie and its'info
#    2 three lines
# and a search comment
@app.route('/',methods = ['GET'])
def route_index():

    return render_temlate(one_movie=one_movie,three_lines=three_lines)

# when the user search
# there some situtations
#    1 search douban movie url,if not exists create to page
#    2 search movie names ,if not exists create to page
#    3 search lines , if not exists no
@app.route('/',methods = ['POST'])
def route_inde_post():
    pass

# show one movie and its info
# while show this:
# the movie info
# the lines
@app.route('/movie/<string:id>',methods = ['GET'])
def route_movie():
    return render_template('',one_movie=one_movie,all_lines=all_lines)


@app.route('/movie/',methods=['POST'])
def route_movie_post():
    return render_tempalte('')

def _id_gen():
    return md5.md5(str(datetime.now())).hexgiest()

class Lines():
    __tablename__='lines_list'
    name =Cloumn(String(200))
    avatar = Column(String(200))
    cut = Column(String(200))
    line_id = Column(String(30),primary_key = True)
    crt_time = Column(DateTime)

    def __init__(self,name,avart,cut,content,movie_id):
        self.name = name
        self.avart = avart
        self.line_id = id_gen()
        pass
class Comment():
    def __init__(self,name,img,content,crt_time,line_id):
        pass



class Movie():
    def ana(self,content):
        import json
        _json_data = json.loads(content)
        self.title = _json_data['title']
        self.alt_title = _json_data['alt_title'] or '';
        self.image = _json_data['image']
        self.summary = _json_data['summary']
        self.alt = _json_data['alt']
        self.source_data=content



def route_to_oauth():
            client  = APIClient(app_key = APP_KEY,app_secret=APP_SECRET,
                redirect_uri=CALLBACK_URL)
            url = client.get_authorize_url()
            return render_template('gotoauth.html',url=url)

def route_come_from_weibo():
        code = request.args.get('code')
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        session['token']=access_token
        session['expire']=expires_in
        t=TokenListInfo(time=datetime.now(),token=access_token,
            expire=expires_in,level='infoq')
        db_session=sessionmaker(bind=DB)
        dbSession=db_session()
        dbSession.add(t)
        dbSession.commit()
        return redirect('index')



# get movie info from douban
def _get_movie_from_douban(id):
    _base_url = 'http://api.douban.com/v2/movie/%s'%id
    import requests
    _orignal_source = requests.get(_base_url)
    movie = Movie()
    movie.ana(_orignal_source)
    return movie

# get movie from db
def _get_movie_from_db(id):
    movie=db_session.query(Movie).filter(Movie.id==id).all()
    if movie:
        return movie[0]
    else:
        return None

# get movie from
def _get_movie_from_db_with_query(id):
    movie=db_session.query(Movie).filter(or_(Movie.title.like("%"+id+"%"),Movie.alt_title.like('%'+id+'%'))).all()
    return movie


# show one lines all comments
# it comes with the ajax requests
# so it not render html template file
@app.route('/lines/commets/<string:id>',methods=['GET'])
def route_lines_comment():
    return render_template('',all_comments=all_comments)


# add a comment to a line
# ajax post content and line id
@app.route('/lines/comments/<string:id>',methods=['POST'])
def route_lines_comment_post():
    pass

if __name__ == "__main__":
    app.run()