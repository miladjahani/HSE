import React from 'react';
import CrudPage from '../components/CrudPage';

export default function PpeIssuance() {
  const fields = [
    { key: "personnel_id", label: "شناسه پرسنل", type: "number", required: true },
    { key: "ppe_item_id", label: "کالا (شناسه)", type: "number", required: true },
    { key: "qty", label: "تعداد", type: "number" },
    { key: "issue_date_shamsi", label: "تاریخ تحویل", type: "text", required: true, placeholder: "1403/01/01" },
    { key: "expiry_date_shamsi", label: "تاریخ انقضا", type: "text", placeholder: "1404/01/01" },
    { key: "notes", label: "توضیحات", type: "text" }
  ];

  const listColumns = [
    { key: "personnel_id", label: "شناسه پرسنل" },
    { key: "ppe_item_id", label: "شناسه کالا" },
    { key: "qty", label: "تعداد" },
    { key: "issue_date_shamsi", label: "تاریخ تحویل" },
    { key: "expiry_date_shamsi", label: "تاریخ انقضا" }
  ];

  return <CrudPage title="تحویل PPE به پرسنل" endpoint="ppe_issuance" fields={fields} listColumns={listColumns} />;
}
