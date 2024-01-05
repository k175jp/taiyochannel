import os
from fastapi import FastAPI, Depends, Query, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Column, TIMESTAMP, Integer, String, create_engine, text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import subprocess
import shutil
import json
import magic
import base64
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


ROOT_PATH="/api"
PATH = '/app/image'
TMP = '/app/tmp'

app = FastAPI()

SQLALCHEMY_DATABASE_URI = 'mariadb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        os.environ.get("DB_USER"),
        os.environ.get("DB_PASSWORD"),
        os.environ.get("DB_HOST"),
        os.environ.get("DB_PORT"),
        os.environ.get("DB_NAME")
    )

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=5)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session():
    db = Session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key = True, nullable=False)
    user_name = Column(String(25), nullable=False)
    explain = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Thread(Base):
    __tablename__ = "thread"
    thread_id = Column(Integer, primary_key=True, nullable=False)
    thread_name = Column(String(50), nullable=False)

class Content(Base):
    __abstract__ = True
    content_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=current_timestamp())
    text = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=True)

def get_model(thread_id):
    classname = 'Thread' + str(thread_id)
    tablename = 'thread' + str(thread_id)

    attrs = {'':'', '__tablename__': tablename, '__table_args__' : {'extend_existing': True}}
    NewClass = type(classname, (Content,), attrs)
    return NewClass

Base.metadata.create_all(bind=engine)

def init():
    db = Session()
    if not db.query(User).filter(User.user_name=="admin").filter(User.email =="admin@taiyochannel.com").first():
        for i in range(5):
            thread = Thread(
                thread_name = f"test{i}"
            )
            db.add(thread)
            db.commit()
            db.flush()
            NewClass = get_model(thread.thread_id)
            Base.metadata.create_all(bind=engine, tables=[NewClass.__table__])
            new = NewClass(
                user_id = 1,
                text = f"test{i}"
            )
            db.add(new)
        user = User(
        user_id = 1,
        user_name = "admin",
        explain = "i am admin",
        email = "admin@taiyochannel.com",
        password = "adminpass"
        )
        db.add(user)
        db.commit()
try:
    init()
except:
    pass

class signinRequest(BaseModel):
    email: str = Query(..., max_length=255)
    password: str = Query(..., max_length=255)

class signupRequest(BaseModel):
    userName: str = Query(..., max_length=25)
    email: str = Query(..., max_length=255)
    password: str = Query(..., max_length=255)

class getProfileRequest(BaseModel):
    myUserId: int
    userId: int

class updateProfileRequestu(BaseModel):
    userId: int
    formContent: str = Query(..., max_length=25)
    password: str = Query(..., max_length=255)

class updateProfileRequestex(BaseModel):
    userId: int
    formContent: str = Query(..., max_length=255)
    password: str = Query(..., max_length=255)

class updateProfileRequestem(BaseModel):
    userId: int
    formContent: str = Query(..., max_length=255)
    password: str = Query(..., max_length=255)

class updateProfileRequestp(BaseModel):
    userId: int
    formContent: str = Query(..., max_length=255)
    password: str = Query(..., max_length=255)

class newThreadRequest(BaseModel):
    threadName: str = Query(..., max_length=50)
    text: str = Query(..., max_length=255)
    userId: int

class postContentRequest(BaseModel):
    text: str = Query(..., max_length=255)
    user_id: int

class postContentRequestWithFile(BaseModel):
    text: str=Query(..., max_length=255)
    user_id: int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

