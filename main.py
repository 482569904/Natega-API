from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import gunicorn # هذا السطر ليس ضروريا لكن من الجيد إبقاؤه

app = Flask(__name__)
CORS(app)

# مثال لرابط وهمي لكشف النتائج. هذا ستحتاج لتغييره لاحقاً
NATEGA_SHEET_URL = "https://www.example.com/results-page.html"

@app.route('/search_by_name', methods=['GET'] )
def search_by_name():
    student_name_query = request.args.get('name')

    if not student_name_query:
        return jsonify({"error": "من فضلك أدخل الاسم للبحث"}), 400

    try:
        # بيانات وهمية للتجربة الآن
        mock_html = """
        <html><body>
            <table id="results-table">
                <tr><th>رقم الجلوس</th><th>الاسم</th><th>المجموع</th></tr>
                <tr><td>100100</td><td>أحمد محمد علي</td><td>350</td></tr>
                <tr><td>100101</td><td>منة الله خالد محمود</td><td>395</td></tr>
                <tr><td>100102</td><td>كريم عبد الرحمن السيد</td><td>377</td></tr>
                <tr><td>100103</td><td>أحمد محمد خليل</td><td>361</td></tr>
            </table>
        </body></html>
        """
        soup = BeautifulSoup(mock_html, 'html.parser')
        
        table = soup.find('table', {'id': 'results-table'})
        if not table:
            return jsonify({"error": "لم يتم العثور على جدول النتائج"}), 500
            
        rows = table.find_all('tr')
        found_students = []
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) > 2:
                seating_no = cols[0].text.strip()
                student_name = cols[1].text.strip()
                total_score = cols[2].text.strip()
                if student_name_query in student_name:
                    found_students.append({
                        "seating_no": seating_no,
                        "name": student_name,
                        "score": total_score
                    })
        
        if not found_students:
            return jsonify({"error": "لم يتم العثور على أي طالب بهذا الاسم"}), 404
        
        return jsonify(found_students)

    except Exception as e:
        return jsonify({"error": "حدث خطأ أثناء البحث", "details": str(e)}), 500

# هذا المسار للتأكد أن الخدمة تعمل
@app.route('/')
def index():
    return "API is running successfully!"
