# كيفية أخذ Screenshots (لقطات الشاشة)

## المطلوب

**عدد Screenshots:** 6-8 لقطات
**الصيغة:** PNG أو JPG
**الجودة:** واضحة وقابلة للقراءة

---

## Screenshot 1: Docker Build Success

### الخطوة 1: افتح Terminal
```bash
cd /path/to/ai381_mlops_project
```

### الخطوة 2: شغل أمر البناء
```bash
docker build -f docker/Dockerfile -t sentiment-api:latest .
```

### الخطوة 3: انتظر حتى ينتهي
- يجب تشوف: `Successfully tagged sentiment-api:latest`

### الخطوة 4: اخذ لقطة
- **Windows:** اضغط Print Screen أو Windows + Shift + S
- **Mac:** اضغط Command + Shift + 4
- **Linux:** اضغط Print Screen

### الخطوة 5: احفظ الملف
- اسم الملف: `01_Docker_Build_Success.png`

---

## Screenshot 2: Docker Container Running

### الخطوة 1: شغل Container
```bash
docker run -p 5000:5000 sentiment-api:latest
```

### الخطوة 2: انتظر حتى يشتغل
- يجب تشوف: `Running on http://0.0.0.0:5000`

### الخطوة 3: اخذ لقطة
- أظهر أن Container يشتغل بنجاح

### الخطوة 4: احفظ الملف
- اسم الملف: `02_Docker_Container_Running.png`

---

## Screenshot 3: API Health Check Response

### الخطوة 1: افتح Terminal جديد
```bash
curl http://localhost:5000/health
```

### الخطوة 2: شوف الرد
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### الخطوة 3: اخذ لقطة
- أظهر الـ response الكامل

### الخطوة 4: احفظ الملف
- اسم الملف: `03_API_Health_Check.png`

---

## Screenshot 4: API Login Success

### الخطوة 1: اختبر Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "student@university.edu", "password": "student123"}'
```

### الخطوة 2: شوف الرد
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "username": "student@university.edu",
    "role": "student"
  }
}
```

### الخطوة 3: اخذ لقطة
- أظهر الـ token والـ user info

### الخطوة 4: احفظ الملف
- اسم الملف: `04_API_Login_Success.png`

---

## Screenshot 5: Sentiment Analysis Response

