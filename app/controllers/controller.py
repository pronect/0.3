from app import db
from app.models.user import User

u1 = User(id='26c940a1-7228-4ea2-a3bc-e6460b172040', name='Бессонов Дмитрий', balance='1000', hold='0', status=1)
db.session.add(u1)
db.session.commit()