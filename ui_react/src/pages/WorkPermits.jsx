import React from 'react';
import CrudPage from '../components/CrudPage';

export default function WorkPermits() {
  const fields = [
    { key: "month_shamsi", label: "ماه (مثال: 1403/01)", type: "text", required: true, placeholder: "1403/01" },
    { key: "permit_count", label: "تعداد مجوزهای صادر شده", type: "number", required: true }
  ];

  const listColumns = [
    { key: "month_shamsi", label: "ماه" },
    { key: "permit_count", label: "تعداد مجوزها" }
  ];

  return <CrudPage title="ثبت مجوزهای کار (Work Permits)" endpoint="work_permits" fields={fields} listColumns={listColumns} />;
}
