from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask import render_template, url_for, redirect, flash, session, request, current_app
from flask_app import app, login_manager
from flask_app.models import *
from flask_app.views.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload
from .views import views_bp # ブループリントをインポート
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import date, timedelta
import os
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

#インデックス
# @auth_bp.route("/")
# def index():
#     return render_template("top.html")
@app.route("/")
def index():
    # create_calendar2024()
    # zaseki = [0,'A','B','C','D','E','F','G','H','I','J']
    # for row in range(1, 11):
    #     for col in range(1, 21):
    #         seat = Seat(Row=zaseki[row], Number=col, ScreenID=3)
    #         db.session.add(seat)
    # db.session.commit()
    # for row in range(1, 11):
    #     for col in range(1, 13):
    #         seat = Seat(Row=zaseki[row], Number=col, ScreenID=2)
    #         db.session.add(seat)
    # db.session.commit()
    # for row in range(1, 8):
    #     for col in range(1, 11):
    #         seat = Seat(Row=zaseki[row], Number=col, ScreenID=1)
    #         db.session.add(seat)
    # db.session.commit()

    # db.session.query(Showing).delete()
    # db.session.commit()

    # Showingテーブルから上映中のMovieIDを取得
    showing_movie_ids = db.session.query(Showing.MovieID).distinct().all()
    showing_movie_ids = [item[0] for item in showing_movie_ids]  # リスト内のタプルを展開

    # 取得したMovieIDリストを使ってMovieテーブルから映画情報を取得
    movies = db.session.query(Movie).filter(Movie.MovieID.in_(showing_movie_ids)).all()
    upcoming_movies = db.session.query(Movie).filter(~Movie.MovieID.in_(showing_movie_ids)).all()
    
    return render_template('top.html',movies=movies, upcoming_movies=upcoming_movies)


#アカウント作成
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        account =Account(Name=form.name.data, KanaName=form.kananame.data, MailAddress=form.mailaddress.data, Password=form.password.data, PhoneNumber=form.phonenumber.data, Birthday=form.birthday.data)
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('signin'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f'Error in {fieldName}: {err}', 'danger')
    return render_template('signup.html', form=form)


#ログインページ
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(Name=form.name.data).first()
        if account and account.Password == form.password.data:
            login_user(account)
            return redirect(url_for('index'))
        else:
            flash('ログインに失敗しました', 'danger')
    return render_template('signin.html', form=form)

#ログアウト
@app.route('/signout')
@login_required
def signout():
    session.clear()
    return redirect(url_for('signin'))


# マイページ
@app.route('/memberinfo', methods=["GET", "POST"])
def memberinfo():
    """ユーザーの個人情報を更新する."""
    # current_user から Account オブジェクトを取得
    user_data = Account.query.filter_by(AccountID=int(current_user.get_id())).first()
    # 予約した情報を取得
    reservations = Reservation.query.filter_by(AccountID=current_user.get_id()).all()
    # アドレステーブルからデータを取得
    address_data = Address.query.filter_by(AccountID=current_user.get_id()).first()
    # 各予約の終了時間を計算
    for reservation in reservations:
        # start_time_str は既に datetime.time 型と仮定
        start_time = reservation.showing.showtime.start_time  
        # datetime.combine を使って datetime オブジェクトに変換
        start_datetime = datetime.combine(datetime.today(), start_time)
        reservation.end_time = (
            start_datetime + timedelta(minutes=reservation.showing.movie.ShowTimes)
        )
        reservation.seat_number = f"{reservation.seat.Row}{reservation.seat.Number}"


    # ログイン済みユーザーかどうかを確認
    if not current_user.is_authenticated:
        flash('このページにアクセスするにはログインしてください。', 'danger')
        return redirect(url_for('signup'))

    form = AccountForm() 
    form2 = AddressForm()

    if request.method == 'GET':
        # フォームにユーザーデータを設定
        form.name.data = user_data.Name
        form.kananame.data = user_data.KanaName
        form.mailaddress.data = user_data.MailAddress
        form.phonenumber.data = user_data.PhoneNumber
        
        # address_data が存在する場合のみフォームにデータを設定
        if address_data:
            # フォームにアドレスデータを設定
            form2.PostNumber.data = address_data.PostNumber
            form2.Todohuken.data = address_data.Todohuken
            form2.Shiku.data = address_data.Shiku
            form2.ChosonNumber.data = address_data.ChosonNumber

    if form.validate_on_submit():
        try:
            # データベースからユーザーデータを取得
            user_data = Account.query.filter_by(AccountID=int(current_user.get_id())).first()

            # ユーザー情報を更新
            user_data.Name = form.name.data
            user_data.kananame = form.kananame.data
            user_data.MailAddress = form.mailaddress.data

            # パスワードが設定されていれば更新
            if form.password.data:
                user_data.password = form.password.data
            user_data.phonenumber = form.phonenumber.data

            print(user_data.Name)
            db.session.commit()
            flash('プロフィールが更新されました。', 'success')

            return redirect(url_for('memberinfo'))  # ホーム画面など適切なページへリダイレクト
        except Exception as e:
            db.session.rollback()
            flash('プロフィールの更新に失敗しました。', 'danger')
            print("Error:", e)  # エラー内容をコンソールに表示

    if form2.validate_on_submit():
        try:
            # データベースからユーザーデータを取得
            address_data = Address.query.filter_by(AccountID=current_user.get_id()).first()
            print("address_data ", address_data)

            if address_data:
                # address_data が存在する場合：更新
                address_data.PostNumber = form2.PostNumber.data
                address_data.Todohuken = form2.Todohuken.data
                address_data.Shiku = form2.Shiku.data
                address_data.ChosonNumber = form2.ChosonNumber.data
            else:
                # address_data が存在しない場合：新規作成
                address_data = Address(
                    PostNumber=form2.PostNumber.data,
                    Todohuken=form2.Todohuken.data,
                    Shiku=form2.Shiku.data,
                    ChosonNumber=form2.ChosonNumber.data,
                    AccountID=current_user.get_id()  # 外部キーを設定
                )
                db.session.add(address_data) 

            db.session.commit()
            flash('アドレス情報が更新されました。', 'success')

            return redirect(url_for('memberinfo'))  # ホーム画面など適切なページへリダイレクト
        except Exception as e:
            db.session.rollback()
            flash('アドレス情報の更新に失敗しました。', 'danger')
            print("Error:", e)  # エラー内容をコンソールに表示

    return render_template('Memberinfo.html', user=current_user, reservations=reservations, form=form, form2=form2)



