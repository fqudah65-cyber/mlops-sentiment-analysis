# كيفية إنشاء GitHub وتحميل المشروع

## الخطوة 1: إنشاء حساب GitHub (إذا ما عندك)

### 1.1 اذهب إلى الموقع
- افتح المتصفح
- اكتب: `github.com`
- اضغط Sign Up (التسجيل)

### 1.2 ملأ البيانات
- **Username**: اختر اسم مستخدم (مثال: farah-alqudah-164312)
- **Email**: بريدك الجامعي أو الشخصي
- **Password**: كلمة مرور قوية

### 1.3 تأكيد البريد
- ستصلك رسالة على البريد
- اضغط على الرابط في الرسالة
- تم! الحساب جاهز

---

## الخطوة 2: إنشاء Repository جديد

### 2.1 اضغط على الزر الأخضر
- بعد تسجيل الدخول
- اضغط على `+` في أعلى اليمين
- اختر `New repository`

### 2.2 ملأ معلومات Repository
- **Repository name**: `ai381-mlops-sentiment-analysis`
- **Description**: `AI 381 Final Project - Sentiment Analysis MLOps System`
- **Public**: اختر Public (عام)
- **Initialize**: لا تختر أي خيار

### 2.3 اضغط Create Repository
- تم! Repository جاهز

---

## الخطوة 3: رفع الملفات على GitHub

### الطريقة الأولى: باستخدام Git (الأسهل)

#### 3.1 ثبت Git (إذا ما عندك)
**على Windows:**
- اذهب إلى: `git-scm.com`
- اضغط Download
- ثبت البرنامج

**على Mac:**
```bash
brew install git
```

**على Linux:**
```bash
sudo apt-get install git
```

#### 3.2 فتح Terminal/Command Prompt

**على Windows:**
- اضغط Windows + R
- اكتب: `cmd`
- اضغط Enter

**على Mac/Linux:**
- افتح Terminal

#### 3.3 انسخ الملفات

```bash
# اذهب إلى مجلد المشروع
cd /path/to/ai381_mlops_project

# أو إذا فك الضغط
cd ~/ai381_mlops_project
```

#### 3.4 أعد تهيئة Git

```bash
git init
git add .
git commit -m "AI 381 Final Project - Sentiment Analysis MLOps System"
```

#### 3.5 أضف الـ Remote

اذهب إلى GitHub repository اللي أنشأته وانسخ الرابط (يكون شبه هيك):
```
https://github.com/YOUR_USERNAME/ai381-mlops-sentiment-analysis.git
```

ثم اكتب:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ai381-mlops-sentiment-analysis.git
git branch -M main
git push -u origin main
```

#### 3.6 ادخل بيانات GitHub
- سيطلب منك اسم المستخدم والكلمة المرورية
- ادخلها

#### 3.7 تم!
- اذهب إلى GitHub
- ستشوف كل الملفات موجودة

---

### الطريقة الثانية: Upload مباشر من GitHub

#### 3.1 اذهب إلى Repository
- افتح صفحة Repository اللي أنشأته

#### 3.2 اضغط Add file
- اضغط على `Add file`
- اختر `Upload files`

#### 3.3 اسحب الملفات
- اسحب كل الملفات من المشروع
- أو اضغط `choose your files`

#### 3.4 اضغط Commit
- اكتب رسالة: `Initial commit: AI 381 Final Project`
- اضغط `Commit changes`

#### 3.5 تم!
- كل الملفات موجودة الآن

---

## الخطوة 4: تفعيل GitHub Actions (CI/CD)

### 4.1 اذهب إلى Actions
- في Repository
- اضغط على تبويب `Actions`

### 4.2 اضغط Enable
- إذا كان معطل، اضغط `Enable GitHub Actions`

### 4.3 تم!
- الـ CI/CD pipeline بيشتغل تلقائياً

---

## الخطوة 5: الحصول على الرابط

### 5.1 انسخ رابط Repository
- في صفحة Repository
- اضغط الزر الأخضر `Code`
- انسخ الرابط

### 5.2 الرابط يكون شبه هيك:
```
https://github.com/YOUR_USERNAME/ai381-mlops-sentiment-analysis
```

### 5.3 استخدم هذا الرابط للتسليم على E-Learning

---

## نصائح مهمة

✅ **تأكد أن Repository عام (Public)**
- اذهب إلى Settings
- تأكد Public مختار

✅ **تأكد من وجود كل الملفات**
- اذهب إلى Code tab
- شوف كل الملفات موجودة

✅ **اضغط على Actions**
- شوف CI/CD pipeline يشتغل
- يجب تشوف ✅ بجانب الـ commits

✅ **اضغط على README.md**
- يجب تشوف المحتوى يظهر بشكل جميل

---

## حل المشاكل

### المشكلة: "fatal: not a git repository"
**الحل:**
```bash
git init
```

### المشكلة: "Permission denied"
**الحل:**
```bash
# استخدم HTTPS بدل SSH
git remote set-url origin https://github.com/YOUR_USERNAME/repo.git
```

### المشكلة: "Branch main not found"
**الحل:**
```bash
git branch -M main
git push -u origin main
```

### المشكلة: الملفات ما ظهرت
**الحل:**
- انتظر 5 دقائق
- اضغط Refresh في المتصفح
- تأكد من أن الـ push نجح

---

## الخطوة النهائية

بعد ما تخلص:
1. ✅ Repository موجود على GitHub
2. ✅ كل الملفات موجودة
3. ✅ CI/CD pipeline يشتغل
4. ✅ الرابط جاهز للتسليم

**الرابط اللي تسلمه على E-Learning:**
```
https://github.com/YOUR_USERNAME/ai381-mlops-sentiment-analysis
```

---

## أمثلة من الأسماء

**مثال 1:**
```
https://github.com/farah-alqudah-164312/ai381-mlops-sentiment-analysis
```

**مثال 2:**
```
https://github.com/mahaba-alkhawaldeh-161271/ai381-mlops-sentiment-analysis
```

---

**تم! الآن عندك GitHub repository جاهز للتسليم** ✅
