import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search } from 'lucide-react';

export default function PersonnelProfile() {
  const [personnelList, setPersonnelList] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    axios.get('/api/personnel').then(res => setPersonnelList(res.data)).catch(console.error);
  }, []);

  const loadProfile = () => {
    if (!selectedId) return;
    axios.get(`/api/personnel/${selectedId}/profile`)
      .then(res => setProfile(res.data))
      .catch(console.error);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">پرونده جامع پرسنل</h2>

      <div className="bg-white p-4 rounded-lg shadow-sm flex items-end gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-1">جستجو و انتخاب پرسنل</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand focus:border-brand"
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
          >
            <option value="">انتخاب کنید...</option>
            {personnelList.map(p => (
              <option key={p.id} value={p.id}>{p.first_name} {p.last_name} ({p.personnel_code})</option>
            ))}
          </select>
        </div>
        <button onClick={loadProfile} className="bg-brand text-white px-6 py-2 rounded-md hover:bg-brand-dark flex items-center gap-2 font-bold shadow">
          <Search size={18} />
          نمایش پرونده
        </button>
      </div>

      {profile && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-bold text-lg border-b pb-2 mb-4">مشخصات فردی</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div><span className="text-gray-500 text-sm">نام و نام خانوادگی:</span><br/><strong>{profile.first_name} {profile.last_name}</strong></div>
              <div><span className="text-gray-500 text-sm">کد پرسنلی:</span><br/><strong>{profile.personnel_code}</strong></div>
              <div><span className="text-gray-500 text-sm">کد ملی:</span><br/><strong>{profile.national_id || '-'}</strong></div>
              <div><span className="text-gray-500 text-sm">سمت:</span><br/><strong>{profile.position || '-'}</strong></div>
              <div><span className="text-gray-500 text-sm">بخش:</span><br/><strong>{profile.department || '-'}</strong></div>
              <div><span className="text-gray-500 text-sm">شماره تماس:</span><br/><strong>{profile.phone || '-'}</strong></div>
              <div><span className="text-gray-500 text-sm">وضعیت قرارداد:</span><br/><strong>{profile.contract_status}</strong></div>
              <div><span className="text-gray-500 text-sm">سایز PPE:</span><br/><strong>{profile.ppe_size || '-'}</strong></div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
             <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <h3 className="font-bold p-4 bg-gray-50 border-b">تجهیزات حفاظت فردی تحویل‌شده</h3>
                <ul className="divide-y divide-gray-100 max-h-60 overflow-y-auto">
                   {profile.ppe_issuance.map(i => (
                     <li key={i.id} className="p-3 text-sm">
                       <div className="font-semibold text-gray-800">{i.item_name} ({i.qty} عدد)</div>
                       <div className="text-xs text-gray-500 mt-1">تاریخ تحویل: {i.issue_date_shamsi}</div>
                     </li>
                   ))}
                   {profile.ppe_issuance.length === 0 && <li className="p-4 text-center text-gray-500">موردی یافت نشد</li>}
                </ul>
             </div>

             <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <h3 className="font-bold p-4 bg-gray-50 border-b">سوابق پزشکی و طب کار</h3>
                <ul className="divide-y divide-gray-100 max-h-60 overflow-y-auto">
                   {profile.medical_exams.map(i => (
                     <li key={i.id} className="p-3 text-sm">
                       <div className="font-semibold text-gray-800">{i.exam_type} - <span className="text-blue-600">{i.exam_date_shamsi}</span></div>
                       <div className="text-xs text-gray-500 mt-1">نتیجه: {i.result}</div>
                     </li>
                   ))}
                   {profile.medical_exams.length === 0 && <li className="p-4 text-center text-gray-500">موردی یافت نشد</li>}
                </ul>
             </div>

             <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <h3 className="font-bold p-4 bg-gray-50 border-b">سوابق حوادث</h3>
                <ul className="divide-y divide-gray-100 max-h-60 overflow-y-auto">
                   {profile.incidents.map(i => (
                     <li key={i.id} className="p-3 text-sm flex justify-between items-center">
                       <div>
                         <div className="font-semibold text-gray-800">{i.incident_type} ({i.severity})</div>
                         <div className="text-xs text-gray-500 mt-1">{i.incident_date_shamsi}</div>
                       </div>
                       <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs">روز از دست رفته: {i.lost_time_days || 0}</span>
                     </li>
                   ))}
                   {profile.incidents.length === 0 && <li className="p-4 text-center text-gray-500">موردی یافت نشد</li>}
                </ul>
             </div>

             <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <h3 className="font-bold p-4 bg-gray-50 border-b">سوابق آموزشی</h3>
                <ul className="divide-y divide-gray-100 max-h-60 overflow-y-auto">
                   {profile.training_records.map(i => (
                     <li key={i.id} className="p-3 text-sm">
                       <div className="font-semibold text-gray-800">{i.course_title}</div>
                       <div className="text-xs text-gray-500 mt-1">اتمام: {i.completion_date_shamsi} | نمره: {i.score || '-'}</div>
                     </li>
                   ))}
                   {profile.training_records.length === 0 && <li className="p-4 text-center text-gray-500">موردی یافت نشد</li>}
                </ul>
             </div>
          </div>
        </div>
      )}
    </div>
  );
}
