from flask_seeder import Seeder, Faker, generator

# SQLAlchemy database model


class User(Base):
    def __init__(self, id_num=None, name=None, age=None):
        self.id_num = id_num
        self.name = name
        self.age = age

    def __str__(self):
        return "ID=%d, Name=%s, Age=%d" % (self.id_num, self.name, self.age)

# All seeders inherit from Seeder


class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
                "id_num": generator.Sequence(),
                "name": generator.Name(),
                "age": generator.Integer(start=20, end=100)
            }
        )

        # Create 5 users
        for user in faker.create(5):
            print("Adding user: %s" % user)
            self.db.session.add(user)
