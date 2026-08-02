import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Medical() {
  const fields = [
    { key: "personnel_id", label: "شناسه پرسنل", type: "number", required: true },
    { key: "exam_type", label: "نوع معاینه", type: "select", options: ["ادیومتری", "اسپیرومتری", "عمومی", "بینایی‌سنجی"] },
    { key: "exam_date_shamsi", label: "تاریخ معاینه", type: "text", required: true, placeholder: "1403/01/01" },
    { key: "next_due_date_shamsi", label: "تاریخ معاینه بعدی", type: "text", placeholder: "1404/01/01" },
    { key: "result", label: "نتیجه", type: "text" },
    { key: "notes", label: "توضیحات", type: "textarea" }
  ];

  const listColumns = [
    { key: "personnel_id", label: "شناسه پرسنل" },
    { key: "exam_type", label: "نوع معاینه" },
    { key: "exam_date_shamsi", label: "تاریخ معاینه" },
    { key: "result", label: "نتیجه" }
  ];

  return <CrudPage title="طب کار و معاینات" endpoint="medical_exams" fields={fields} listColumns={listColumns} />;
}
