import React from 'react';
import CrudPage from '../components/CrudPage';

export default function PpeStock() {
  const fields = [
    { key: "item_name", label: "نام کالا", type: "text", required: true },
    { key: "item_code", label: "کد کالا", type: "text" },
    { key: "unit", label: "واحد", type: "text" },
    { key: "stock_qty", label: "موجودی فعلی", type: "number" },
    { key: "min_qty", label: "حداقل موجودی (هشدار)", type: "number" },
    { key: "shelf_life_months", label: "عمر مفید (ماه)", type: "number" }
  ];

  const listColumns = [
    { key: "item_name", label: "نام کالا" },
    { key: "item_code", label: "کد کالا" },
    { key: "unit", label: "واحد" },
    { key: "stock_qty", label: "موجودی فعلی" },
    { key: "min_qty", label: "حداقل موجودی" }
  ];

  return <CrudPage title="انبار PPE" endpoint="ppe_items" fields={fields} listColumns={listColumns} />;
}
