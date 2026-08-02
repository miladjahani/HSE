import React from 'react';
import CrudPage from '../components/CrudPage';

export default function ManHours() {
  const fields = [
    { key: "month_shamsi", label: "ماه (مثال: 1403/01)", type: "text", required: true, placeholder: "1403/01" },
    { key: "total_employees", label: "تعداد کل پرسنل", type: "number", required: true },
    { key: "man_hours", label: "نفر-ساعت کارکرد", type: "number", required: true }
  ];

  const listColumns = [
    { key: "month_shamsi", label: "ماه" },
    { key: "total_employees", label: "تعداد پرسنل" },
    { key: "man_hours", label: "نفر-ساعت" }
  ];

  return <CrudPage title="ثبت نفر-ساعت کارکرد" endpoint="man_hours" fields={fields} listColumns={listColumns} />;
}
