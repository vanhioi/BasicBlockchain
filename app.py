from flask import Flask, request, jsonify, render_template
from models.Blockchain import Blockchain, Transaction  # Import từ mã nguồn

app = Flask(__name__)

# Khởi tạo Blockchain
student_blockchain = Blockchain()

# =============================
# ROUTES
# =============================

@app.route('/')
def index():
    """Trang chính: Giao diện nhập giao dịch."""
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Thêm giao dịch mới."""
    data = request.form
    student_id = data.get('student_id')
    course = data.get('course')
    score = data.get('score')

    if not student_id or not course or not score:
        return jsonify({'message': 'Vui lòng điền đầy đủ thông tin!'}), 400

    try:
        score = float(score)
        transaction = Transaction(student_id, course, score)
        student_blockchain.addTransaction(transaction)
        return jsonify({'message': 'Giao dịch đã được thêm thành công!'})
    except ValueError:
        return jsonify({'message': 'Điểm số không hợp lệ!'}), 400

@app.route('/mine_block', methods=['POST'])
def mine_block():
    """Khai thác block."""
    if not student_blockchain.pending_transactions:
        return jsonify({'message': 'Không có giao dịch chờ xử lý!'}), 400

    student_blockchain.minePendingTransactions()
    return jsonify({'message': f"Block {len(student_blockchain.chain) - 1} đã được khai thác thành công!"})

@app.route('/blockchain', methods=['GET'])
def view_blockchain():
    """Hiển thị toàn bộ Blockchain."""
    chain_data = []
    for block in student_blockchain.chain:
        block_data = {
            'index': block.index,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'merkle_root': block.merkle_root,
            'timestamp': block.timestamp,
            'transactions': [tx.toDict() for tx in block.transactions]
        }
        chain_data.append(block_data)
    return jsonify({'chain': chain_data, 'length': len(chain_data)})

@app.route('/block/<int:block_index>', methods=['GET'])
def block_details(block_index):
    """Hiển thị chi tiết một block."""
    if block_index >= len(student_blockchain.chain):
        return jsonify({'message': 'Block không tồn tại!'}), 404

    block = student_blockchain.chain[block_index]
    block_data = {
        'index': block.index,
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'merkle_root': block.merkle_root,
        'timestamp': block.timestamp,
        'transactions': [tx.toDict() for tx in block.transactions]
    }
    return jsonify(block_data)

# =============================
# KHỞI CHẠY SERVER
# =============================

if __name__ == '__main__':
    app.run(debug=True)
