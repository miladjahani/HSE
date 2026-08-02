import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Download } from 'lucide-react';

const TABLES = [
  { id: "personnel", label: "پرسنل" },
  { id: "incidents", label: "حوادث و شبه‌حوادث" },
  { id: "ppe_items", label: "انبار PPE" },
  { id: "ppe_issuance", label: "تحویل PPE" },
  { id: "training_courses", label: "دوره‌های آموزشی" },
  { id: "training_records", label: "ثبت دوره‌های آموزشی" },
  { id: "medical_exams", label: "معاینات طب کار" },
  { id: "disciplinary_records", label: "تشویق و تنبیه" },
  { id: "man_hours", label: "نفر-ساعت کارکرد" },
  { id: "work_permits", label: "مجوزهای کار" },
  { id: "environmental_metrics", label: "شاخص‌های محیط زیست" }
];

export default function Reports() {
  const [selectedTables, setSelectedTables] = useState([]);
  const [useFilters, setUseFilters] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [personnelList, setPersonnelList] = useState([]);
  const [selectedPersonnel, setSelectedPersonnel] = useState([]);

  useEffect(() => {
    axios.get('/api/personnel').then(res => setPersonnelList(res.data)).catch(console.error);
  }, []);

  const handleTableToggle = (id) => {
    if (selectedTables.includes(id)) {
      setSelectedTables(selectedTables.filter(t => t !== id));
    } else {
      setSelectedTables([...selectedTables, id]);
    }
  };

  const handlePersonnelToggle = (id) => {
    if (selectedPersonnel.includes(id)) {
      setSelectedPersonnel(selectedPersonnel.filter(p => p !== id));
    } else {
      setSelectedPersonnel([...selectedPersonnel, id]);
    }
  };

  const handleExport = () => {
    if (selectedTables.length === 0) return alert('حداقل یک جدول را انتخاب کنید.');

    let url = `/api/reports/export?tables=${selectedTables.join(',')}`;
    if (useFilters) {
      if (startDate) url += `&start_date=${startDate}`;
      if (endDate) url += `&end_date=${endDate}`;
      if (selectedPersonnel.length > 0) url += `&personnel_ids=${selectedPersonnel.join(',')}`;
    }

    // Trigger download
    window.open(axios.defaults.baseURL + url, '_blank');
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <FileText className="text-brand" />
        گزارش‌گیری و خروجی اکسل
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Table Selection */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">انتخاب جداول اطلاعاتی</h3>
          <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
            {TABLES.map(t => (
              <label key={t.id} className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 border border-transparent hover:border-gray-200 cursor-pointer transition">
                <input
                  type="checkbox"
                  className="w-5 h-5 text-brand rounded focus:ring-brand"
                  checked={selectedTables.includes(t.id)}
                  onChange={() => handleTableToggle(t.id)}
                />
                <span className="font-medium text-gray-700">{t.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 flex flex-col">
          <h3 className="font-bold text-gray-800 mb-4 border-b pb-2">فیلترهای گزارش</h3>

          <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200 cursor-pointer mb-6">
            <input
              type="checkbox"
              className="w-5 h-5 text-brand rounded focus:ring-brand"
              checked={useFilters}
              onChange={(e) => setUseFilters(e.target.checked)}
            />
            <span className="font-bold text-gray-800">اعمال فیلتر (تاریخ و پرسنل)</span>
          </label>

          {useFilters && (
            <div className="space-y-4 flex-1 overflow-y-auto pr-2">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">از تاریخ (1403/01/01)</label>
                  <input type="text" value={startDate} onChange={e => setStartDate(e.target.value)} className="w-full border rounded-md px-3 py-2" placeholder="1403/01/01" />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">تا تاریخ</label>
                  <input type="text" value={endDate} onChange={e => setEndDate(e.target.value)} className="w-full border rounded-md px-3 py-2" placeholder="1403/12/29" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2 mt-4">محدود به پرسنل خاص:</label>
                <div className="space-y-1 max-h-40 overflow-y-auto border rounded-md p-2 bg-gray-50">
                  {personnelList.map(p => (
                    <label key={p.id} className="flex items-center gap-2 p-1 hover:bg-gray-200 rounded cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedPersonnel.includes(p.id)}
                        onChange={() => handlePersonnelToggle(p.id)}
                      />
                      <span className="text-sm">{p.first_name} {p.last_name} ({p.personnel_code})</span>
                    </label>
                  ))}
                  {personnelList.length === 0 && <span className="text-xs text-gray-400">پرسنلی یافت نشد</span>}
                </div>
              </div>
            </div>
          )}

          <div className="mt-auto pt-6">
            <button
              onClick={handleExport}
              className="w-full bg-brand text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg hover:bg-brand-dark transition transform hover:scale-[1.02]"
            >
              <Download size={20} />
              دریافت فایل اکسل
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
