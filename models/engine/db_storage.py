from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                .format(user, passwd, host, db),
                pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return dic

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        fetches specific object
        :param cls: class of object as string
        :param id: id of object as string
        :return: found object or None
        """
        all_class = self.all(cls)

        for obj in all_class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        count of how many instances of a class
        :param cls: class name
        :return: count of instances of a class
        """
        return len(self.all(cls))

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()

    def get(self, cls, id):
        """Retrieve one object by class and id"""
        return self.__session.query(cls).filter_by(id=id).first()

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        else:
            count = 0
            for cls in [State, City, User, Place, Review, Amenity]:
                count += self.__session.query(cls).count()
            return count

