from flask import Blueprint, request, jsonify, render_template, current_app
from werkzeug.utils import secure_filename
# from .models import PDFDocument, db
# from .tasks import classify_pdf
import os

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Save to database and trigger task
    from .models import PDFDocument, TaskHistory, db
    from .tasks import classify_pdf

    new_task = TaskHistory(status="Running")
    db.session.add(new_task)
    db.session.commit()
    new_task_id = new_task.id

    pdf = PDFDocument(filename=filename, file_url=file_path)
    db.session.add(pdf)
    db.session.commit()

    task = classify_pdf.apply_async(args=[pdf.id])
    pdf.task_id = new_task_id
    db.session.commit()

    return jsonify({'task_id': new_task_id, 'pdf_id': pdf.id}), 202


@main.route('/tasks', methods=['GET'])
def return_all_tasks():
    from .models import TaskHistory
    tasks = TaskHistory.query.all()

    tasks_data = [
        {"id": task.id, "task_id": task.reference_id, "status": task.status, "timestamp": task.timestamp}
        for task in tasks
    ]
    return jsonify(tasks_data)


@main.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    from .tasks import classify_pdf
    from .models import TaskHistory, db

    task = classify_pdf.AsyncResult(task_id)
    response = {'status': task.state}
    print(task.state)
    if task.state == 'SUCCESS':
        response['result'] = task.result

    update_task = TaskHistory.query.get(task_id)
    update_task.status = task.state
    db.session.commit()

    return jsonify(response)
