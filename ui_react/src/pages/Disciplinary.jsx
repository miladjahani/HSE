import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Disciplinary() {
  const fields = [
    { key: "personnel_id", label: "شناسه پرسنل", type: "number", required: true },
    { key: "record_type", label: "نوع", type: "select", options: ["تشویق", "تنبیه"] },
    { key: "title", label: "عنوان", type: "text" },
    { key: "description", label: "توضیحات", type: "textarea" },
    { key: "event_date_shamsi", label: "تاریخ (1403/01/01)", type: "text", required: true, placeholder: "1403/01/01" },
    { key: "reward_or_penalty", label: "پاداش یا جریمه", type: "text" }
  ];

  const listColumns = [
    { key: "personnel_id", label: "شناسه پرسنل" },
    { key: "record_type", label: "نوع" },
    { key: "title", label: "عنوان" },
    { key: "event_date_shamsi", label: "تاریخ" }
  ];

  return <CrudPage title="مدیریت تشویق و تنبیه" endpoint="disciplinary_records" fields={fields} listColumns={listColumns} />;
}
