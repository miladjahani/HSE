import React, { useState } from 'react';
import axios from 'axios';

export default function SetupWizard({ onComplete }) {
  const [formData, setFormData] = useState({ company_name: '', mine_name: '', license_no: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.company_name) return alert("نام شرکت الزامی است");
    axios.post('/api/workspace', formData).then(onComplete).catch(console.error);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-white">راه اندازی اولیه فضای کاری</h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-gray-300">نام شرکت *</label>
              <div className="mt-1">
                <input required type="text" className="appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand focus:border-brand sm:text-sm bg-gray-700 text-white" value={formData.company_name} onChange={e => setFormData({...formData, company_name: e.target.value})} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300">نام معدن</label>
              <div className="mt-1">
                <input type="text" className="appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-brand focus:border-brand sm:text-sm bg-gray-700 text-white" value={formData.mine_name} onChange={e => setFormData({...formData, mine_name: e.target.value})} />
              </div>
            </div>
            <div>
              <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-brand hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand">
                ثبت و ورود
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
