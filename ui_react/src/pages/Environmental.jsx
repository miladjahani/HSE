import React from 'react';
import CrudPage from '../components/CrudPage';

export default function Environmental() {
  const fields = [
    { key: "month_shamsi", label: "ماه (مثال: 1403/01)", type: "text", required: true, placeholder: "1403/01" },
    { key: "water_consumption_m3", label: "مصرف آب (متر مکعب)", type: "number" },
    { key: "water_recovery_m3", label: "بازیافت آب (متر مکعب)", type: "number" },
    { key: "energy_consumption_kwh", label: "مصرف برق (کیلووات ساعت)", type: "number" },
    { key: "gas_consumption_m2", label: "مصرف گاز (متر مکعب)", type: "number" }
  ];

  const listColumns = [
    { key: "month_shamsi", label: "ماه" },
    { key: "water_consumption_m3", label: "مصرف آب" },
    { key: "water_recovery_m3", label: "بازیافت آب" },
    { key: "energy_consumption_kwh", label: "مصرف برق" },
    { key: "gas_consumption_m2", label: "مصرف گاز" }
  ];

  return <CrudPage title="شاخص‌های محیط زیستی" endpoint="environmental_metrics" fields={fields} listColumns={listColumns} />;
}
