import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Edit2, Trash2, X } from 'lucide-react';

export default function CrudPage({ title, endpoint, fields, listColumns }) {
  const [data, setData] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({});
  const [editingId, setEditingId] = useState(null);

  const loadData = () => {
    axios.get(`/api/${endpoint}`)
      .then(res => setData(res.data))
      .catch(console.error);
  };

  useEffect(() => {
    loadData();
  }, [endpoint]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingId) {
      axios.put(`/api/${endpoint}/${editingId}`, formData)
        .then(() => { setIsModalOpen(false); loadData(); })
        .catch(console.error);
    } else {
      axios.post(`/api/${endpoint}`, formData)
        .then(() => { setIsModalOpen(false); loadData(); })
        .catch(console.error);
    }
  };

  const handleDelete = (id) => {
    if (window.confirm('آیا از حذف این رکورد مطمئن هستید؟')) {
      axios.delete(`/api/${endpoint}/${id}`)
        .then(loadData)
        .catch(console.error);
    }
  };

  const openNew = () => {
    setFormData({});
    setEditingId(null);
    setIsModalOpen(true);
  };

  const openEdit = (row) => {
    setFormData(row);
    setEditingId(row.id);
    setIsModalOpen(true);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
        <button onClick={openNew} className="flex items-center gap-2 bg-brand text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-brand-dark transition">
          <Plus size={20} />
          ثبت جدید
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-soft border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-right">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                {listColumns.map(col => (
                  <th key={col.key} className="px-6 py-3 text-sm font-semibold text-gray-600">
                    {col.label}
                  </th>
                ))}
                <th className="px-6 py-3 text-sm font-semibold text-gray-600">عملیات</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.map((row) => (
                <tr key={row.id} className="hover:bg-gray-50">
                  {listColumns.map(col => (
                    <td key={col.key} className="px-6 py-4 text-sm text-gray-700">
                      {row[col.key] || '-'}
                    </td>
                  ))}
                  <td className="px-6 py-4 text-sm">
                    <div className="flex gap-3">
                      <button onClick={() => openEdit(row)} className="text-blue-500 hover:text-blue-700 transition"><Edit2 size={18} /></button>
                      <button onClick={() => handleDelete(row.id)} className="text-red-500 hover:text-red-700 transition"><Trash2 size={18} /></button>
                    </div>
                  </td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr><td colSpan={listColumns.length + 1} className="px-6 py-8 text-center text-gray-500">هیچ داده‌ای یافت نشد</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl shadow-float border border-gray-100 w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
              <h3 className="text-lg font-bold text-gray-800">{editingId ? 'ویرایش رکورد' : 'ثبت رکورد جدید'}</h3>
              <button onClick={() => setIsModalOpen(false)} className="text-gray-500 hover:text-gray-700"><X size={24} /></button>
            </div>

            <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {fields.map(field => (
                  <div key={field.key} className={field.type === 'textarea' ? 'col-span-1 md:col-span-2' : ''}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
                    {field.type === 'select' ? (
                      <select
                        required={field.required}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand focus:border-brand"
                        value={formData[field.key] || ''}
                        onChange={e => setFormData({...formData, [field.key]: e.target.value})}
                      >
                        <option value="">انتخاب کنید...</option>
                        {field.options?.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                      </select>
                    ) : field.type === 'textarea' ? (
                       <textarea
                        required={field.required}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand focus:border-brand"
                        rows="3"
                        value={formData[field.key] || ''}
                        onChange={e => setFormData({...formData, [field.key]: e.target.value})}
                      />
                    ) : (
                      <input
                        type={field.type === 'number' ? 'number' : 'text'}
                        required={field.required}
                        placeholder={field.placeholder || ''}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-brand focus:border-brand"
                        value={formData[field.key] || ''}
                        onChange={e => setFormData({...formData, [field.key]: field.type === 'number' ? Number(e.target.value) : e.target.value})}
                      />
                    )}
                  </div>
                ))}
              </div>
              <div className="mt-8 pt-4 border-t border-gray-200 flex justify-end gap-3">
                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">انصراف</button>
                <button type="submit" className="px-6 py-2 bg-brand text-white rounded-md font-bold hover:bg-brand-dark shadow">ذخیره اطلاعات</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
