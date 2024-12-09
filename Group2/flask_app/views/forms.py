from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from wtforms import *
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_app.models import *
from flask_app.views import auth


class SignUpForm(FlaskForm):
    name = StringField('氏名', validators=[DataRequired(), Length(min=2, max=20)])
    kananame = StringField('カナ', validators=[DataRequired()])
    mailaddress = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password')])
    sex = SelectField('性別', coerce=int)
    phonenumber = StringField('電話番号', validators=[DataRequired(), Length(min=6, max=13)])
    birthday = DateField('生年月日', format='%Y/%m/%d')
    submit = SubmitField('サインアップ')

    def validate_password(self, field):
        if field.data == self.name.data:
            raise ValidationError("氏名と同じパスワードは使用できません")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.sex.choices = [(c.SexID, c.Sex) for c in Sex.query.all()]

    
class SigninForm(FlaskForm):
    name = StringField('メールアドレス', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class DeleteAllForm(FlaskForm):
    submit = SubmitField('すべて削除')

class AddressForm(FlaskForm):
    """住所入力フォーム"""
    PostNumber = StringField('郵便番号', validators=[DataRequired(message='郵便番号は必須です'), Length(min=7, max=7, message='7桁の数字を入力してください')])
    Todohuken = StringField('都道府県', validators=[DataRequired(message='都道府県は必須です')])
    Shiku = StringField('市区町村', validators=[DataRequired(message='市区町村は必須です')])
    ChosonNumber = StringField('番地', validators=[DataRequired(message='番地は必須です')])
    submit2 = SubmitField('登録')

class AccountForm(FlaskForm):
    name = StringField('氏名', validators=[DataRequired()])
    kananame = StringField('フリガナ', validators=[DataRequired()])
    mailaddress = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード')  # 入力があれば更新
    phonenumber = TelField('電話番号')
    submit = SubmitField('更新')

class DeleteMovieForm(FlaskForm):
    submit = SubmitField('削除')