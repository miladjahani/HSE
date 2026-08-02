import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Incidents() {
  const fields = [
    { key: "incident_date_shamsi", label: "تاریخ", type: "text", required: true, placeholder: "1403/01/01" },
    { key: "incident_type", label: "نوع", type: "select", options: ["حادثه", "شبه‌حادثه", "نزدیک به حادثه"] },
    { key: "severity", label: "شدت", type: "select", options: ["جزئی", "متوسط", "شدید", "فوت"] },
    { key: "risk_assessment_level", label: "سطح ریسک", type: "select", options: ["Critical", "High", "Medium", "Low"] },
    { key: "lost_time_days", label: "روزهای از دست رفته", type: "number" },
    { key: "personnel_id", label: "شناسه پرسنل مرتبط", type: "number" },
    { key: "action_status", label: "وضعیت اقدام", type: "select", options: ["باز", "در حال انجام", "بسته"] },
    { key: "description", label: "شرح حادثه", type: "textarea" },
  ];

  const listColumns = [
    { key: "incident_date_shamsi", label: "تاریخ" },
    { key: "incident_type", label: "نوع" },
    { key: "severity", label: "شدت" },
    { key: "action_status", label: "وضعیت" }
  ];

  return <CrudPage title="مدیریت حوادث" endpoint="incidents" fields={fields} listColumns={listColumns} />;
}
