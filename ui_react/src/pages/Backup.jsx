import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, Download, RotateCcw, AlertTriangle } from 'lucide-react';

export default function Backup() {
  const [backups, setBackups] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadBackups = () => {
    axios.get('/api/backup/list')
      .then(res => setBackups(Array.isArray(res.data) ? res.data : []))
      .catch(console.error);
  };

  useEffect(() => {
    loadBackups();
  }, []);

  const handleBackup = () => {
    setLoading(true);
    axios.post('/api/backup')
      .then(res => {
        alert(res.data.message + '\nمسیر: ' + res.data.path);
        loadBackups();
      })
      .catch(err => alert("خطا در تهیه پشتیبان"))
      .finally(() => setLoading(false));
  };

  const handleRestore = (path) => {
    if (!window.confirm('آیا مطمئن هستید؟ تمام داده‌های فعلی با داده‌های این فایل جایگزین خواهند شد. این عملیات غیرقابل بازگشت است!')) return;

    setLoading(true);
    axios.post('/api/restore', { path })
      .then(res => alert(res.data.message))
      .catch(err => alert("خطا در بازیابی: " + (err.response?.data?.detail || err.message)))
      .finally(() => setLoading(false));
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <Database className="text-brand" />
        پشتیبان‌گیری و بازیابی دیتابیس
      </h2>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
        <p className="text-gray-600 mb-6">
          شما می‌توانید در هر زمان از تمامی اطلاعات خود (پرسنل، حوادث، انبار و ...) یک فایل پشتیبان تهیه کنید.
          توصیه می‌شود حداقل هفته‌ای یکبار این کار را انجام دهید.
        </p>
        <button
          onClick={handleBackup}
          disabled={loading}
          className="bg-brand text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg hover:bg-brand-dark transition transform hover:scale-105"
        >
          <Download size={20} />
          {loading ? 'در حال پردازش...' : 'تهیه نسخه پشتیبان جدید'}
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
        <h3 className="font-bold text-gray-800 p-6 bg-gray-50 border-b border-gray-200">فایل‌های پشتیبان موجود</h3>
        <ul className="divide-y divide-gray-100">
          {backups.map(b => (
            <li key={b.path} className="p-4 flex items-center justify-between hover:bg-gray-50 transition">
              <div>
                <div className="font-bold text-gray-800 dir-ltr text-left">{b.name}</div>
                <div className="text-xs text-gray-500 mt-1 text-left">{Math.round(b.size / 1024)} KB | {b.path}</div>
              </div>
              <button
                onClick={() => handleRestore(b.path)}
                disabled={loading}
                className="bg-red-50 text-red-600 px-4 py-2 rounded-lg font-bold flex items-center gap-2 hover:bg-red-100 transition"
              >
                <RotateCcw size={16} />
                بازیابی
              </button>
            </li>
          ))}
          {backups.length === 0 && (
            <li className="p-8 text-center text-gray-500">هیچ فایل پشتیبانی یافت نشد.</li>
          )}
        </ul>
      </div>

      <div className="bg-orange-50 border-r-4 border-orange-500 p-4 rounded-lg flex items-start gap-3">
         <AlertTriangle className="text-orange-500 flex-shrink-0" />
         <p className="text-sm text-orange-800">
           <strong>توجه:</strong> عملیات بازیابی (Restore) باعث می‌شود اطلاعات فعلی دیتابیس کاملاً حذف شده و با اطلاعات فایل انتخابی جایگزین شود. قبل از بازیابی حتماً یک بکاپ جدید بگیرید.
         </p>
      </div>
    </div>
  );
}