### الخطوة 1: احصل على Token أولاً
```bash
# من الخطوة السابقة، انسخ access_token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### الخطوة 2: اختبر التحليل
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

### الخطوة 3: شوف الرد
```json
{
  "text": "This product is amazing!",
  "sentiment": "positive",
  "confidence": 0.92,
  "probabilities": {
    "positive": 0.92,
    "negative": 0.05,
    "neutral": 0.03
  }
}
```

### الخطوة 4: اخذ لقطة
- أظهر النتيجة الكاملة

### الخطوة 5: احفظ الملف
- اسم الملف: `05_Sentiment_Analysis_Response.png`

---

## Screenshot 6: Tests Passing

### الخطوة 1: شغل الاختبارات
```bash
cd backend
pytest tests/ -v
```

### الخطوة 2: انتظر حتى تنتهي
- يجب تشوف: `passed` أو `✓`

### الخطوة 3: اخذ لقطة
- أظهر أن جميع الاختبارات نجحت

### الخطوة 4: احفظ الملف
- اسم الملف: `06_Tests_Passing.png`

---

## Screenshot 7: GitHub Actions Workflow

### الخطوة 1: اذهب إلى GitHub
- افتح المتصفح
- اذهب إلى: `github.com/YOUR_USERNAME/ai381-mlops-sentiment-analysis`

### الخطوة 2: اضغط على Actions
- في الأعلى، اضغط تبويب `Actions`

### الخطوة 3: شوف الـ Workflows
- يجب تشوف CI/CD pipeline
- يجب تشوف ✅ بجانب الـ commits

### الخطوة 4: اخذ لقطة
- أظهر أن الـ pipeline يشتغل بنجاح

### الخطوة 5: احفظ الملف
- اسم الملف: `07_GitHub_Actions_Workflow.png`

---

## Screenshot 8: GitHub Repository

### الخطوة 1: اذهب إلى Repository
- في GitHub، اضغط على `Code` tab

### الخطوة 2: أظهر الملفات
- يجب تشوف كل الملفات موجودة

### الخطوة 3: اخذ لقطة
- أظهر هيكل المشروع

### الخطوة 4: احفظ الملف
- اسم الملف: `08_GitHub_Repository_Structure.png`

---

## طريقة أخذ Screenshots

### على Windows:

**الطريقة 1: Print Screen**
```
1. اضغط Print Screen
2. افتح Paint
3. اضغط Ctrl + V
4. اضغط File > Save As
5. اختر PNG
6. احفظ
```

**الطريقة 2: Windows + Shift + S**
```
1. اضغط Windows + Shift + S
2. اسحب لاختيار الجزء
3. سيُحفظ تلقائياً
```

### على Mac:

**الطريقة 1: Command + Shift + 4**
```
1. اضغط Command + Shift + 4
2. اسحب لاختيار الجزء
3. سيُحفظ على Desktop
```

**الطريقة 2: Command + Shift + 5**
```
1. اضغط Command + Shift + 5
2. اختر الخيار
3. اضغط Capture
```

### على Linux:

**الطريقة 1: Print Screen**
```
1. اضغط Print Screen
2. ستُحفظ تلقائياً
```

**الطريقة 2: استخدم Gnome Screenshot**
```bash
gnome-screenshot
```

---

## نصائح مهمة

✅ **الوضوح:**
- تأكد أن الخط واضح
- أكبّر الشاشة إذا لزم
- استخدم 1080p أو أعلى

✅ **الاكتمال:**
- أظهر الـ command والـ output
- لا تقطع أجزاء مهمة
- أظهر الأخطاء إذا حدثت

✅ **الترتيب:**
- رقّم الملفات (01, 02, 03...)
- اتبع الترتيب المنطقي
- ابدأ من البناء ثم الاختبار

✅ **الصيغة:**
- استخدم PNG (أفضل)
- أو JPG (مقبول)
- لا تستخدم BMP

✅ **الحجم:**
- يجب يكون واضح
- لا تقلل الحجم جداً
- لا تزيد الحجم جداً

---

## قائمة التحقق

قبل التسليم:

- [ ] 8 لقطات موجودة
- [ ] كل لقطة واضحة وقابلة للقراءة
- [ ] الملفات مرقمة (01, 02, 03...)
- [ ] الصيغة PNG أو JPG
- [ ] جميع الأوامر والنتائج موجودة
- [ ] GitHub Actions يظهر بنجاح
- [ ] Repository يظهر بنجاح

---

## أسماء الملفات

```
01_Docker_Build_Success.png
02_Docker_Container_Running.png
03_API_Health_Check.png
04_API_Login_Success.png
05_Sentiment_Analysis_Response.png
06_Tests_Passing.png
07_GitHub_Actions_Workflow.png
08_GitHub_Repository_Structure.png
```

---

## كيفية التسليم

### الخيار 1: ملف ZIP
```bash
# ضع كل الـ screenshots في مجلد
# اضغط كليك يمين > Send to > Compressed folder
# احفظ باسم: Screenshots.zip
```

### الخيار 2: تحميل على E-Learning
1. اذهب إلى E-Learning
2. اضغط Upload
3. اختر كل الملفات
4. اضغط Upload

### الخيار 3: Google Drive
1. اذهب إلى Google Drive
2. اضغط New > Folder
3. اسم المجلد: Screenshots
4. اسحب الملفات فيه
5. انسخ رابط المجلد

---

**تم! الآن عندك Screenshots جاهزة للتسليم** ✅
