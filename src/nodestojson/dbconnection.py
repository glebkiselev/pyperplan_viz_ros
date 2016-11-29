from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from random import choice

engine = create_engine('sqlite:////tmp/visualizer.db', echo=True)
Base = declarative_base(bind=engine)

def graphplan(nodes):
    step = 0
    for graph in s.query(Graph):
        step = graph.step + 1
    g = Graph(step, nodes)
    s.add_all([g])
    s.commit()

def solution(solution):
    step = 0
    for graph in s.query(Graph):
        step = graph.step + 1
    g = Solution(step, solution)
    s.add_all([g])
    s.commit()

class Solution(Base):
    __tablename__ = 'solution'
    step = Column(Integer, primary_key=True)
    tree = Column(String())

    def __init__(self, step, tree):
        self.step = step
        self.tree = tree

class Graph(Base):
    __tablename__ = 'graphs'
    step = Column(Integer, primary_key=True)
    tree = Column(String())

    def __init__(self, step, tree):
        self.step = step
        self.tree = tree
class Rosrecall(Base):
    __tablename__ = 'rosrecalls'
    iterater = Column(Integer, primary_key=True)
    def __init__(self, iterater):
        self.iterater = iterater

Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()