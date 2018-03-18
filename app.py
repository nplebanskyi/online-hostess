from flask import Flask, jsonify, render_template, flash, request, url_for, redirect, json
import sqlite3 as sql
from data_base_processor import *
import uuid
from table_types import TableType

app = Flask(__name__)
dbp = DataBaseProcessor()

@app.route('/api/v0/session', methods=['GET'])
def get_session_token():
    result = {}
    userTypeMap = {
        'user': True,
        'admin': True,
        '__secret__': True
    }
    status = 200

    try:
        userType = request.args['user_type']
    except KeyError as err:
        result['error'] = 'Provided wrong params.'
        status = 400
    except Exception as e:
        result['error'] = str(e)
        status = 500
    else:
        if not (userTypeMap.get(userType) is None):
            result['token'] = uuid.uuid4()
        else:
            status = 400
            result['error'] = 'Unknown user_type'
    finally:
        return app.response_class(
            response = json.dumps(result),
            status = status,
            mimetype = 'application/json'
        )

@app.route('/api/v0/home', methods=['GET'])
def get_establishments():
    result = {}
    rows = dbp.read_all_rows_from_table(TableType.ESTABLISHMENT)
    if not (rows is None):
        colNumber = 4
        i = 0
        formedRows = []
        formedRow = []
        for table in rows:
            if i == 0 and len(formedRow) > 0:
                formedRows.append(formedRow)
                formedRow = []
            formedRow.append(table)
            i = (i + 1) % colNumber
        if len(formedRow) > 0:
            formedRows.append(formedRow)
        rows = formedRows
    print(len(rows))
    print(len(rows[0]))
    if not (rows is None):
        result['establishments'] = rows
    else:
        result['error'] = "Oops... Unexpected error."
    return render_template("home.html", establishmentsRows=rows)

@app.route('/api/v0/establishment-tables/<id>', methods=['GET', 'POST'])
def get_establishment_tables(id):
    try:
        if request.method == 'POST':
            print('POST')
            print(request)
            print(request.form)
            order = {}
            order['name'] = request.form['recipient-name']
            order['surname'] = request.form['recipient-surname']
            order['email'] = request.form['userEmail']
            order['comment'] = request.form['comment']
            order['tableId'] = request.form['table-id']
            dbp.update_table_status(order['tableId'], 'reserved', order['email'])
            print(order)
            error = False
            if error:
                flash('Error.................')
            else:
                return redirect(url_for('get_establishments'))
        elif request.method == 'GET':
            tables = dbp.read_establishment_tables(id)
            return render_template("tables.html", tables=tables)
    except Exception as e:
        print(e)

@app.route('/api/v0/tables', methods=['GET'])
def get_tables():
    result = {}
    rows = dbp.read_all_rows_from_table(TableType.TABLE)
    if not (rows is None):
        result['tables'] = rows
    else:
        result['error'] = "Not found table with id " + id
    return jsonify(result)

@app.route('/api/v0/tables/<id>', methods=['GET'])
def get_table_by_id(id):
    result = {}
    row = dbp.read_row_from_table_by_id(TableType.TABLE, id)
    if not (row is None):
        result['table'] = row
    else:
        result['error'] = "Not found table with id " + id
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

@app.errorhandler(404)
def not_found(error):
    result = { 'error': 'Not found.' }
    return app.response_class(
        response = json.dumps(result),
        status = 404,
        mimetype = 'application/json'
    )