def save_image(form_picture):
    random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/images/movieimages', picture_fn)

    i = Image.open(form_picture)
    i.save(image_path)

    return picture_fn

#いろいろつくる
@app.route('/seibetutukuru', methods=['GET', 'POST'])
def seibetutukuru():
    seibetu = request.form.get('seibetutukuru')
    capa = request.form.get('capacity')
    agelimit = request.form.get('agelimit')
    movie = request.form.get('movie')
    start_time = request.form.get('start_time')
    kubunmei = request.form.get('kubunmei')
    agelimitdayo = request.form.get('agelimitdayo')
    moviecategory = request.form.get('moviecategory')
    moviecategorydayo = request.form.get('moviecategorydayo')
    cast = request.form.get('cast')
    moviedayo = request.form.get('moviedayo')
    screendayo = request.form.get('screendayo')
    showtimedayo = request.form.get('shottimedayo')
    showdatedayo = request.form.get('showdatedayo')
    moviedesu = request.form.get('moviedesu')
    form = DeleteAllForm()
    delete_movie_form = DeleteMovieForm()  # フォームを作成

    
    md = request.form.get('md')
    ms = request.form.get('ms')
    ov = request.form.get('ov')
    st = request.form.get('st')
    hazime = request.form.get('startdate')
    owari = request.form.get('finishdate')
    
    
    priceplans = request.form.get('priceplans')
    price = request.form.get('price')
    
    discountname = request.form.get('discountname')
    discount = request.form.get('discount')

    
    movie_imagelength = None
    movie_imageside = None

    if 'movie_imagelength' in request.files:
        file = request.files['movie_imagelength']
        movie_imagelength = save_image(file)
        if movie_imageside:
            print(f"ファイルが保存されました: {movie_imagelength}")
        else:
            flash('ファイルの保存に失敗しました。', 'error')

    if 'movie_imageside' in request.files:
        file = request.files['movie_imageside']
        movie_imageside = save_image(file)
        if movie_imageside:
            print(f"ファイルが保存されました: {movie_imageside}")
        else:
            flash('ファイルの保存に失敗しました。', 'error')
    a = request.form.get('a')
    b = request.form.get('b')
    c = request.form.get('c')
    zaseki = [0,'A','B','C','D','E','F','G','H','I','J']
    
    if request.method == 'POST':
        if seibetu:
            seibetu = Sex(Sex=seibetu)
            db.session.add(seibetu)
            db.session.commit()
        if capa:
            capa = Screen(Capacity=capa)
            db.session.add(capa)
            db.session.commit()
        if agelimit:
            agelimit = AgeLimit(AgeLimit=agelimit)
            db.session.add(agelimit)
            db.session.commit()
        if movie:
            movie = Movie(MovieTitle=movie, AgeLimitID=agelimitdayo, MovieCategoryID=moviecategorydayo, MovieImageLength=movie_imagelength, MovieImageSide=movie_imageside, MD=md, MS=ms, Overview=ov, ShowTimes=st, StartDate=hazime, FinishDate=owari)
            db.session.add(movie)
            db.session.commit()

        if moviecategory:
            moviecategory = MovieCategory(CategoryName=moviecategory)
            db.session.add(moviecategory)
            db.session.commit()
        if cast:
            cast = Cast(CastName=cast, MovieID=moviedayo)
            db.session.add(cast)
            db.session.commit()
        if start_time and kubunmei:    
            start_time = datetime.strptime(start_time, '%H:%M').time() 
            showtime = ShowTime(kubunmei=kubunmei, start_time=start_time)
            db.session.add(showtime)
            db.session.commit()
        if priceplans and price:
            price = Price(PricePlans=priceplans, Price=price)
            db.session.add(price)
            db.session.commit()
        if discountname and discount:
            discount = Discount(DiscountName=discountname, Discount=discount)
            db.session.add(discount)
            db.session.commit()

        if delete_movie_form.validate_on_submit():
            print("a")
            movie_id_to_delete = request.form['delete_movie_id']
            try:
                movie_id_to_delete = int(movie_id_to_delete)
                movie = Movie.query.get_or_404(movie_id_to_delete) # Movieオブジェクトを取得
                db.session.delete(movie) # Movieオブジェクトを削除
                db.session.commit()
                flash('映画情報を削除しました', 'success')
            except (TypeError, ValueError):
                flash('無効な映画IDです。', 'danger')
                
        showing = None  # showing変数をif文の外側で定義
        movie_id = request.form.get('moviedesu')
        screen_id = request.form.get('screendayo')
        showdatedayo = request.form.get('showdatedayo')  # 修正: showdatedayo も取得
        showtimedayo = request.form.get('showtimedayo')  # 修正: showtimedayo も取得
        # 型変換と値の確認
        try:
            movie_id = int(movie_id)
            screen_id = int(screen_id)
        except (TypeError, ValueError):
            flash('映画IDとスクリーンIDは数値である必要があります。', 'danger')
            return redirect(url_for('seibetutukuru'))  # エラーがあればフォームへ戻る
        
        if movie_id and screen_id and showdatedayo and showtimedayo:
            showing = Showing(ShowTime=showtimedayo, ShowDate=showdatedayo, MovieID=movie_id, ScreenID=screen_id) 
            print("showing をデータベースに追加します")
            db.session.add(showing)
            db.session.commit()
            flash('上映情報を追加しました。', 'success')
        else:
            flash('必要な情報が選択されていません。', 'danger')

    if a:
        for row in range(1, 11):
            for col in range(1, 21):
                seat = Seat(Row=zaseki[row], Number=col, ScreenID=3)
                db.session.add(seat)
        db.session.commit()
    if b:
        for row in range(1, 11):
            for col in range(1, 13):
                seat = Seat(Row=zaseki[row], Number=col, ScreenID=2)
                db.session.add(seat)
        db.session.commit()
    if c:
        for row in range(1, 8):
            for col in range(1, 11):
                seat = Seat(Row=zaseki[row], Number=col, ScreenID=1)
                db.session.add(seat)
        db.session.commit()

    # 予約テーブルのレコード全消し 佐藤
    # この機能を使うときは、上映テーブルにデータ入れるやつをコメントアウトしないと動かん　治す気力はない　ほかの機能止まったらごめん
    if form.validate_on_submit():
        db.session.query(Reservation).delete()
        db.session.commit()
        return redirect(url_for('seibetutukuru'))

    reservations = Reservation.query.all()
    agelimits = AgeLimit.query.all()
    moviecategorys = MovieCategory.query.all()
    movies = Movie.query.all()
    calendars = Calendar2024.query.all()
    showtimess = ShowTime.query.all()
    screens  = Screen.query.all()

    
    return render_template('seibetutukuru.html', showtimes=showtimess, reservations=reservations, agelimits=agelimits, moviecategorys=moviecategorys, movies=movies, calendars=calendars, screens=screens, form=form, delete_movie_form=delete_movie_form)



app.register_blueprint(views_bp) # ブループリントをアプリケーションに登録

def create_calendar2024():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    delta = end_date - start_date
    
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        if not Calendar2024.query.filter_by(day=day).first():
            calendar_day = Calendar2024(day=day)
            db.session.add(calendar_day)
    
    db.session.commit()
    
# def initialize_database():
#     db.create_all()
#     create_calendar2024()