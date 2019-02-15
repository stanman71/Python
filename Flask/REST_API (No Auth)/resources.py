from models import Todo

from flask_restful import reqparse, abort, Resource, fields, marshal_with
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


""" ######## """
""" database """
""" ######## """

Session = sessionmaker(autocommit = False,
                       autoflush  = False,
                       bind       = create_engine('mysql+pymysql://python:python@localhost/python'))
session = scoped_session(Session)

todo_fields = {
    'id'  : fields.Integer,
    'task': fields.String,
    'uri' : fields.Url('todo', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


""" ######### """
""" functions """
""" ######### """

class TodoResource(Resource):
    @marshal_with(todo_fields)
    def get(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        return todo

    def delete(self, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if not todo:
            abort(404, message="Todo {} doesn't exist".format(id))
        session.delete(todo)
        session.commit()
        return {}, 204

    @marshal_with(todo_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        todo = session.query(Todo).filter(Todo.id == id).first()
        todo.task = parsed_args['task']
        session.add(todo)
        session.commit()
        return todo, 201


class TodoListResource(Resource):
    @marshal_with(todo_fields)
    def get(self):
        todos = session.query(Todo).all()
        return todos

    @marshal_with(todo_fields)
    def post(self):
        parsed_args = parser.parse_args()
        todo = Todo(task=parsed_args['task'])
        session.add(todo)
        session.commit()
        return todo, 201