@app.post('%s/signin' % ROOT_PATH)
def signin(request:signinRequest, db: Session = Depends(session)):
    user = db.execute(text("SELECT * FROM user WHERE email = '%s' AND password = '%s'" % (request.email, request.password))).first()
    if user:
        response_body = jsonable_encoder({"status":"ok", "userId" : user.user_id})
    else:
        response_body = jsonable_encoder({"status": "error", "content": "認証に失敗しました"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/signup' % ROOT_PATH)
def signup(request: signupRequest, db: Session = Depends(session)):
    result_set = db.query(User).filter(User.email == request.email).first()
    if result_set is None:
        user = User(
            user_name = request.userName,
            email = request.email,
            password = request.password
        )
        db.add(user)
        db.commit()
        response_body = jsonable_encoder({"status":"ok"})
    else:
        response_body = jsonable_encoder({"status":"error", "content": "メールアドレスはすでに使用されています"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/profile' % ROOT_PATH)
def get_profile(request: getProfileRequest, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).first()
    if user:
        if request.myUserId == request.userId:
            response_body = jsonable_encoder({"status":"ok", "userName":user.user_name, "explain":user.explain,"email":user.email, "password":user.password})
        else:
            response_body = jsonable_encoder({"status":"ok", "userName":user.user_name, "explain":user.explain})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"ユーザを取得できませんでした"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/update_profile/userName' % ROOT_PATH)
def update_profile(request: updateProfileRequestu, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).filter(User.password == request.password).first()
    if user:
        user.user_name = request.formContent
        db.commit()
        response_body = jsonable_encoder({"status":"ok"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"パスワードが間違っています"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/update_profile/explain' % ROOT_PATH)
def update_profile(request: updateProfileRequestex, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).filter(User.password == request.password).first()
    if user:
        user.explain = request.formContent
        db.commit()
        response_body = jsonable_encoder({"status":"ok"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"パスワードが間違っています"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/update_profile/email' % ROOT_PATH)
def update_profile(request: updateProfileRequestem, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).filter(User.password == request.password).first()
    if user:
        user.email = request.formContent
        db.commit()
        response_body = jsonable_encoder({"status":"ok"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"パスワードが間違っています"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/update_profile/password' % ROOT_PATH)
def update_profile(request: updateProfileRequestp, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).filter(User.password == request.password).first()
    if user:
        user.password = request.formContent
        db.commit()
        response_body = jsonable_encoder({"status":"ok"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"パスワードが間違っています"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.get('%s/thread/{thread_id}' % ROOT_PATH)
def get_thread(thread_id: int, db: Session = Depends(session)):
    thread = db.query(Thread).filter(Thread.thread_id == thread_id).first()
    if thread:
        ThreadContent = get_model(thread_id)
        contents = db.query(ThreadContent).all()
        data = []
        for content in contents:
            user = db.query(User).filter(User.user_id == content.user_id).first()
            if content.filename:
                img = open(f"{PATH}/{content.filename}", "rb").read()
                b64_img = base64.b64encode(img).decode('utf-8')
                data.append({'content_id':content.content_id, 'user_id':content.user_id, 'user_name':user.user_name, 'created_at': content.created_at, 'text':content.text, 'img':b64_img})
            else:
                data.append({'content_id':content.content_id, 'user_id':content.user_id, 'user_name':user.user_name, 'created_at': content.created_at, 'text':content.text})
        response_body = jsonable_encoder({"status":"ok", "list":data, 'threadName':thread.thread_name})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"スレッドが存在しません"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/thread/{thread_id}' % ROOT_PATH)
def new_content(request: postContentRequest, thread_id: int, db: Session = Depends(session)):
    print(request.user_id)
    user = db.query(User).filter(User.user_id == request.user_id).first()
    if user:
        thread = db.query(Thread).filter(Thread.thread_id == thread_id).first()
        if thread:
            ThreadContent = get_model(thread_id)
            content = ThreadContent(
                user_id = request.user_id,
                text = request.text
            )
            db.add(content)
            db.commit()
            response_body = jsonable_encoder({"status":"ok"})
        else:
            response_body = jsonable_encoder({"status":"error", "content":"スレッドが存在しません"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"ユーザを取得できませんでした"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/threadWithFile/{thread_id}' % ROOT_PATH)
def new_content(file: UploadFile = File(...), user_id: int = 0, thread_id: int = 0, text: str = Query(..., max_lenght=255), db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        thread = db.query(Thread).filter(Thread.thread_id == thread_id).first()
        if thread:
            ThreadContent = get_model(thread_id)
            path_tmp = f'{TMP}/{file.filename}'
            with open(path_tmp, 'w+b') as buf:
                shutil.copyfileobj(file.file, buf)
            mime = magic.from_file(path_tmp, mime=True).split('/')
            if  mime[0] == "image" and (mime[1] == "jpeg" or mime[1] == "gif" or mime[1] == "png") :
                ret = subprocess.run(fr'/app/file.sh "{file.filename}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
                if ret.stderr == '':
                    filename = ''.join(ret.stdout.splitlines())
                    path = f'{PATH}/{filename}'
                    img = Image.open(path_tmp)
                    if img.height > 700:
                        img_resized = img.resize((700, 700 * img.height // img.width),resample=Image.LANCZOS)
                        img_resized.save(path, quality=90)
                    else:
                        shutil.move(f'{path_tmp}', path)
                    content = ThreadContent(
                        user_id = user_id,
                        text = text,
                        filename = filename
                    )
                    db.add(content)
                    db.commit()
                    response_body = jsonable_encoder({"status":"ok", "filename":path})
                else:
                    response_body = jsonable_encoder({"status":"error", "content":ret.stderr})
            else :
                response_body = jsonable_encoder({"status":"error", "content":"ファイルが追加できません", "mime":mime})
        else:
            response_body = jsonable_encoder({"status":"error", "content":"スレッドが存在しません"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"ユーザを取得できませんでした"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.post('%s/new_thread' % ROOT_PATH)
def new_thread(request: newThreadRequest, db: Session = Depends(session)):
    user = db.query(User).filter(User.user_id == request.userId).first()
    if user:
        if request.text:
            thread = Thread(
                thread_name = request.threadName
            )
            db.add(thread)
            db.commit()
            db.flush()
            NewClass = get_model(thread.thread_id)
            Base.metadata.create_all(bind=engine, tables=[NewClass.__table__])
            new_thread = NewClass(
                user_id = request.userId,
                text = request.text
            )
            db.add(new_thread)
            db.commit()
            response_body = jsonable_encoder({"status":"ok", "id":thread.thread_id})
        else:
            response_body = jsonable_encoder({"status":"error", "content":"本文が入力されていません"})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"ユーザを取得できませんでした"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)

@app.get('%s/search' % ROOT_PATH)
def get_thread_list(threadname : str = Query(..., max_length=50), db: Session = Depends(session)):
    thread = db.query(Thread).filter(Thread.thread_name.like(f"%{threadname}%")).all()
    if thread:
        response_body = jsonable_encoder({"status":"ok", "list":thread})
    else:
        response_body = jsonable_encoder({"status":"error", "content":"検索にヒットするスレッドが存在しません"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)