from app import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))
    action = db.Column(db.String(50), nullable=False)  # login, logout, create, update, delete
    module = db.Column(db.String(50), nullable=False)  # auth, users, institutions, courses
    description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))  # IPv4 o IPv6
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuditLog {self.id}: {self.action} - {self.description}>'
