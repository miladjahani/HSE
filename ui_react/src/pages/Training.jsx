import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Training() {
  const fields = [
    { key: "personnel_id", label: "شناسه پرسنل", type: "number", required: true },
    { key: "course_id", label: "شناسه دوره", type: "number", required: true },
    { key: "completion_date_shamsi", label: "تاریخ اتمام (1403/01/01)", type: "text", required: true, placeholder: "1403/01/01" },
    { key: "expiry_date_shamsi", label: "تاریخ انقضا", type: "text", placeholder: "1404/01/01" },
    { key: "score", label: "نمره", type: "text" }
  ];

  const listColumns = [
    { key: "personnel_id", label: "شناسه پرسنل" },
    { key: "course_id", label: "شناسه دوره" },
    { key: "completion_date_shamsi", label: "تاریخ اتمام" },
    { key: "score", label: "نمره" }
  ];

  return <CrudPage title="ثبت دوره‌های آموزشی" endpoint="training_records" fields={fields} listColumns={listColumns} />;
}
