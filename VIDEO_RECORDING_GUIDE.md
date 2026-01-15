# كيفية تسجيل فيديو توضيحي للمشروع

## المتطلبات

**المدة:** 5-10 دقائق
**الصيغة:** MP4
**الجودة:** 1080p (أو أقل)
**الصوت:** واضح

---

## الخطوة 1: اختيار برنامج التسجيل

### على Windows:
**الخيار 1: Windows 10 Screen Recorder (مدمج)**
- اضغط Windows + G
- سيفتح Game Bar
- اضغط Record

**الخيار 2: OBS Studio (مجاني)**
- اذهب: `obsproject.com`
- حمّل البرنامج
- ثبته

### على Mac:
**الخيار 1: QuickTime (مدمج)**
- افتح QuickTime Player
- File > New Screen Recording

**الخيار 2: ScreenFlow**
- اشتريه من App Store

### على Linux:
**OBS Studio:**
```bash
sudo apt-get install obs-studio
```

---

## الخطوة 2: إعداد البيئة

### 2.1 ثبت المشروع على جهازك

```bash
# فك ضغط الملف
tar -xzf ai381_final_submission.tar.gz
cd ai381_mlops_project

# ثبت المتطلبات
pip install -r backend/requirements.txt

# شغل المشروع
cd backend/src
python app.py
```

### 2.2 تأكد من أن المشروع يشتغل
```bash
# في terminal آخر
curl http://localhost:5000/health
```

يجب تشوف:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2.3 افتح Postman أو Insomnia (اختياري)
- برنامج لاختبار API
- يسهل عملية التسجيل

---

## الخطوة 3: محتوى الفيديو (الخطة)

### المدة الكلية: 5-10 دقائق

**1. المقدمة (1 دقيقة)**
- "السلام عليكم، هذا مشروع AI 381"
- "اسمي [اسمك]، رقمي الجامعي [رقمك]"
- "المشروع عن: Sentiment Analysis MLOps System"

**2. نظرة عامة على المشروع (1 دقيقة)**
- اشرح المشكلة بإيجاز
- اشرح الحل
- أظهر الهندسة المعمارية (من README)

**3. تشغيل المشروع (1 دقيقة)**
- أظهر كيف تشغل المشروع
- أظهر health check

**4. اختبار API (2-3 دقائق)**
- Login
- تحليل نص واحد
- تحليل batch (عدة نصوص)
- الحصول على معلومات النموذج

**5. اختبارات الكود (1 دقيقة)**
- أظهر تشغيل الاختبارات
- أظهر النتائج

**6. Docker (1 دقيقة)**
- أظهر بناء Docker image
- أظهر تشغيل Container

**7. CI/CD (1 دقيقة)**
- أظهر GitHub Actions
- أظهر الـ pipeline يشتغل

**8. الخاتمة (30 ثانية)**
- "شكراً على المتابعة"
- "الملفات موجودة على GitHub"

---

## الخطوة 4: التسجيل الفعلي

### 4.1 ابدأ التسجيل

**Windows:**
- اضغط Windows + G
- اضغط Record button

**Mac:**
- افتح QuickTime
- اضغط Record

**OBS:**
- اضغط Start Recording

### 4.2 اتبع الخطة

**1. المقدمة:**
```
"السلام عليكم، أنا Farah Alqudah برقم 164312
هذا مشروع AI 381 الفصل النهائي
المشروع عن بناء نظام MLOps لتحليل المشاعر"
```

**2. أظهر الملفات:**
```bash
# افتح المشروع في VS Code أو أي محرر
# أظهر الهيكل:
# - backend/src/
# - backend/tests/
# - docker/
# - .github/workflows/
```

**3. شغل المشروع:**
```bash
cd backend/src
python app.py
```

**4. اختبر API:**

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "student@university.edu", "password": "student123"}'
```

**تحليل نص:**
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

**5. اختبارات:**
```bash
cd backend
pytest tests/ -v
```

**6. Docker:**
```bash
docker build -f docker/Dockerfile -t sentiment-api:latest .
docker run -p 5000:5000 sentiment-api:latest
```

**7. GitHub Actions:**
- اذهب إلى GitHub
- اضغط Actions
- أظهر الـ pipeline

### 4.3 انهِ التسجيل

**Windows:**
- اضغط Windows + G
- اضغط Stop Recording

**Mac:**
- اضغط Stop

**OBS:**
- اضغط Stop Recording

---

## الخطوة 5: تحرير الفيديو (اختياري)

### إذا كنت تريد تحسين الفيديو:

**برامج مجانية:**
- **DaVinci Resolve** (احترافي)
- **OpenShot** (بسيط)
- **Shotcut** (متوسط)

**ما تحتاج تعمل:**
- قص الأجزاء الطويلة
- أضف عنوان في البداية
- أضف موسيقى خفيفة (اختياري)

---

## الخطوة 6: حفظ الفيديو

### 4.1 اختر الصيغة
- **MP4** (الأفضل)
- **MOV** (Mac)
- **AVI** (Windows)

### 4.2 اختر الجودة
- **1080p** (الأفضل)
- **720p** (جيد)
- **480p** (قبول)

### 4.3 احفظ الملف
- اسم الملف: `AI381_Demo_Video.mp4`
- الحجم: يجب يكون أقل من 500 MB

---

## الخطوة 7: رفع الفيديو

### الخيار 1: YouTube (الأسهل)
1. اذهب إلى YouTube
2. اضغط Upload
3. اختر الملف
4. اكتب العنوان والوصف
5. اختر Private (خاص)
6. انسخ الرابط

### الخيار 2: Google Drive
1. اذهب إلى Google Drive
2. اضغط New > File Upload
3. اختر الملف
4. انسخ الرابط

### الخيار 3: تحميل على E-Learning مباشرة
1. احفظ الملف
2. في E-Learning، اضغط Upload
3. اختر الملف

---

## نصائح مهمة

✅ **الصوت:**
- تأكد من أن الميكروفون يشتغل
- تحدث بوضوح وببطء
- لا تتحدث بسرعة

✅ **الشاشة:**
- أكبّر الخط (Ctrl + Plus)
- أغلق الإشعارات
- أغلق البرامج الأخرى

✅ **المحتوى:**
- لا تقرأ من ورقة
- تحدث بشكل طبيعي
- اشرح ما تفعله

✅ **الأخطاء:**
- إذا أخطأت، ابدأ من جديد
- لا تقلق من الأخطاء الصغيرة
- المهم أن تشرح المشروع

✅ **المدة:**
- لا تقل عن 5 دقائق
- لا تزيد عن 10 دقائق
- إذا طالت، قص الأجزاء الطويلة

---

## قائمة التحقق

قبل التسليم:

- [ ] الفيديو يعمل بدون مشاكل
- [ ] الصوت واضح
- [ ] المدة بين 5-10 دقائق
- [ ] الصيغة MP4
- [ ] الحجم أقل من 500 MB
- [ ] الفيديو يغطي جميع النقاط
- [ ] الفيديو موجود على YouTube أو Drive أو E-Learning

---

## مثال على الفيديو

**الوقت | المحتوى**
```
0:00 - 0:30  | المقدمة والتعريف
0:30 - 1:30  | شرح المشروع
1:30 - 2:00  | هيكل الملفات
2:00 - 3:00  | تشغيل المشروع
3:00 - 5:00  | اختبار API
5:00 - 6:00  | اختبارات الكود
6:00 - 7:00  | Docker
7:00 - 8:00  | GitHub Actions
8:00 - 8:30  | الخاتمة
```

---

**تم! الآن عندك فيديو توضيحي جاهز للتسليم** ✅
