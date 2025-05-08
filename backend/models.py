from config import db

class Contact(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    summoner = db.Column(db.String(80), unique=False, nullable=False)
    puuid = db.Column(db.String(200), unique=False, nullable=False)


    def to_json(self):
        return{
            "id": self.id,
            "summoner": self.summoner,
            "puuid": self.puuid
        }
