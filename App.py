from dataclasses import field
from unicodedata import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, all_
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/employee_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    sex = db.Column(db.String(1))
    salary = db.Column(db.Integer)
    branch_id = db.Column(db.Integer)
    deleted = db.Column(db.Boolean(), default=False)

    def to_dict(self):
        return dict(
            emp_id=self.emp_id,
            first_name=self.first_name,
            last_name=self.last_name,
            sex=self.sex,
            salary=self.salary,
            branch_id=self.branch_id,
            deleted=self.deleted
        )


class employeeSchema(ma.Schema):
    class Meta:
        field = ('emp_id', 'first_name', 'last_name',
                 'sex', 'salary', 'branch_id', 'deleted')


employee_schema = employeeSchema()
employees_schema = employeeSchema(many=True)


@app.route('/post', methods=['POST'])
def add_employee():
    emp = employee(**request.get_json())
    db.session.add(emp)
    db.session.commit()


@app.route('/get', methods=['GET'])
def get_employee():
    emp = employee.query.all()
    return jsonify([u.to_dict() for u in emp])


@app.route('/employee_details/<id>/', methods=['GET'])
def employee_details(id):
    emp = employee.query.get(id)
    print(emp, 'emp')
    return jsonify(emp.to_dict())


@app.route('/employee_update/<id>/', methods=['PUT'])
def employee_update(id):
    emp = employee.query.get(id)
    emp_id = request.json['emp_id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    sex = request.json['sex']
    salary = request.json['salary']
    branch_id = request.json['branch_id']

    employee.emp_id = emp_id
    employee.first_name = first_name
    employee.last_name = last_name
    employee.sex = sex
    employee.salary = salary
    employee.branch_id = branch_id

    db.session.commit()
    return employee_schema.jsonify(emp.to_dict())


@app.route('/employee_delete/<id>/', methods=['DELETE'])
def employee_delete(id):
    employees = employee.query.get(id)
    employees.deleted = True
    db.session.commit()
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)