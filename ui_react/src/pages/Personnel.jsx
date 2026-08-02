import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Personnel() {
  const fields = [
    { key: "personnel_code", label: "کد پرسنلی", type: "text", required: true },
    { key: "first_name", label: "نام", type: "text", required: true },
    { key: "last_name", label: "نام خانوادگی", type: "text", required: true },
    { key: "national_id", label: "کد ملی", type: "text" },
    { key: "position", label: "سمت", type: "text" },
    { key: "department", label: "واحد / بخش", type: "text" },
    { key: "contract_type", label: "نوع قرارداد", type: "select", options: ["رسمی", "قراردادی", "پیمانکار", "کارآموز"] },
    { key: "contract_status", label: "وضعیت قرارداد", type: "select", options: ["فعال", "تعلیق", "پایان‌یافته"] },
    { key: "hire_date_shamsi", label: "تاریخ استخدام (مانند 1403/01/01)", type: "text", placeholder: "1403/01/01" },
    { key: "phone", label: "شماره تماس", type: "text" },
    { key: "ppe_size", label: "سایز لوازم حفاظت فردی", type: "text" }
  ];

  const listColumns = [
    { key: "personnel_code", label: "کد" },
    { key: "first_name", label: "نام" },
    { key: "last_name", label: "نام خانوادگی" },
    { key: "position", label: "سمت" },
    { key: "contract_status", label: "وضعیت" }
  ];

  return <CrudPage title="مدیریت پرسنل" endpoint="personnel" fields={fields} listColumns={listColumns} />;
}
