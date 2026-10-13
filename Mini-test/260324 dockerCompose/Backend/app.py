from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        with pymysql.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 3306)),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'testdb'),
            connect_timeout=5,
            charset='utf8mb4',
        ) as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute('SELECT id, name FROM users ORDER BY id')
                users = cursor.fetchall()

        return jsonify({'data': users})
    except pymysql.MySQLError:
        app.logger.exception('查詢 MySQL 失敗')
        return jsonify({'message': '無法讀取資料庫資料'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)