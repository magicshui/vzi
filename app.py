#coding: utf-8
import config
from config import *
from flask import Flask,render_template
import utils
from utils import *


app = Flask(__name__)
app.debug=True
app.secret_key='@#$@#$DFFSWEFSDsdfasdfqew!312x1'

@app.route('/oauth')
def route_oauth():
    movie=dbSession.query(Movie,Lines).filter(Movie.id==Lines.movie_id).order_by(func.rand()).first()
    WeiboClient = APIClient(app_key = Weibo_APP_KEY,app_secret=Weibo_APP_SECRET,
        redirect_uri=Weibo_CALLBACK_URL)
    url_weibo=WeiboClient.get_authorize_url()
    return render_template('oauth.html',weibo_url=url_weibo,movie=movie)

@app.route('/od')
def route_oauth_douban_to_for_sys():
    Doubanclient = DoubanClient(Douban_APP_KEY, Douban_APP_SECRET,Douban_CALLBACK_URL, 'movie_basic_r,douban_basic_common')
    return redirect(Doubanclient.authorize_url)
        
@app.route('/oauth/back/douban')
def route_oauth_douban():
    code = request.args.get('code')
    Doubanclient = DoubanClient(Douban_APP_KEY, Douban_APP_SECRET,Douban_CALLBACK_URL, 'movie_basic_r,douban_basic_common')
    Doubanclient.auth_with_code(code)
    dbSession=db_session()
    #return str(Doubanclient.client.token)
    rx=dbSession.query(SysInfo).all()
    for  x in rx:
        dbSession.delete(x)
        dbSession.commit()
    s=SysInfo(douban=Doubanclient.client.token)
    dbSession.add(s)
    dbSession.commit()
    Doubanclient.auth_with_token(Doubanclient.client.token)
    return 'ok'
        
@app.route('/oauth/back/weibo')
def route_oauth_weibo():
    code = request.args.get('code')
    client = APIClient(app_key = Weibo_APP_KEY,app_secret=Weibo_APP_SECRET,
    redirect_uri=Weibo_CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client.set_access_token(access_token,expires_in)
    result=client.get.users__show(uid=r.uid)
    if 'name' in session and 'come' in session:
        return redirect('/')
    session['name']=result.name
    session['come']='sina'
    if not dbSession.query(User).filter(User.name==result.name).all():
        return redirect('/')
    _user= User(name=result.name,come='sina',avatar=result.profile_image_url)
    dbSession=db_session()
    dbSession.add(_user)
    dbSession.commit()
    dbSession.flush()
    session['avatar']=result.profile_image_url
    return redirect('/')

@app.route('/')
def route_index():
    if 'name' in session and 'come' in session:
        dbSession=db_session()
        movie=dbSession.query(Movie,Lines).filter(Movie.id==Lines.movie_id).order_by(func.rand()).first()
        dbSession.flush()
        return render_template('index.html',movie=movie)
    
    return redirect('/oauth')
    
def _get_movie_from_douban(id):
    try:
        Doubanclient = DoubanClient(Douban_APP_KEY, Douban_APP_SECRET,Douban_CALLBACK_URL, 'movie_basic_r,douban_basic_common')
        dbSession=db_session()
        r_=dbSession.query(SysInfo).first()
        Doubanclient.auth_with_token(r_.douban)
        data=Doubanclient.movie.get(id)
        movie = Movie(id=id,title=data['title'],alt_title=data['alt_title'],
        image=data['image'],alt=data['alt'],summary=data['summary'])
        return movie
    except Exception,e:
        raise
        return None
        
        
@app.route('/',methods=['POST'])
def route_search():
    _q=request.form['q']
    dbSession=db_session()
    if not dbSession.query(Movie).filter(Movie.id==_q).all():
        movie=_get_movie_from_douban(_q)
        if movie!=None:
            dbSession=db_session()
            dbSession.add(movie)
            dbSession.commit()
            dbSession.flush()
            return render_template('movie.html',movie=movie,lines='')
        else:
        
            res=_search_movie_and_lines(_q)
            return render_template('search.html',res=res)

    else :
        res=_search_movie_and_lines(_q)

        return render_template('search.html',res=res)

@app.route('/movie/<string:id>',methods=['GET'])
def route_get_movie_with_id(id):
    dbSession=db_session()
    movie=dbSession.query(Movie).filter(Movie.id==id).first()
    lines=dbSession.query(Lines).filter(Lines.movie_id==id).all()
    dbSession.flush()
    return render_template('movie.html',movie=movie,lines=lines)

@app.route('/movie/back',methods=['GET'])
def route_movie_background():
    dbSession=db_session()
    movie=dbSession.query(Movie).filter(Movie.back=='').all()
    dbSession.flush()
    return render_template('back.html',res=movie)
    
@app.route('/movie/<string:id>/back',methods=['POST'])
def route_movie_background_up(id):
    cut = request.files['back']
    movie=dbSession.query(Movie).filter(Movie.id==id).first()
    _save_path=os.path.join(UPLOAD_FOLDER_BACK, movie.id+'.'+cut.filename.split('.')[-1])
    movie.back="http://movie.shui.us/static/back/"+movie.id+'.'+cut.filename.split('.')[-1]
    dbSession.commit()
    return redirect('/movie/back')
     
@app.route('/movie/<string:movie_id>/lines',methods=['POST'])
def route_leave_a_line(movie_id):
    cut = request.files['cut']
    _line=Lines(content=request.form['content'],movie_id=movie_id,cut=cut.filename.split('.')[-1])
    _save_path=os.path.join(UPLOAD_FOLDER, _line.id+'.'+cut.filename.split('.')[-1])
    cut.save(_save_path)
    dbSession=db_session()
    dbSession.add(_line)
    dbSession.commit()
    dbSession.flush()
    return redirect('/movie/%s'%movie_id)
def _search_movie_and_lines(q):
    dbSession=db_session()
    res=dbSession.query(Movie,Lines).filter(Lines.movie_id==Movie.id).filter(or_(Movie.id==q,or_(Lines.content.like('%'+q+'%'),or_(Movie.title.like('%'+q+'%'),Movie.alt_title.like('%'+q+'%'))))).all()

    return res 

@app.route('/movie/<string:movie_id>/lines/<string:id>')
def route_one_line(movie_id,id):
    dbSession=db_session()
    movie=dbSession.query(Movie).filter(Movie.id==movie_id).first()
    line=dbSession.query(Lines).filter(Lines.id==id).first()
    dbSession.flush()
    return render_template('line.html',movie=movie,line=line)

@app.route('/logout')
def route_logout():
    session.clear()
    return redirect('/')
