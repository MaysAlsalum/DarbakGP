# تفعيل البيئة الافتراضية
.\.venv\Scripts\Activate.ps1 

#تأكد من نسخه python
python --version 
py -3.10 --version    

#تأكد من وجود المكتبات 
pip install -r requirements.txt

#New Bransh
git checkout -b new_branch_name


#رفع Branch
git add .
git commit -m "Your commit message"
git push origin new_branch_name

# Run Django
cd backend
python manage.py runserver

# Run FastAPI server (main.py) using Uvicorn with auto-reload for development
uvicorn backend.src.api.main:app --reload