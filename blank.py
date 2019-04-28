#!/usr/bin/env python
#coding:utf-8
#tested in win


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String(8),unique=True,nullable=False)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'

class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer,primary_key=True)
    name = Column(String(16),unique=True,nullable=False)

    def __repr__(self):
        return f'<{self.id} : {self.name}>'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    email = Column(String(64),unique=True,nullable=False)
    name = Column(String(15),unique=True,nullable=False)

    def __repr__(self):
        return f'<{self.name} : {self.email}>'

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer,primary_key=True)
    timestamp = Column(String(100))
    title = Column(String(64),nullable=False)
    link = Column(String(1000),nullable=False)
    tag_id = Column(String(20),ForeignKey('tags.id'),nullable=False)
    tag = relationship('Tag',backref='articles')
    src_id = Column(String(20),ForeignKey('sources.id'),nullable=False)
    src = relationship('Source',backref='articles')
    user_id = Column(String(20),ForeignKey('users.id'),nullable=False) 
    user = relationship('User',backref='articles')

    def __repr__(self):
        return f'<{self.title} : {self.tag.name} : {self.user.name}>'


class db():
    def __init__(self,dbfile):
        engine = create_engine(r'sqlite:///'+dbfile)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()        

    def query_tagid(self,tagname):
        return self.session.query(Tag).filter_by(name=tagname).first().id

    def query_userid(self,username):
        return self.session.query(User).filter_by(name=username).first().id

    def query_srcid(self,sourcename):
        return self.session.query(Source).filter_by(name=sourcename).first().id

    def query_article(self,title):
        return self.session.query(Article).filter_by(title=title).all()

    def insert_article(self,article_dict):
        timestamp = article_dict['timestamp']
        title = article_dict['title']
        tagid = self.query_tagid(article_dict['tag'])
        userid = self.query_userid(article_dict['user'])
        link = article_dict['link']
        src_id = self.query_srcid(article_dict['source'])
        article = Article(timestamp=timestamp,title=title,tag_id=tagid,user_id=userid,link=link,src_id=src_id)
        self.session.add(article)
        self.session.commit()


def test(session):
    # test case
    tag1 = Tag(name='GgG')
    tag2 = Tag(name='t2')  
    u1 = User(email='u1@h.com',name='u1')
    u2 = User(email='u2@h.com',name='u2')
    s1 = Source(name='wx')
    s2 = Source(name='mm')

    for x in [tag1,tag2,u1,u2,s1,s2]:
        session.add(x)
    session.commit()
    t = session.query(Tag).all()
    print(t)
    u = session.query(User).all()
    print(u)
    s = session.query(Source).all()
    print(s)

    atid = session.query(Tag).filter_by(name='GgG').first().id
    auid = session.query(User).filter_by(name='u1').first().id
    asid = session.query(Source).filter_by(name='wx').first().id
    a1 = Article(timestamp=func.now(),title='a1',tag_id=atid,user_id=auid,link='111',src_id=asid)

    atid = session.query(Tag).filter_by(name='t2').first().id
    auid = session.query(User).filter_by(name='u2').first().id
    asid = session.query(Source).filter_by(name='mm').first().id
    a2 = Article(timestamp=func.now(),title='a2',tag_id=atid,user_id=auid,link='222',src_id=asid)

    atid = session.query(Tag).filter_by(name='t2').first().id
    auid = session.query(User).filter_by(name='u1').first().id
    asid = session.query(Source).filter_by(name='wx').first().id
    a3 = Article(timestamp=func.now(),title='a3',tag_id=atid,user_id=auid,link='333',src_id=asid)

    for x in [a1,a2,a3]:
        session.add(x)
    session.commit()
    a = session.query(Article).all()
    print(a)

    a1 = session.query(Article).filter_by(title='a1').first()
    print(a1.tag.name)
    print(a1.user.name)
    print('='*10)

    u1 = session.query(User).filter_by(name='u1').first()
    al = u1.articles
    for x in al:
        print(x.title)
    print('='*10)

    t2 = session.query(Tag).filter_by(name='t2').first()
    for x in t2.articles:
        print(x.title)
    print('='*10)

    wx = session.query(Source).filter_by(name='wx').first()
    for x in wx.articles:
        print(x.title)

if __name__ == "__main__":
    import os
    dbfile = r'E:\test.db'
    # os.remove(dbfile)

    # engine = create_engine(r'sqlite:///'+dbfile)
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # Base.metadata.create_all(engine)  # create table

    # test(session)

    # tag3 = Tag(name='gesgs') 
    # session.add(tag3)
    # session.commit()
    # t = session.query(Tag).all()
    
    s = db(dbfile)

    # a4 = Article(timestamp=,title='a1',tag_id=tagid,user_id=userid,link='111',src_id=srcid)

    a5 = {'timestamp':func.now(),'title':'testtitle','tag':'gesgs','user':'u2','link':'aaaaa','source':'mm'}
    s.insert_article(a5)
    t = s.query_article('testtitle')
    print(t)
    # for x in t:
    #     print(x.link)
    # print(a5['tag'])